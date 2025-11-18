from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PlayerMove(BaseModel):
  model_config = ConfigDict(
    extra="ignore",
    populate_by_name=True,
  )

  row: int = Field(..., ge=1, le=3, description="The row of the move (1, 2, or 3)")
  col: Literal["a", "b", "c"] = Field(..., description="The column of the move (a, b, or c)")


class BoardState(BaseModel):
  board: list[list[Literal[" ", "X", "O"]]] = Field(..., description="The board state")
  round_number: int = Field(..., ge=1, le=9, description="The round number (1, 2, or 3)")
  current_player: Literal["X", "O"] = Field(..., description="The current player (X or O)")
  is_game_over: bool = Field(..., description="Whether the game is over")
  winner: Literal["X", "O", None] = Field(..., description="The winner (X, O, or None)")
  game_over_reason: Literal["AI wins", "Human wins", "Tie", None] = Field(
    ..., description="The reason the game is over (AI wins, Human wins, Tie, or None)"
  )
