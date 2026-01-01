from src.tic_tac_toe.game import TicTacToe
from src.tic_tac_toe.models import BoardUpdateResult, GameStatus, Player

# ==================== Initialization Tests ====================


def test_game_initialization():
  game = TicTacToe()
  assert game.board == [None] * 9
  assert game.current_player == Player.O
  assert game.game_log == []
  assert game.turn == 1


def test_starting_player():
  game = TicTacToe()
  assert game.current_player == Player.O


# ==================== Basic Move Tests ====================


def test_first_move():
  game = TicTacToe()
  result = game.make_move(Player.O, 0)
  assert result == BoardUpdateResult(
    success=True,
    status=GameStatus.ONGOING,
    message="Move successful. Now X's turn.",
    board_state=[Player.O, None, None, None, None, None, None, None, None],
  )
  assert game.current_player == Player.X
  assert game.turn == 2


def test_second_move():
  game = TicTacToe()
  game.make_move(Player.O, 0)
  result = game.make_move(Player.X, 1)
  assert result == BoardUpdateResult(
    success=True,
    status=GameStatus.ONGOING,
    message="Move successful. Now O's turn.",
    board_state=[Player.O, Player.X, None, None, None, None, None, None, None],
  )
  assert game.current_player == Player.O
  assert game.turn == 3


def test_player_alternation():
  """Test that players alternate correctly throughout the game."""
  game = TicTacToe()
  assert game.current_player == Player.O

  game.make_move(Player.O, 0)
  assert game.current_player == Player.X

  game.make_move(Player.X, 1)
  assert game.current_player == Player.O

  game.make_move(Player.O, 2)
  assert game.current_player == Player.X


def test_turn_counter_increments():
  """Test that turn counter increments correctly."""
  game = TicTacToe()
  assert game.turn == 1

  game.make_move(Player.O, 0)
  assert game.turn == 2

  game.make_move(Player.X, 1)
  assert game.turn == 3

  game.make_move(Player.O, 2)
  assert game.turn == 4


# ==================== Win Condition Tests ====================


def test_row_1_win():
  """Test win condition for top row (positions 0, 1, 2)."""
  game = TicTacToe()
  game.make_move(Player.O, 0)
  game.make_move(Player.X, 3)
  game.make_move(Player.O, 1)
  game.make_move(Player.X, 4)
  result = game.make_move(Player.O, 2)
  assert result == BoardUpdateResult(
    success=True,
    status=GameStatus.WIN,
    message="Player O wins!",
    board_state=[Player.O, Player.O, Player.O, Player.X, Player.X, None, None, None, None],
  )
  assert game.get_game_status()[0] == GameStatus.WIN
  assert game.check_win() == Player.O


def test_row_2_win():
  """Test win condition for middle row (positions 3, 4, 5)."""
  game = TicTacToe()
  game.make_move(Player.O, 3)
  game.make_move(Player.X, 0)
  game.make_move(Player.O, 4)
  game.make_move(Player.X, 1)
  result = game.make_move(Player.O, 5)
  assert result.status == GameStatus.WIN
  assert result.message == "Player O wins!"
  assert game.check_win() == Player.O


def test_row_3_win():
  """Test win condition for bottom row (positions 6, 7, 8)."""
  game = TicTacToe()
  game.make_move(Player.O, 6)
  game.make_move(Player.X, 0)
  game.make_move(Player.O, 7)
  game.make_move(Player.X, 1)
  result = game.make_move(Player.O, 8)
  assert result.status == GameStatus.WIN
  assert result.message == "Player O wins!"
  assert game.check_win() == Player.O


def test_column_1_win():
  """Test win condition for left column (positions 0, 3, 6)."""
  game = TicTacToe()
  game.make_move(Player.O, 0)
  game.make_move(Player.X, 1)
  game.make_move(Player.O, 3)
  game.make_move(Player.X, 2)
  result = game.make_move(Player.O, 6)
  assert result.status == GameStatus.WIN
  assert result.message == "Player O wins!"
  assert game.check_win() == Player.O


def test_column_2_win():
  """Test win condition for middle column (positions 1, 4, 7)."""
  game = TicTacToe()
  game.make_move(Player.O, 1)
  game.make_move(Player.X, 0)
  game.make_move(Player.O, 4)
  game.make_move(Player.X, 2)
  result = game.make_move(Player.O, 7)
  assert result.status == GameStatus.WIN
  assert result.message == "Player O wins!"
  assert game.check_win() == Player.O


