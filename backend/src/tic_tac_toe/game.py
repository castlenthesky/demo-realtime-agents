# src/tic_tac_toe/game.py
from enum import Enum

from socketio import AsyncServer


class Column(Enum):
  """Column identifiers for the tic-tac-toe board."""

  A = "a"
  B = "b"
  C = "c"


class TicTacToe:
  def __init__(self, sio: AsyncServer | None = None, sid: str | None = None):
    self.sio = sio
    self.sid = sid
    self.board = [[" " for _ in range(3)] for _ in range(3)]
    self.human_player = "X"
    self.ai_player = "O"
    self.winner = None
    self.game_over = False

  async def emit_board(self):
    if self.sio:
      await self.sio.emit("BOARD", {"board": self.board}, to=self.sid)

  async def emit_human_move_made(self, row: int, col: Column):
    if self.sio:
      await self.sio.emit("HUMAN_MOVE_MADE", {"row": row, "col": col}, to=self.sid)

  async def emit_ai_move_made(self, row: int, col: Column):
    if self.sio:
      await self.sio.emit("AI_MOVE_MADE", {"row": row, "col": col}, to=self.sid)

  async def emit_game_over(self, result: str):
    if self.sio:
      await self.sio.emit("GAME_OVER", {"result": result}, to=self.sid)

  def print_board(self):
    """Print the board with a visually appealing format."""
    print("\n   a   b   c")
    print("  ┌───┬───┬───┐")
    for i, row in enumerate(self.board):
      # Format cells: show number if empty, or X/O if occupied
      cells = []
      for cell in row:
        if cell == " ":
          cells.append(" ")
        else:
          cells.append(cell)
      row_num = i + 1  # Display 1-3 instead of 0-2
      print(f"{row_num} │ {cells[0]} │ {cells[1]} │ {cells[2]} │")
      if i < 2:
        print("  ├───┼───┼───┤")
    print("  └───┴───┴───┘\n")

  def _col_to_index(self, col):
    """Convert column letter (a, b, c) or Column enum to internal index (0, 1, 2)."""
    # Handle Enum
    if isinstance(col, Column):
      col = col.value
    # Handle string
    if isinstance(col, str):
      col = col.lower()
      if col == "a":
        return 0
      elif col == "b":
        return 1
      elif col == "c":
        return 2
    return None

  def _index_to_col(self, index):
    """Convert internal column index (0, 1, 2) to letter (a, b, c)."""
    return ["a", "b", "c"][index]

  def _row_to_index(self, row):
    """Convert row number (1, 2, 3) to internal index (0, 1, 2)."""
    if isinstance(row, int):
      if 1 <= row <= 3:
        return row - 1
    return None

  def _index_to_row(self, index):
    """Convert internal row index (0, 1, 2) to row number (1, 2, 3)."""
    return index + 1

  def make_human_turn(self, row, col):
    """Make human's move. row: 1-3, col: 'a', 'b', or 'c'."""
    # Convert user coordinates to internal indices
    row_idx = self._row_to_index(row)
    col_idx = self._col_to_index(col)

    if row_idx is None or col_idx is None:
      return False
    if self.board[row_idx][col_idx] != " ":
      return False
    self.board[row_idx][col_idx] = self.human_player
    self._update_game_state()
    return True

  def make_ai_turn(self, row: int, col: Column) -> bool:
    """
    Make AI's move. row: 1-3, col: Column enum (a, b, or c).
    Args:
      row: int - Row number (1-3)
      col: Column - Column enum (Column.A, Column.B, or Column.C)
    Returns:
      bool: True if the move was made, False otherwise
    Raises:
      ValueError: If the row or col is not a valid input
    """
    if not isinstance(row, int):
      raise ValueError("row must be an int")
    if not isinstance(col, Column):
      raise ValueError("col must be a Column enum")
    if row < 1 or row > 3:
      raise ValueError("row must be between 1 and 3")
    # Convert user coordinates to internal indices
    row_idx = self._row_to_index(row)
    col_idx = self._col_to_index(col)

    if row_idx is None or col_idx is None:
      return False
    if self.board[row_idx][col_idx] != " ":
      return False
    self.board[row_idx][col_idx] = self.ai_player
    self._update_game_state()
    return True

  def choose_ai_move(self):
    """Calculate and return the AI's move as (row, col) tuple in user coordinates (1-3, Column enum)."""
    # Try to win
    move = self._find_winning_move(self.ai_player)
    if move:
      row_idx, col_idx = move
      col_str = self._index_to_col(col_idx)
      col_enum = Column[col_str.upper()]  # Convert "a" -> Column.A
      return (self._index_to_row(row_idx), col_enum)

    # Try to block human from winning
    move = self._find_winning_move(self.human_player)
    if move:
      row_idx, col_idx = move
      col_str = self._index_to_col(col_idx)
      col_enum = Column[col_str.upper()]  # Convert "a" -> Column.A
      return (self._index_to_row(row_idx), col_enum)

    # Take first available spot
    for row_idx in range(3):
      for col_idx in range(3):
        if self.board[row_idx][col_idx] == " ":
          col_str = self._index_to_col(col_idx)
          col_enum = Column[col_str.upper()]  # Convert "a" -> Column.A
          return (self._index_to_row(row_idx), col_enum)
    return None

  def _find_winning_move(self, player):
    """Find a winning move for the given player, or None if none exists."""
    for row in range(3):
      for col in range(3):
        if self.board[row][col] == " ":
          # Try this move
          self.board[row][col] = player
          winner = self._check_winner()
          # Undo the move
          self.board[row][col] = " "
          if winner == player:
            return (row, col)
    return None

  def _check_winner(self):
    """Check for a winner and return the winning player, or None."""
    # Check rows
    for row in range(3):
      if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
        return self.board[row][0]

    # Check columns
    for col in range(3):
      if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
        return self.board[0][col]

    # Check diagonal top-left to bottom-right
    if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
      return self.board[0][0]

    # Check diagonal top-right to bottom-left
    if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
      return self.board[0][2]

    return None

  def check_game_over(self):
    """Check if game is over (has winner or board is full)."""
    return self._check_winner() is not None or self.is_board_full()

  def is_game_over(self):
    return self.game_over

  def is_board_full(self):
    return all(cell != " " for row in self.board for cell in row)

  def _update_game_state(self):
    """Update game state flags after a move."""
    winner = self._check_winner()
    if winner:
      self.winner = winner
      self.game_over = True
    elif self.is_board_full():
      self.winner = None
      self.game_over = True
    else:
      self.game_over = False

  def get_winner(self):
    return self.winner

  def get_current_player(self):
    """Return the player who should move next (X goes first)."""
    human_count = sum(row.count(self.human_player) for row in self.board)
    ai_count = sum(row.count(self.ai_player) for row in self.board)
    # X goes first, so if counts are equal, it's X's turn
    # If X has fewer moves, it's X's turn
    if human_count <= ai_count:
      return self.human_player
    else:
      return self.ai_player


if __name__ == "__main__":
  game = TicTacToe()
  game.print_board()
  while not game.is_game_over():
    if game.get_current_player() == game.human_player:
      while True:
        try:
          row_input = input("Enter row (1-3): ").strip()
          while True:
            col_input = input("Enter col (a-c): ").strip().lower()
            if col_input in ["a", "b", "c"]:
              break
            else:
              print("Invalid input! Please enter a, b, or c.")
          row = int(row_input)
          if game.make_human_turn(row, col_input):
            break
          else:
            print("Invalid move! That spot is taken or out of bounds. Try again.")
        except ValueError:
          print("Invalid input! Please enter row as 1-3 and col as a, b, or c.")
        except (KeyboardInterrupt, EOFError):
          print("\nGame cancelled.")
          exit()
    else:
      print("AI's turn...")
      move = game.choose_ai_move()
      if move:
        row, col = move
        game.make_ai_turn(row, col)
      else:
        print("No valid moves available!")
        break
    game.print_board()

  # Display game result
  winner = game.get_winner()
  if winner:
    print(f"Game over! Winner: {winner}")
  else:
    print("Game over! It's a tie!")
