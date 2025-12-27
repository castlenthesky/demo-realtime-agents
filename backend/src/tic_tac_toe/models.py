from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class GameStatus(Enum):
  ONGOING = "ongoing"
  WIN = "win"
  DRAW = "draw"


class Player(Enum):
  O = "O"  # noqa: E741
  X = "X"


class PlayerMove(BaseModel):
  model_config = ConfigDict(
    extra="ignore",
    populate_by_name=True,
  )

  position: int = Field(..., ge=0, le=8, description="The flat board position (0-8)")


class BoardState(BaseModel):
  board: list[list[Literal[" ", "X", "O"]]] = Field(..., description="The board state")
  round_number: int = Field(..., ge=1, le=9, description="The round number (1, 2, or 3)")
  current_player: Literal["X", "O"] = Field(..., description="The current player (X or O)")
  is_game_over: bool = Field(..., description="Whether the game is over")
  winner: Literal["X", "O", None] = Field(..., description="The winner (X, O, or None)")
  game_over_reason: Literal["AI wins", "Human wins", "Tie", None] = Field(
    ..., description="The reason the game is over (AI wins, Human wins, Tie, or None)"
  )