def test_column_3_win():
  """Test win condition for right column (positions 2, 5, 8)."""
  game = TicTacToe()
  game.make_move(Player.O, 2)
  game.make_move(Player.X, 0)
  game.make_move(Player.O, 5)
  game.make_move(Player.X, 1)
  result = game.make_move(Player.O, 8)
  assert result.status == GameStatus.WIN
  assert result.message == "Player O wins!"
  assert game.check_win() == Player.O


def test_diagonal_top_left_to_bottom_right_win():
  """Test win condition for diagonal (positions 0, 4, 8)."""
  game = TicTacToe()
  game.make_move(Player.O, 0)
  game.make_move(Player.X, 1)
  game.make_move(Player.O, 4)
  game.make_move(Player.X, 2)
  result = game.make_move(Player.O, 8)
  assert result.status == GameStatus.WIN
  assert result.message == "Player O wins!"
  assert game.check_win() == Player.O


def test_diagonal_top_right_to_bottom_left_win():
  """Test win condition for diagonal (positions 2, 4, 6)."""
  game = TicTacToe()
  game.make_move(Player.O, 8)
  game.make_move(Player.X, 2)
  game.make_move(Player.O, 0)
  game.make_move(Player.X, 4)
  game.make_move(Player.O, 1)
  result = game.make_move(Player.X, 6)
  assert result.status == GameStatus.WIN
  assert result.message == "Player X wins!"
  assert game.check_win() == Player.X


def test_win_with_x_player():
  """Test that X can win the game."""
  game = TicTacToe()
  game.make_move(Player.O, 0)
  game.make_move(Player.X, 1)
  game.make_move(Player.O, 3)
  game.make_move(Player.X, 4)
  game.make_move(Player.O, 8)
  result = game.make_move(Player.X, 7)
  assert result.status == GameStatus.WIN
  assert result.message == "Player X wins!"
  assert game.check_win() == Player.X


# ==================== Tie Condition Tests ====================


def test_draw_full_board_no_winner():
  """Test that a full board with no winner results in a draw."""
  game = TicTacToe()
  # Create a draw scenario: O wins rows, X wins columns, but no complete line
  # ┌───┬───┬───┐
  # │ O │ X │   │
  # ├───┼───┼───┤
  # │ X │ O │   │
  # ├───┼───┼───┤
  # │   │   │ O │
  # └───┴───┴───┘
  game.make_move(Player.O, 0)
  game.make_move(Player.X, 1)
  game.make_move(Player.O, 2)
  game.make_move(Player.X, 4)
  game.make_move(Player.O, 3)
  game.make_move(Player.X, 6)
  game.make_move(Player.O, 5)
  game.make_move(Player.X, 8)
  result = game.make_move(Player.O, 7)

  assert result.status == GameStatus.DRAW
  assert result.message == "The game is a draw."
  assert game.check_draw() is True
  assert game.check_win() is None
  assert all(cell is not None for cell in game.board)


def test_draw_alternating_moves():
  """Test a different draw scenario with alternating pattern."""
  game = TicTacToe()
  # ┌───┬───┬───┐
  # │ O │ X │ O │
  # ├───┼───┼───┤
  # │ O │ X │ X │
  # ├───┼───┼───┤
  # │ X │ O │ O │
  # └───┴───┴───┘
  moves = [
    (Player.O, 0),
    (Player.X, 1),
    (Player.O, 2),
    (Player.X, 4),
    (Player.O, 3),
    (Player.X, 5),
    (Player.O, 7),
    (Player.X, 6),
    (Player.O, 8),
  ]

  for player, position in moves:
    result = game.make_move(player, position)

  assert result.status == GameStatus.DRAW
  assert game.check_draw() is True
  assert game.check_win() is None


# ==================== Invalid Move Tests ====================


def test_invalid_position_negative():
  """Test that negative positions are rejected."""
  game = TicTacToe()
  result = game.make_move(Player.O, -1)
  assert result.success is False
  assert result.status == GameStatus.ONGOING
  assert "Invalid position" in result.message
  assert game.board == [None] * 9
  assert game.current_player == Player.O  # Should not change


def test_invalid_position_too_large():
  """Test that positions > 8 are rejected."""
  game = TicTacToe()
  result = game.make_move(Player.O, 9)
  assert result.success is False
  assert result.status == GameStatus.ONGOING
  assert "Invalid position" in result.message
  assert game.board == [None] * 9
  assert game.current_player == Player.O  # Should not change


