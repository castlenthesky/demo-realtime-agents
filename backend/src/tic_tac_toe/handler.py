# src/events/tic_tac_toe.py
import asyncio

from agent_framework import AgentThread, ChatAgent, ChatMessage
from socketio import AsyncServer

from src.tic_tac_toe.agent import create_agent, execute_agent_turn
from src.tic_tac_toe.game import TicTacToe

# Module-level state dicts for per-connection instances
games: dict[str, TicTacToe] = {}
agents: dict[str, ChatAgent] = {}
agent_threads: dict[str, AgentThread] = {}


async def init_game_and_agent(sio: AsyncServer, sid: str):
  """Initialize or reinitialize game, agent, and thread for a connection."""
  # Clean up old state if exists
  for state_dict in [games, agents, agent_threads]:
    state_dict.pop(sid, None)

  # Create new game instance (no socket params)
  game = TicTacToe()
  games[sid] = game

  # Create agent using agent.py function
  agent = create_agent(game)
  agents[sid] = agent

  # Create agent thread for conversation persistence
  thread = agent.get_new_thread()
  agent_threads[sid] = thread
  print(f"✅ Created thread for {sid}")

  # Send initial board and status
  await sio.emit("board_update", game.get_board_data(), to=sid)
  await sio.emit("status_update", {"text": "New game – your move, human."}, to=sid)
  await sio.emit("ai_message", {"text": "Fresh meat. Let's see how fast you lose."}, to=sid)


async def ai_turn(sio: AsyncServer, sid: str, new_message: ChatMessage):
  """
  Execute AI turn with streaming commentary and tool calls.
  This function handles both in-game moves and post-game queries.
  Uses AgentThread for conversation persistence.
  """
  agent = agents.get(sid)
  game = games.get(sid)
  thread = agent_threads.get(sid)

  if not agent or not game or not thread:
    print(
      f"⚠️ Missing components for {sid}: agent={bool(agent)}, game={bool(game)}, thread={bool(thread)}"
    )
    return

  print(f"🤖 Starting AI turn for {sid}")
  print(f"📨 Message: {new_message.text}")

  try:
    # Track board state before agent execution to detect moves
    board_before = [row[:] for row in game.get_board()]  # Deep copy

    update_count = 0
    # Stream agent response using agent.py function
    async for update_dict in execute_agent_turn(agent, thread, new_message):
      update_count += 1

      # Check if this is an error update
      if update_dict.get("type") == "error":
        error_text = update_dict.get("error", "Unknown error")
        await sio.emit("status_update", {"text": f"AI error: {error_text}"}, to=sid)
        print(f"❌ Agent error: {error_text}")
        return

      # Extract text chunks (commentary/banter)
      text_content = "".join(
        content.get("text", "")
        for content in update_dict.get("contents", [])
        if content.get("type") == "text"
      )

      if text_content.strip():
        await sio.emit("ai_message", {"text": text_content}, to=sid)
        print(f"💬 Sent text: {text_content[:50]}...")

    print(f"✅ Completed streaming with {update_count} updates")

    # Check if agent made a move by comparing board states
    board_after = game.get_board()
    ai_move_made = False
    move_row = None
    move_col = None

    for row_idx in range(3):
      for col_idx in range(3):
        if board_before[row_idx][col_idx] != board_after[row_idx][col_idx]:
          if board_after[row_idx][col_idx] == "O":  # AI made a move
            ai_move_made = True
            move_row = row_idx + 1  # Convert to 1-3
            move_col = ["a", "b", "c"][col_idx]
            break
      if ai_move_made:
        break

    # Emit AI move and board update if a move was made
    if ai_move_made:
      await sio.emit(
        "ai_tool_executed", {"tool": "make_ai_turn", "row": move_row, "col": move_col}, to=sid
      )
      await sio.emit("board_update", game.get_board_data(), to=sid)
      print(f"📡 Emitted AI move: {move_row}{move_col}")

    # Check if game is over after agent completes turn
    if game.game_over:
      result_data = game.get_game_over_data()
      await sio.emit("game_over", result_data, to=sid)
      print(f"🏁 Game over: {result_data}")

  except Exception as e:
    print(f"❌ Agent error for {sid}: {e}")
    import traceback

    traceback.print_exc()
    await sio.emit("status_update", {"text": f"AI error: {str(e)}"}, to=sid)


class TicTacToeHandler:
  """Handler for tic-tac-toe socket events."""

  def __init__(self, sio: AsyncServer):
    self.sio = sio
    self._register_handlers()

  def _register_handlers(self):
    """Register all socket event handlers."""

    @self.sio.on("join_game")  # type: ignore
    async def handle_join_game(sid):
      print(f"Client joining tic-tac-toe game: {sid}")
      await init_game_and_agent(self.sio, sid)

    @self.sio.on("human_move")  # type: ignore
    async def handle_human_move(sid, data):
      game = games.get(sid)
      thread = agent_threads.get(sid)

      if not game or not thread:
        print(f"⚠️ Missing game or thread for {sid}")
        return

      # Check if game is already over
      if game.is_game_over():
        await self.sio.emit("invalid_move", {"reason": "Game is already over"}, to=sid)
        return

      # Check if it's human's turn
      if game.get_current_player() != "X":
        await self.sio.emit("invalid_move", {"reason": "Not your turn"}, to=sid)
        return

      row = data.get("row")
      col = data.get("col")

      print(f"👤 Human move: {row}{col} for {sid}")

      # Make human move (synchronous now)
      success = game.make_human_turn(row, col)

      if not success:
        await self.sio.emit("invalid_move", {"reason": "Invalid move"}, to=sid)
        return

      # Emit human move event and board update
      await self.sio.emit("HUMAN_MOVE_MADE", {"row": row, "col": col}, to=sid)
      await self.sio.emit("board_update", game.get_board_data(), to=sid)

      # Check if game is over after human move
      if game.game_over:
        await self.sio.emit("game_over", game.get_game_over_data(), to=sid)
        return

      # Tell the agent what the human did
      human_move_msg = ChatMessage(
        role="user", text=f"I just placed X at position {row}{col}. Your turn! Be sassy!"
      )

      # Update status
      await self.sio.emit("status_update", {"text": "AI is thinking..."}, to=sid)

      # Trigger AI turn if game is not over
      if not game.is_game_over():
        asyncio.create_task(ai_turn(self.sio, sid, human_move_msg))

    @self.sio.on("restart_game")  # type: ignore
    async def handle_restart(sid):
      print(f"Restarting game for {sid}")
      await init_game_and_agent(self.sio, sid)

    @self.sio.on("post_game_query")  # type: ignore
    async def handle_post_game_query(sid, data):
      thread = agent_threads.get(sid)

      if not thread:
        print(f"⚠️ No thread found for post-game query: {sid}")
        return

      query = data.get("query", "")
      if not query.strip():
        return

      print(f"💭 Post-game query from {sid}: {query}")

      # Create message with user's question
      query_msg = ChatMessage(role="user", text=query)

      # Update status
      await self.sio.emit("status_update", {"text": "AI is thinking..."}, to=sid)

      # Reuse same ai_turn function - works for post-game too!
      asyncio.create_task(ai_turn(self.sio, sid, query_msg))
