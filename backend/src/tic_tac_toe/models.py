from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class GameStatus(Enum):
  ONGOING = "ongoing"
  WIN = "win"
  DRAW = "draw"


class Player(Enum):
  O = "O"  # noqa: E741
  X = "X"


class GameLogRecord(BaseModel):
  turn: int = Field(..., description="The game turn number")
  player: Player = Field(..., description="The player who made the move")
  position: int = Field(..., description="The board position taken by the player")
  success: bool = Field(..., description="Whether the move was successful")


class PlayerMoveRequest(BaseModel):
  """Request model for a player move."""

  model_config = ConfigDict(
    extra="ignore",
    populate_by_name=True,
  )

  position: int = Field(
    ...,
    ge=0,
    le=8,
    description="Given a flat array representing the game board (0-2 being row 1, 3-5 being row 2, 6-8 being row 3), this input (0-8) is the position on the board to make the move.",
  )


class BoardUpdateResult(BaseModel):
  success: bool = Field(..., description="Whether the move was successful")
  message: str = Field(..., description="The message from the move")
  board_state: List[Optional[Player]] = Field(..., description="The board state")
  status: GameStatus = Field(..., description="The status of the game")


class BoardState(BaseModel):
  board: list[list[Literal[" ", "X", "O"]]] = Field(..., description="The board state")
  round_number: int = Field(..., ge=1, le=9, description="The round number (1, 2, or 3)")
  current_player: Literal["X", "O"] = Field(..., description="The current player (X or O)")
  is_game_over: bool = Field(..., description="Whether the game is over")
  winner: Literal["X", "O", None] = Field(..., description="The winner (X, O, or None)")
  game_over_reason: Literal["AI wins", "Human wins", "Tie", None] = Field(
    ..., description="The reason the game is over (AI wins, Human wins, Tie, or None)"
  )
