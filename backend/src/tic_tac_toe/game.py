# src/tic_tac_toe/game.py
import uuid
from enum import Enum

import src.tic_tac_toe.errors as errors


class Column(Enum):
  """Column identifiers for the tic-tac-toe board."""

  A = "a"
  B = "b"
  C = "c"


class TicTacToe:
  def __init__(self):
    self.game_id = uuid.uuid4()
    self.board = [[" " for _ in range(3)] for _ in range(3)]
    self.ai_player: str = "X"
    self.human_player: str = "O"
    self.round_number: int = 1
    self.is_human_turn: bool = True
    self.is_current_player_turn_completed: bool = False
    self.is_game_over: bool = False
    self.winner: str | None = None
    self.game_over_reason: str | None = None

  def reset(self):
    self.board = [[" " for _ in range(3)] for _ in range(3)]
    self.round_number = 1
    self.is_human_turn = True
    self.is_current_player_turn_completed = False
    self.is_game_over = False
    self.winner = None
    self.game_over_reason = None

  def get_board_state(self) -> str:
    board_state = (
      "    a   b   c\n"
      + "  ┌───┬───┬───┐\n"
      + f"1 │ {self.board[0][0]} │ {self.board[0][1]} │ {self.board[0][2]} │\n"
      + "  ├───┼───┼───┤\n"
      + f"2 │ {self.board[1][0]} │ {self.board[1][1]} │ {self.board[1][2]} │\n"
      + "  ├───┼───┼───┤\n"
      + f"3 │ {self.board[2][0]} │ {self.board[2][1]} │ {self.board[2][2]} │\n"
      + "  └───┴───┴───┘\n"
      + f"Round {self.round_number}\n"
      + f"Current player: {'Human' if self.is_human_turn else 'AI'}\n"
      + f"Current player turn completed: {'Yes' if self.is_current_player_turn_completed else 'No'}\n"
      + f"Winner: {'Human' if self.winner == self.human_player else 'AI' if self.winner == self.ai_player else 'None'}\n"
      + f"Game over: {'Yes' if self.is_game_over else 'No'}\n"
      + f"{'Game over reason: ' + self.game_over_reason + '\n ' if self.game_over_reason else ''}"
    )
    print(board_state)
    return board_state

  def _is_player_move_valid(self, player: str, row: int, col: Column) -> bool:
    """Private method to validate a player move."""
    # Check if it is the player's turn
    if self.is_human_turn != (player == self.human_player):
      raise errors.GameInvalidStateError(f"It is not {player}'s turn!")
    # Check if the player identifier is valid
    if player not in [self.human_player, self.ai_player]:
      raise errors.InvalidPlayerError(f"Player must be {self.human_player} or {self.ai_player}")
    # Check if the current player has already moved
    if self.is_current_player_turn_completed:
      raise errors.GameInvalidStateError(f"{player} has already moved this turn!")
    # Check if the game is already over
    if self.winner or self.is_game_over:
      raise errors.GameInvalidStateError("Game is already over")
    # Check if the row is valid
    if row > 3 or row < 1:
      raise errors.InvalidMoveError(f"Invalid row: {row}")
    # Check if the column is valid
    if col not in Column:
      raise errors.InvalidMoveError(f"Invalid column: {col}")
    # Check if the spot is already taken
    if self.board[row - 1][list(Column).index(col)] != " ":
      raise errors.InvalidMoveError(f"Row {row}, column {col.value} is already taken")
    # If all checks pass, return True to indicate the move is valid
    return True

  def _make_player_move(self, player: str, row: int, col: Column) -> bool:
    """Private method to make a move for the players."""
    try:
      if self._is_player_move_valid(player, row, col):
        # Update the board with the player's move
        print(
          f"Updating board at row {row - 1}, column {list(Column).index(Column(col))} with player {player}"
        )
        self.board[row - 1][list(Column).index(col)] = player
        # Lock state to prevent further moves for this player's turn
        self.is_current_player_turn_completed = True
        # Check for win state
        is_game_over = self._check_for_game_over()
        if is_game_over:
          return True
        # Increment the round number
        self.round_number += 1
        # Switch the current player
        self.is_human_turn = not self.is_human_turn
        # Initialize the next player's turn
        self.is_current_player_turn_completed = False
        return True
    except Exception as e:
      print(f"Error making player move: {e}")
      return False
    return False

  def make_ai_move(self, row: int, col: Column) -> bool:
    """Make a move for the AI player."""
    return self._make_player_move(self.ai_player, row, col)

  def make_human_move(self, row: int, col: Column) -> bool:
    """Make a move for the human player."""
    return self._make_player_move(self.human_player, row, col)

  def _check_winner_rows(self) -> bool:
    """Private method to check for a winner in any row."""
    for row in self.board:
      if row.count(self.ai_player) == 3:
        self.is_game_over = True
        self.winner = self.ai_player
        self.game_over_reason = "AI wins"
        print(f"AI wins by row: {row}")
        print(self.get_board_state())
        return True
      if row.count(self.human_player) == 3:
        self.is_game_over = True
        self.winner = self.human_player
        self.game_over_reason = "Human wins"
        print(f"Human wins by row: {row}")
        print(self.get_board_state())
        return True
    return False

  def _check_winner_columns(self) -> bool:
    """Private method to check for a winner in any column."""
    for col in range(3):
      if [self.board[row][col] for row in range(3)].count(self.ai_player) == 3:
        self.is_game_over = True
        self.winner = self.ai_player
        self.game_over_reason = "AI wins"
        print(f"AI wins by column: {col}")
        print(self.get_board_state())
        return True
      if [self.board[row][col] for row in range(3)].count(self.human_player) == 3:
        self.is_game_over = True
        self.winner = self.human_player
        self.game_over_reason = "Human wins"
        print(f"Human wins by column: {col}")
        print(self.get_board_state())
        return True
    return False

  def _check_winner_diagonals(self) -> bool:
    """Private method to check for a winner on the diagonal."""
    if [self.board[i][i] for i in range(3)].count(self.ai_player) == 3:
      self.is_game_over = True
      self.winner = self.ai_player
      self.game_over_reason = "AI wins"
      print(f"AI wins by diagonal: {[self.board[i][i] for i in range(3)]}")
      print(self.get_board_state())
      return True
    if [self.board[i][i] for i in range(3)].count(self.human_player) == 3:
      self.is_game_over = True
      self.winner = self.human_player
      self.game_over_reason = "Human wins"
      print(f"Human wins by diagonal: {[self.board[i][i] for i in range(3)]}")
      print(self.get_board_state())
      return True
    return False

  def _check_winner_anti_diagonals(self) -> bool:
    """Private method to check for a winner on the anti-diagonal."""
    if [self.board[i][2 - i] for i in range(3)].count(self.ai_player) == 3:
      self.is_game_over = True
      self.winner = self.ai_player
      self.game_over_reason = "AI wins"
      print(f"AI wins by anti-diagonal: {[self.board[i][2 - i] for i in range(3)]}")
      print(self.get_board_state())
      return True
    if [self.board[i][2 - i] for i in range(3)].count(self.human_player) == 3:
      self.is_game_over = True
      self.winner = self.human_player
      self.game_over_reason = "Human wins"
      print(f"Human wins by anti-diagonal: {[self.board[i][2 - i] for i in range(3)]}")
      print(self.get_board_state())
      return True
    return False

  def _check_tie(self) -> bool:
    """Private method to check for a tie."""
    if not any(" " in row for row in self.board):
      self.is_game_over = True
      self.winner = "Tie"
      self.game_over_reason = "Tie"
      print("Game is a tie")
      print(self.get_board_state())
      return True
    return False

  def _check_for_game_over(self) -> bool:
    """Private method to check for game over."""
    # 1. Check for three in a row, column, or diagonal
    #   a. Check for three in any row
    if self._check_winner_rows():
      return True
    #   b. Check for three in any column
    if self._check_winner_columns():
      return True
    #   c. Check for three top-left-to-bottom-right diagonal
    if self._check_winner_diagonals():
      return True
    #   d. Check for three top-right-to-bottom-left diagonal
    if self._check_winner_anti_diagonals():
      return True
    # 2. Check if the board is completely filled
    if self._check_tie():
      return True
    # If no winner, the game is not over
    return False
