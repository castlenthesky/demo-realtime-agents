# src/tic_tac_toe/manager.py
"""Manager class for the tic-tac-toe game."""

from agent_framework import ChatAgent, ChatMessage
from pydantic import BaseModel, ConfigDict
from socketio import AsyncServer

from src.tic_tac_toe.agent import create_tic_tac_toe_agent
from src.tic_tac_toe.game import TicTacToe
from src.tic_tac_toe.models import PlayerMove


class GameSessionData(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)

  game: TicTacToe
  agent: ChatAgent


class GameSession(BaseModel):
  session_id: str
  session: GameSessionData


class TicTacToeManager:
  """Manager class for the tic-tac-toe game."""

  def __init__(self, sio: AsyncServer):
    self.sio = sio
    self.game_sessions: dict[str, GameSession] = {}
    self._register_handlers()

  def _register_handlers(self) -> None:
    """Register all socket event listeners."""
    self.sio.on("GAME_RESET", self.handle_game_reset)
    self.sio.on("USER_MOVE", self.handle_user_move)
    self.sio.on("USER_MESSAGE", self.handle_user_message)

  async def handle_game_reset(self, sid: str, data: dict = {}):
    """Handle game reset events."""
    print(f"🔧 Game reset event: {sid}")
    # 1. Find the game session by sid in the game_sessions dictionary (creating it, if it doesn't exist)
    game_session = self.game_sessions.get(sid)
    if not game_session:
      # Initialize the game services (game, agent, agent_thread)
      game = TicTacToe(sio=self.sio, sid=sid)
      await game.reset()
      agent = create_tic_tac_toe_agent(game)
      # Create the game session
      game_session = GameSession(
        session_id=sid,
        session=GameSessionData(game=game, agent=agent),
      )
      self.game_sessions[sid] = game_session
    else:
      # Reset the game in the game session
      # TODO: Kill running thread

      await game_session.session.game.reset()
      game_session.session.agent = create_tic_tac_toe_agent(game_session.session.game)
    return True

  async def handle_user_move(self, sid: str, data: dict = {}):
    """Handle user move events."""
    # 0. Process the user move data
    user_move = PlayerMove(**data)
    # 1. Find the game session by sid in the game_sessions dictionary (raising an error if it doesn't exist)
    game_session = self.game_sessions.get(sid)
    if not game_session:
      raise ValueError(f"Game session not found for sid: {sid}")
    # 2. Call the method to make the move for the user until the move is successful
    while True:
      try:
        if await game_session.session.game.make_human_move(user_move):
          break
      except Exception as e:
        await self.sio.emit("ERROR", {"message": str(e)}, to=sid)
        print(f"Error making user move: {e}")
        break
    # 3. Emit the results of the user's move to the client
    await self.sio.emit("USER_MOVE_RESULT", user_move.model_dump(), to=sid)
    await self.sio.emit(
      "BOARD_STATE_UPDATED", await game_session.session.game.get_board_state(), to=sid
    )
    # 4. If the game is over, emit the appropriate result to the client (win/loss/tie)
    if game_session.session.game.is_game_over:
      match game_session.session.game.game_over_reason:
        case "AI wins":
          await self.sio.emit("GAME_OVER_RESULT", "AI wins", to=sid)
        case "Human wins":
          await self.sio.emit("GAME_OVER_RESULT", "Human wins", to=sid)
        case "Tie":
          await self.sio.emit("GAME_OVER_RESULT", "Tie", to=sid)
        case _:
          await self.sio.emit("ERROR", {"message": "Game over reason not found"}, to=sid)
    # 5. If the game is not over, run the agent's response to the user's move
    if not game_session.session.game.is_game_over:
      # Only run the agent if it is the agent's turn
      # TODO: Limit the number of times the agent can run
      # TODO: Fix agent tool calling issues
      while not game_session.session.game.is_human_turn:
        message_text = f"The user has placed their marker on row {user_move.row} and column {user_move.col}. Your turn!"
        async for update in game_session.session.agent.run_stream(
          messages=[ChatMessage(role="user", text=message_text)]
        ):
          await self.sio.emit("AGENT_STREAM_TOKEN", update.to_dict(), to=sid)
          # TODO: Add message logging
      await self.sio.emit(
        "AGENT_MOVE_RESULT",
        await game_session.session.game.get_board_state(),
        to=sid,
      )

  async def handle_user_message(self, sid: str, data: dict = {}):
    """Handle user message events."""
    await self.sio.emit("ERROR", {"message": "User message not implemented"}, to=sid)
    raise NotImplementedError("User message not implemented")
