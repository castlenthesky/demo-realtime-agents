# backend/src/tic_tac_toe/game.py
from typing import Any, Dict, List, Optional, Tuple

from src.tic_tac_toe.models import GameStatus, Player


class TicTacToe:
  """
  A class to manage a Tic-Tac-Toe game, tracking state, moves, wins, and providing structured responses.
  The board is a flat list of 9 elements (0-8), with None for empty spots.
  Includes a messages list for game commentary, aligned with chat features but self-contained without external dependencies.
  """

  def __init__(self):
    self.board: List[Optional[Player]] = [None] * 9
    self.current_player: Player = Player.X
    self.move_history: List[
      Dict[str, Any]
    ] = []  # List of {'turn': int, 'player': Player, 'position': int}
    self.turn: int = 1  # Starts at 1 for the first move
    self.messages: List[str] = []  # List of game messages/commentary

  def reset(self) -> Dict[str, Any]:
    """Reset the game to initial state, clearing messages as well."""
    self.board = [None] * 9
    self.current_player = Player.O
    self.move_history = []
    self.turn = 1
    self.messages = []
    return {
      "success": True,
      "status": GameStatus.ONGOING.value,
      "message": "Game reset successfully.",
      "board_state": self.get_board(),
    }

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

  def make_move(self, player: Player, position: int) -> Dict[str, Any]:
    """
    Make a move for the given player at the position.
    Validates the move, updates the board, logs history, swaps player, checks status, and adds to messages.
    Returns structured result.
    """
    # Validation block (for future abstraction)
    if not self._validate_position(position):
      return {
        "success": False,
        "status": GameStatus.ONGOING.value,
        "message": f"Invalid position: {position} (must be 0-8).",
        "board_state": self.get_board(),
      }
    if not self._validate_empty(position):
      return {
        "success": False,
        "status": GameStatus.ONGOING.value,
        "message": f"Position {position} is already taken.",
        "board_state": self.get_board(),
      }
    if not self._validate_turn(player):
      return {
        "success": False,
        "status": GameStatus.ONGOING.value,
        "message": f"It's not {player.value}'s turn.",
        "board_state": self.get_board(),
      }

    # Update board and history
    self.board[position] = player
    self.move_history.append({"turn": self.turn, "player": player.value, "position": position})
    self.turn += 1

    # Swap player
    self.current_player = Player.O if player == Player.X else Player.X

    # Get status and prepare message
    status, winner = self.get_game_status()
    if status == GameStatus.WIN:
      message = f"Player {winner} wins!"
    elif status == GameStatus.DRAW:
      message = "The game is a draw."
    else:
      message = f"Move successful. Now {self.current_player.value}'s turn."

    # Add to messages (self-contained commentary)
    self.messages.append(message)

    return {
      "success": True,
      "status": status.value,
      "message": message,
      "board_state": self.get_board(),
    }

  def take_X_move(self, position: int) -> Dict[str, Any]:
    """Hardcoded method for AI to make a move as X, calling make_move."""
    print(f"Taking X move at position: {position}")
    return self.make_move(Player.X, position)

  def take_O_move(self, position: int) -> Dict[str, Any]:
    """Hardcoded method for human or other to make a move as O, calling make_move."""
    print(f"Taking O move at position: {position}")
    return self.make_move(Player.O, position)

  # Win check strategies (grouped for future abstraction, e.g., into Strategy pattern if extending to other games)
  def _check_rows(self) -> Optional[Player]:
    """Check for a winner in rows."""
    for i in range(0, 9, 3):
      if self.board[i] == self.board[i + 1] == self.board[i + 2] and self.board[i] is not None:
        return self.board[i]
    return None

  def _check_columns(self) -> Optional[Player]:
    """Check for a winner in columns."""
    for i in range(3):
      if self.board[i] == self.board[i + 3] == self.board[i + 6] and self.board[i] is not None:
        return self.board[i]
    return None

  def _check_diagonals(self) -> Optional[Player]:
    """Check for a winner in diagonals."""
    if self.board[0] == self.board[4] == self.board[8] and self.board[0] is not None:
      return self.board[0]
    if self.board[2] == self.board[4] == self.board[6] and self.board[2] is not None:
      return self.board[2]
    return None

  def check_win(self) -> Optional[Player]:
    """Check if there's a winner using row, column, and diagonal strategies."""
    return self._check_rows() or self._check_columns() or self._check_diagonals()

  def check_draw(self) -> bool:
    """Check if the game is a draw (board full, no winner)."""
    return all(cell is not None for cell in self.board)

  def get_game_status(self) -> Tuple[GameStatus, Optional[str]]:
    """
    Get the current game status.
    Returns (status, winner_value if win else None)
    """
    winner = self.check_win()
    if winner:
      return GameStatus.WIN, winner.value
    if self.check_draw():
      return GameStatus.DRAW, None
    return GameStatus.ONGOING, None

  def get_board(self) -> List[Optional[str]]:
    """Get a snapshot of the board (copy), with player values or None."""
    return [cell.value if cell else None for cell in self.board.copy()]

  def get_board_string(self) -> str:
    """Get a string representation of the board for display."""
    board_str = ""
    for i in range(9):
      cell = self.board[i]
      current_mark = cell.value if cell else " "
      board_str += f" {current_mark} "
      if (i + 1) % 3 == 0:
        board_str += "\n-----------\n" if i < 8 else ""
      else:
        board_str += "|"
    return board_str

  def get_current_turn(self) -> str:
    """Get whose turn it is."""
    return self.current_player.value

  def get_messages(self) -> List[str]:
    """Get the list of game messages/commentary."""
    return self.messages.copy()

  # Position mapping utilities (grouped for future abstraction, e.g., into a Mapper class for different input formats)
  @staticmethod
  def pos_to_index(pos_str: str) -> int:
    """
    Convert grid position like 'A1' to flat index (0-8).
    Rows: A=0, B=1, C=2; Columns: 1=0, 2=1, 3=2 (assuming 1-3 for columns).
    """
    if len(pos_str) != 2:
      raise ValueError("Invalid position format. Use e.g., 'A1'.")
    row_char, col_char = pos_str.upper()
    row = ord(row_char) - ord("A")
    col = int(col_char) - 1  # Assuming columns are 1-3
    if not (0 <= row <= 2 and 0 <= col <= 2):
      raise ValueError("Position out of bounds.")
    return row * 3 + col

  @staticmethod
  def index_to_pos(index: int) -> str:
    """Convert flat index (0-8) to grid position like 'A1'."""
    if not 0 <= index <= 8:
      raise ValueError("Index out of bounds.")
    row = index // 3
    col = index % 3
    row_char = chr(ord("A") + row)
    col_char = str(col + 1)  # 0->1, 1->2, 2->3
    return row_char + col_char
