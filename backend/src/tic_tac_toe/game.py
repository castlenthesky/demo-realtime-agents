# backend/src/tic_tac_toe/game.py
from typing import List, Optional, Tuple

from src.tic_tac_toe.models import BoardUpdateResult, GameLogRecord, GameStatus, Player


class TicTacToe:
  """
  A class to manage a Tic-Tac-Toe game, tracking state, moves, wins, and providing structured responses.
  The board is a flat list of 9 elements (0-8), with None for empty spots.
  """

  def __init__(self, starting_player: Player = Player.O):
    self.board: List[Optional[Player]] = [None] * 9
    self.current_player: Player = Player.O
    self.game_log: List[GameLogRecord] = []
    self.status: GameStatus = GameStatus.ONGOING
    self.turn: int = 1  # Starts at 1 for the first move

  def reset(self) -> BoardUpdateResult:
    """Reset the game state to initial state."""
    self.board = [None] * 9
    self.current_player = Player.O
    self.game_log = []
    self.status = GameStatus.ONGOING
    self.turn = 1
    return BoardUpdateResult(
      success=True,
      status=self.status,
      message="Game reset successfully.",
      board_state=self.get_board(),
    )

  # Validation methods (grouped for future abstraction, e.g., into a Validator class)
  def _validate_position(self, position: int) -> bool:
    """Check if position is within bounds."""
    return 0 <= position <= 8

  def _validate_empty(self, position: int) -> bool:
    """Check if the spot is empty."""
    return self.board[position] is None

  def _validate_turn(self, player: Player) -> bool:
    """Check if it's the correct player's turn."""
    return player == self.current_player

  def make_move(self, player: Player, position: int) -> BoardUpdateResult:
    """
    Make a move for the given player at the position.
    Validates the move, updates the board, logs history, swaps player, checks status, and adds to messages.
    Returns structured result.
    """
    # Validation block (for future abstraction)
    if self.status != GameStatus.ONGOING:
      return BoardUpdateResult(
        success=False,
        status=self.status,
        message=f"Game is not ongoing. Current status: {self.status.value}",
        board_state=self.get_board(),
      )
    if not self._validate_turn(player):
      self.game_log.append(
        GameLogRecord(turn=self.turn, player=player, position=position, success=False)
      )
      return BoardUpdateResult(
        success=False,
        status=self.status,
        message=f"It's not {player.value}'s turn.",
        board_state=self.get_board(),
      )
    if not self._validate_position(position):
      self.game_log.append(
        GameLogRecord(turn=self.turn, player=player, position=position, success=False)
      )
      return BoardUpdateResult(
        success=False,
        status=self.status,
        message=f"Invalid position: {position} (must be 0-8).",
        board_state=self.get_board(),
      )
    if not self._validate_empty(position):
      self.game_log.append(
        GameLogRecord(turn=self.turn, player=player, position=position, success=False)
      )
      return BoardUpdateResult(
        success=False,
        status=self.status,
        message=f"Position {position} is not empty.",
        board_state=self.get_board(),
      )

    # Update board and history
    self.board[position] = player
    self.game_log.append(
      GameLogRecord(turn=self.turn, player=player, position=position, success=True)
    )
    self.turn += 1

    # Swap player
    self.current_player = Player.O if player == Player.X else Player.X

    # Get status and prepare message
    status, winner = self.get_game_status()
    if status == GameStatus.WIN:
      message = f"Player {winner.value if winner else 'unknown'} wins!"
    elif status == GameStatus.DRAW:
      message = "The game is a draw."
    else:
      message = f"Move successful. Now {self.current_player.value}'s turn."

    return BoardUpdateResult(
      success=True,
      status=status,
      message=message,
      board_state=self.get_board(),
    )

  def take_X_move(self, position: int) -> BoardUpdateResult:
    """Hardcoded method for making a move as X, calling make_move."""
    print(f"Taking X move at position: {position}")
    return self.make_move(Player.X, position)

  def take_O_move(self, position: int) -> BoardUpdateResult:
    """Hardcoded method for making a move as O, calling make_move."""
    print(f"Taking O move at position: {position}")
    return self.make_move(Player.O, position)

  # Win check strategies (grouped for future abstraction, e.g., into Strategy pattern if extending to other games)
  def _check_rows(self) -> Optional[Player]:
    """Check for a winner in rows."""
    for i in range(0, 9, 3):
      if self.board[i] == self.board[i + 1] == self.board[i + 2] and self.board[i] is not None:
        self.status = GameStatus.WIN
        return self.board[i]
    return None

  def _check_columns(self) -> Optional[Player]:
    """Check for a winner in columns."""
    for i in range(3):
      if self.board[i] == self.board[i + 3] == self.board[i + 6] and self.board[i] is not None:
        self.status = GameStatus.WIN
        return self.board[i]
    return None

  def _check_diagonals(self) -> Optional[Player]:
    """Check for a winner in diagonals."""
    if self.board[0] == self.board[4] == self.board[8] and self.board[0] is not None:
      self.status = GameStatus.WIN
      return self.board[0]
    if self.board[2] == self.board[4] == self.board[6] and self.board[2] is not None:
      self.status = GameStatus.WIN
      return self.board[2]
    return None

  def check_win(self) -> Optional[Player]:
    """Check if there's a winner using row, column, and diagonal strategies."""
    return self._check_rows() or self._check_columns() or self._check_diagonals()

  def check_draw(self) -> bool:
    """Check if the game is a draw (board full, no winner)."""
    if all(cell is not None for cell in self.board):
      self.status = GameStatus.DRAW
      return True
    return False

  def get_game_status(self) -> Tuple[GameStatus, Optional[Player]]:
    """
    Get the current game status.
    Returns (status, winner_value if win else None)
    """
    winner = self.check_win()
    if winner:
      return self.status, winner
    if self.check_draw():
      return self.status, None
    return self.status, None

  def get_board(self) -> List[Optional[Player]]:
    """Get a snapshot of the board (copy), with player values or None."""
    return self.board.copy()

  def get_board_string(self) -> str:
    """Get a string representation of the board for display with clean box-drawing borders."""
    lines = []

    upper_border = "┌───┬───┬───┐"
    center_border = "├───┼───┼───┤"
    lower_border = "└───┴───┴───┘"
    lines.append(upper_border)

    for row in range(3):
      row_cells = []
      for col in range(3):
        idx = row * 3 + col
        cell = self.board[idx]
        mark = cell.value if cell else " "
        row_cells.append(f" {mark} ")
      lines.append("│" + "│".join(row_cells) + "│")

      # Horizontal separator (except after last row)
      if row < 2:
        lines.append(center_border)

    # Bottom border
    lines.append(lower_border)
    return "\n".join(lines)

  def get_current_turn(self) -> str:
    """Get whose turn it is."""
    return self.current_player.value