def test_invalid_position_out_of_bounds():
  """Test various out-of-bounds positions."""
  game = TicTacToe()
  for invalid_pos in [-10, -1, 9, 10, 100]:
    result = game.make_move(Player.O, invalid_pos)
    assert result.success is False
    assert "Invalid position" in result.message
    assert game.current_player == Player.O  # Should not change


def test_position_already_occupied():
  """Test that moves to occupied positions are rejected."""
  game = TicTacToe()
  game.make_move(Player.O, 0)
  result = game.make_move(Player.X, 0)  # Try to move to occupied position
  assert result.success is False
  assert result.status == GameStatus.ONGOING
  assert "not empty" in result.message
  assert game.board[0] == Player.O  # Should remain O
  assert game.current_player == Player.X  # Turn should not advance


def test_wrong_player_turn():
  """Test that wrong player cannot make a move."""
  game = TicTacToe()
  assert game.current_player == Player.O

  # X tries to move when it's O's turn
  result = game.make_move(Player.X, 0)
  assert result.success is False
  assert result.status == GameStatus.ONGOING
  assert "not X's turn" in result.message
  assert game.board[0] is None  # Move should not be made
  assert game.current_player == Player.O  # Should not change


def test_same_player_twice_in_row():
  """Test that same player cannot make two moves in a row."""
  game = TicTacToe()
  game.make_move(Player.O, 0)
  # O tries to move again
  result = game.make_move(Player.O, 1)
  assert result.success is False
  assert "not O's turn" in result.message
  assert game.board[1] is None
  assert game.current_player == Player.X  # Should be X's turn


# ==================== Game End State Tests ====================


def test_no_moves_after_win():
  """Test that moves cannot be made after a win."""
  game = TicTacToe()
  # Create a win for O
  game.make_move(Player.O, 0)
  game.make_move(Player.X, 3)
  game.make_move(Player.O, 1)
  game.make_move(Player.X, 4)
  win_result = game.make_move(Player.O, 2)
  assert win_result.status == GameStatus.WIN

  # Try to make a move after win
  result = game.make_move(Player.X, 5)
  assert result.success is False
  assert "Current status: win" in result.message  # Game state should prevent further moves
  assert game.get_game_status()[0] == GameStatus.WIN


def test_no_moves_after_draw():
  """Test that moves cannot be made after a draw."""
  game = TicTacToe()
  # ┌───┬───┬───┐
  # │ O │ X │ O │
  # ├───┼───┼───┤
  # │ O │ X │ X │
  # ├───┼───┼───┤
  # │ X │ O │ O │
  # └───┴───┴───┘
  moves = [
    (Player.O, 0),
    (Player.X, 1),
    (Player.O, 2),
    (Player.X, 4),
    (Player.O, 3),
    (Player.X, 5),
    (Player.O, 7),
    (Player.X, 6),
    (Player.O, 8),
  ]
  for player, position in moves:
    game.make_move(player, position)

  assert game.get_game_status()[0] == GameStatus.DRAW

  # Try to make a move after draw (should fail due to turn validation)
  result = game.make_move(Player.X, 0)  # Position already occupied anyway
  assert result.success is False
  assert game.get_game_status()[0] == GameStatus.DRAW


# ==================== Game Log Tests ====================


def test_game_log_records_successful_moves():
  """Test that successful moves are logged correctly."""
  game = TicTacToe()
  assert len(game.game_log) == 0

  game.make_move(Player.O, 0)
  assert len(game.game_log) == 1
  assert game.game_log[0].turn == 1
  assert game.game_log[0].player == Player.O
  assert game.game_log[0].position == 0
  assert game.game_log[0].success is True

  game.make_move(Player.X, 1)
  assert len(game.game_log) == 2
  assert game.game_log[1].turn == 2
  assert game.game_log[1].player == Player.X
  assert game.game_log[1].position == 1
  assert game.game_log[1].success is True


def test_game_log_records_failed_moves():
  """Test that failed moves are also logged."""
  game = TicTacToe()
  assert len(game.game_log) == 0

  # Invalid move
  game.make_move(Player.O, -1)
  assert len(game.game_log) == 1
  assert game.game_log[0].success is False
  assert game.game_log[0].player == Player.O
  assert game.game_log[0].position == -1

  # Wrong player
  game.make_move(Player.X, 0)  # Should fail, it's O's turn
  assert len(game.game_log) == 2
  assert game.game_log[1].success is False


# ==================== Reset Tests ====================


