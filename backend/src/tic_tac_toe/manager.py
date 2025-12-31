# backend/src/tic_tac_toe/manager.py
"""Manager class for the tic-tac-toe game."""

from agent_framework import AgentThread, ChatAgent, ChatMessage
from pydantic import BaseModel, ConfigDict
from socketio import AsyncServer

from src.tic_tac_toe.agent import create_tic_tac_toe_agent
from src.tic_tac_toe.game import TicTacToe
from src.tic_tac_toe.models import GameStatus, PlayerMove


class GameSession(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)

  session_id: str
  game: TicTacToe
  agent: ChatAgent
  thread: AgentThread


class TicTacToeManager:
  """Manager class for the tic-tac-toe game."""

  def __init__(self, sio: AsyncServer):
    self.sio = sio
    self.game_sessions: dict[str, GameSession] = {}
    self._register_handlers()

  def _register_handlers(self) -> None:
    """Register all socket event listeners."""
    self.sio.on("connect", self.handle_connect)
    self.sio.on("GAME_RESET", self.handle_game_initialization)
    self.sio.on("USER_MOVE", self.handle_user_move)
    self.sio.on("post_game_query", self.handle_post_game_query)

  def _create_agent_move_tool(self, sid: str, game: TicTacToe):
    """Create a session-specific tool for agent moves with socket emission."""

    async def agent_make_move(position: int) -> dict:
      """Agent tool: Make X move at position, update game, and emit socket events."""
      # Make the move
      result = game.take_X_move(position)

      if not result["success"]:
        return result

      # Emit board update to frontend
      await self.sio.emit(
        "ai_tool_executed",
        {
          "message": result.get("message", ""),
          "board_state": result.get("board_state", []),
          "status": result.get("status", ""),
        },
        to=sid,
      )

      # Check if game is over and emit appropriate event
      status, winner = game.get_game_status()
      if status != GameStatus.ONGOING:
        if status == GameStatus.DRAW:
          await self.sio.emit("GAME_OVER_RESULT", "Tie", to=sid)
        elif winner == "X":
          await self.sio.emit("GAME_OVER_RESULT", "AI wins", to=sid)
        elif winner == "O":
          await self.sio.emit("GAME_OVER_RESULT", "Human wins", to=sid)
        else:
          await self.sio.emit("ERROR", {"message": "Game over reason not found"}, to=sid)

      return result

    # Set function metadata for agent framework
    agent_make_move.__name__ = "agent_make_move"
    agent_make_move.__doc__ = (
      "Make X move at the specified position (0-8). Returns game state and move result."
    )

    return agent_make_move

  # This belongs in its own handler, but included here for demo purposes
  async def handle_connect(self, sid: str, environ: dict):
    """Handle client connection and initialize game session."""
    # User authentication goes here
    print(f"Client connected: {sid}")
    await self.handle_game_initialization(sid)

  # Initialize a new game session
  async def handle_game_initialization(self, sid: str, data: dict = {}):
    """Handle game initialization events."""
    print(f"🔧 Game reset event: {sid}")
    # 1. Find the game session by sid in the game_sessions dictionary (creating it, if it doesn't exist)
    game_session = self.game_sessions.get(sid)
    if not game_session:
      # Initialize the game services (game, agent, agent_thread)
      game = TicTacToe()
      game.reset()  # Sync call, no await
      # Create session-specific agent move tool
      agent_move_tool = self._create_agent_move_tool(sid, game)
      agent = create_tic_tac_toe_agent(game, agent_move_tool)
      # Create the game session
      game_session = GameSession(
        session_id=sid,
        game=game,
        agent=agent,
        thread=AgentThread(),
      )
      self.game_sessions[sid] = game_session
    else:
      # Reset the game in the game session
      # TODO: Kill running thread if necessary
      game_session.game.reset()  # Sync call
      # Recreate agent move tool for the reset game
      agent_move_tool = self._create_agent_move_tool(sid, game_session.game)
      game_session.agent = create_tic_tac_toe_agent(game_session.game, agent_move_tool)
    # Emit updated board state after reset
    await self.sio.emit("BOARD_STATE_UPDATED", game_session.game.get_board(), to=sid)
    return True

  # Handle a user move
  async def handle_user_move(self, sid: str, data: dict = {}):
    """Handle user move events."""
    # 0. Validate the user move data received from the client
    user_move = PlayerMove(**data)
    position = PlayerMove(**data).position
    # 1. Find the game session by sid in the game_sessions dictionary (creating if not exists by calling initialization)
    game_session = self.game_sessions.get(sid)
    if not game_session:
      await self.handle_game_initialization(sid)
      game_session = self.game_sessions[sid]
    # 2. Make the move for the user (human as O)
    result = game_session.game.take_O_move(position)
    if not result["success"]:
      await self.sio.emit("ERROR", {"message": result["message"]}, to=sid)
      return
    print(f"🔧 Move result: {result}")
    # 3. Emit the results of the user's move to the client
    await self.sio.emit("USER_MOVE_RESULT", user_move.model_dump(), to=sid)
    await self.sio.emit("BOARD_STATE_UPDATED", result["board_state"], to=sid)
    # 4. If the game is over, emit the appropriate result to the client (win/loss/tie)
    status, winner = game_session.game.get_game_status()
    if status != GameStatus.ONGOING:
      if status == GameStatus.DRAW:
        await self.sio.emit("GAME_OVER_RESULT", "Tie", to=sid)
      elif winner == "X":
        await self.sio.emit("GAME_OVER_RESULT", "AI wins", to=sid)
      elif winner == "O":
        await self.sio.emit("GAME_OVER_RESULT", "Human wins", to=sid)
      else:
        await self.sio.emit("ERROR", {"message": "Game over reason not found"}, to=sid)
      return
    # 5. If the game is not over, run the agent's response to the user's move
    # The agent will call agent_make_move tool which handles emissions
    if game_session.game.get_current_turn() == "X":
      message_text = (
        f"The user has placed their marker at position {user_move.position}. Your turn!"
      )
      print("Executing agent turn...")
      async for update in game_session.agent.run_stream(
        thread=game_session.thread,
        messages=[ChatMessage(role="user", text=message_text)],
      ):
        # Stream agent updates to frontend (tool handles board/game-over emissions)
        print(f"Agent stream token: {update.to_dict()}")
        update_type = update.to_dict().get("contents", [{}])[0].get("type", "")
        # Reasoning Chunks
        if update_type == "text_reasoning":
          await self.sio.emit("AGENT_REASONING_CHUNK", update.to_dict(), to=sid)
        # Text Chunks
        if update_type == "text":
          await self.sio.emit("AGENT_STREAM_TOKEN", update.to_dict(), to=sid)
        # Function Calling and Results
        elif update_type == "function_call":
          await self.sio.emit("AGENT_FUNCTION_CALL", update.to_dict(), to=sid)
        elif update_type == "function_result":
          await self.sio.emit("AGENT_FUNCTION_RESULT", update.to_dict(), to=sid)

        elif update_type == "game_over":
          await self.sio.emit("AGENT_GAME_OVER", update.to_dict(), to=sid)
        else:
          pass
        await self.sio.emit("AGENT_STREAM_TOKEN", update.to_dict(), to=sid)

  async def handle_post_game_query(self, sid: str, data: dict = {}):
    """Handle post-game query events."""
    query = data.get("query", "").strip()
    if not query:
      return
    # Find the game session
    game_session = self.game_sessions.get(sid)
    if not game_session:
      await self.handle_game_initialization(sid)
      game_session = self.game_sessions[sid]
    # Run the agent with the query and stream response as ai_message
    async for update in game_session.agent.run_stream(
      thread=game_session.thread,
      messages=[ChatMessage(role="user", text=query)],
    ):
      await self.sio.emit(
        "ai_message", {"text": update.to_dict().get("text", "")}, to=sid
      )  # Assuming update has text
    # TODO: Adjust based on actual update structure for ai_message
