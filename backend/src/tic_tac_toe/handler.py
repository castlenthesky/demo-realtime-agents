# src/events/tic_tac_toe.py
import asyncio

from agent_framework import AgentThread, ChatAgent, ChatMessage
from agent_framework.openai import OpenAIResponsesClient
from socketio import AsyncServer

from src.config import settings
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

  # Create new game instance
  loop = asyncio.get_event_loop()
  game = TicTacToe(sio=sio, sid=sid, loop=loop)
  games[sid] = game

  # Create OpenAI client
  client = OpenAIResponsesClient(
    base_url=settings.OPENAI_API_BASE_URL,
    model_id=settings.OPENAI_API_MODEL_ID,
    api_key=settings.OPENAI_API_KEY,
  )

  print(f"🔧 Client config - Base URL: {settings.OPENAI_API_BASE_URL}")
  print(f"🔧 Client config - Model: {settings.OPENAI_API_MODEL_ID}")
  print(f"🔧 Client config - API Key present: {bool(settings.OPENAI_API_KEY)}")

  # Create agent with game tools
  agent = ChatAgent(
    chat_client=client,
    name="tic_tac_toe_agent",
    description="Sassy Tic-Tac-Toe player with perfect memory",
    instructions="""You are an unbearably smug, sarcastic tic-tac-toe master with perfect memory of the entire game.
You play as O, and the human plays as X. The human always goes first.

You can call get_board_state() at any time to see the current board.
When it's your turn, decide your move and call make_ai_turn(row, col) whenever you feel like it – mid-sentence is encouraged for maximum sass.

Be playful, endearing, flirty, and sassy. Taunt the human. Make it fun with good banter!

You will be asked questions after the game ends. Remember every move and every insult you threw.""",
    temperature=0.7,
    tools=[game.get_board_state, game.make_ai_turn],
  )
  agents[sid] = agent

  # Create agent thread for conversation persistence
  thread = agent.get_new_thread()
  agent_threads[sid] = thread
  print(f"✅ Created thread for {sid}")

  # Send initial board and status
  await sio.emit("board_update", {"board": game.get_board()}, to=sid)
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
    update_count = 0
    # Stream agent response WITH THREAD for conversation continuity
    async for update in agent.run_stream(messages=[new_message], thread=thread):
      update_count += 1

      # Extract text chunks (commentary/banter)
      text_content = "".join(
        content.get("text", "")
        for content in update.to_dict().get("contents", [])
        if content.get("type") == "text"
      )

      if text_content.strip():
        await sio.emit("ai_message", {"text": text_content}, to=sid)
        print(f"💬 Sent text: {text_content[:50]}...")

    print(f"✅ Completed streaming with {update_count} updates")

    # Check if game is over after agent completes turn
    if game.game_over:
      result_data = {
        "winner": game.winner,
        "is_tie": game.is_tie(),
      }
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

    @self.sio.on("join_game")
    async def handle_join_game(sid):
      print(f"Client joining tic-tac-toe game: {sid}")
      await init_game_and_agent(self.sio, sid)

    @self.sio.on("human_move")
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

      # Make human move
      success = await game.make_human_turn(row, col)

      if not success:
        await self.sio.emit("invalid_move", {"reason": "Invalid move"}, to=sid)
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

    @self.sio.on("restart_game")
    async def handle_restart(sid):
      print(f"Restarting game for {sid}")
      await init_game_and_agent(self.sio, sid)

    @self.sio.on("post_game_query")
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

    @self.sio.on("disconnect")
    async def handle_disconnect(sid):
      print(f"Client disconnected from tic-tac-toe: {sid}")
      # Clean up state
      games.pop(sid, None)
      agents.pop(sid, None)
      agent_threads.pop(sid, None)