def test_reset_game():
  """Test that reset returns game to initial state."""
  game = TicTacToe()
  game.make_move(Player.O, 0)
  game.make_move(Player.X, 1)
  game.make_move(Player.O, 2)

  result = game.reset()
  assert result.success is True
  assert result.status == GameStatus.ONGOING
  assert game.board == [None] * 9
  assert game.current_player == Player.O
  assert game.game_log == []
  assert game.turn == 1


def test_reset_after_win():
  """Test that reset works after a win."""
  game = TicTacToe()
  # Create a win
  game.make_move(Player.O, 0)
  game.make_move(Player.X, 3)
  game.make_move(Player.O, 1)
  game.make_move(Player.X, 4)
  game.make_move(Player.O, 2)
  assert game.get_game_status()[0] == GameStatus.WIN

  game.reset()
  assert game.get_game_status()[0] == GameStatus.ONGOING
  assert game.check_win() is None
  assert game.check_draw() is False


def test_reset_after_draw():
  """Test that reset works after a draw."""
  game = TicTacToe()
  # ┌───┬───┬───┐
  # │ O │ X │ O │
  # ├───┼───┼───┤
  # │ O │ X │ X │
  # ├───┼───┼───┤
  # │ X │ O │ O │
  # └───┴───┴───┘
  # Create a draw
  moves = [
    (Player.O, 0),
    (Player.X, 1),
    (Player.O, 2),
    (Player.X, 4),
    (Player.O, 3),
    (Player.X, 5),
    (Player.O, 7),
    (Player.X, 6),
    (Player.O, 8),
  ]
  for player, position in moves:
    game.make_move(player, position)
  assert game.get_game_status()[0] == GameStatus.DRAW

  game.reset()
  assert game.get_game_status()[0] == GameStatus.ONGOING
  assert game.check_win() is None
  assert game.check_draw() is False


# ==================== State Validation Tests ====================


def test_board_state_consistency():
  """Test that board state remains consistent after moves."""
  game = TicTacToe()
  game.make_move(Player.O, 0)
  game.make_move(Player.X, 4)
  game.make_move(Player.O, 8)

  board_copy = game.get_board()
  assert board_copy[0] == Player.O
  assert board_copy[4] == Player.X
  assert board_copy[8] == Player.O
  assert board_copy[1] is None

  # Verify it's a copy, not a reference
  board_copy[0] = Player.X
  assert game.board[0] == Player.O  # Original should be unchanged


def test_game_status_ongoing_during_play():
  """Test that game status is ONGOING during normal play."""
  game = TicTacToe()
  assert game.get_game_status()[0] == GameStatus.ONGOING

  game.make_move(Player.O, 0)
  assert game.get_game_status()[0] == GameStatus.ONGOING

  game.make_move(Player.X, 1)
  assert game.get_game_status()[0] == GameStatus.ONGOING

  game.make_move(Player.O, 2)
  assert game.get_game_status()[0] == GameStatus.ONGOING


def test_win_detection_immediate():
  """Test that win is detected immediately when it occurs."""
  game = TicTacToe()
  game.make_move(Player.O, 0)
  game.make_move(Player.X, 3)
  game.make_move(Player.O, 1)
  game.make_move(Player.X, 4)

  # Before winning move
  assert game.get_game_status()[0] == GameStatus.ONGOING
  assert game.check_win() is None

  # Winning move
  game.make_move(Player.O, 2)
  assert game.get_game_status()[0] == GameStatus.WIN
  assert game.check_win() == Player.O


def test_draw_detection_immediate():
  """Test that draw is detected immediately when board is full."""
  game = TicTacToe()
  # Fill board without a winner
  # ┌───┬───┬───┐
  # │ O │ X │ O │
  # ├───┼───┼───┤
  # │ O │ X │ X │
  # ├───┼───┼───┤
  # │ X │ O │ O │
  # └───┴───┴───┘
  moves = [
    (Player.O, 0),
    (Player.X, 1),
    (Player.O, 2),
    (Player.X, 4),
    (Player.O, 3),
    (Player.X, 5),
    (Player.O, 7),
    (Player.X, 6),
  ]
  for player, position in moves:
    game.make_move(player, position)
    assert game.get_game_status()[0] == GameStatus.ONGOING

  # Final move that creates draw
  result = game.make_move(Player.O, 8)
  assert result.status == GameStatus.DRAW
  assert game.get_game_status()[0] == GameStatus.DRAW
  assert game.check_draw() is True
