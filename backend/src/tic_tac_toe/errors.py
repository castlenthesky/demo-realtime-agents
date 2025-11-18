# src/tic_tac_toe/errors.py
"""Errors for the tic-tac-toe game."""


class GameErrorBase(Exception):
  """Base exception for game errors."""

  pass


class InvalidPlayerError(GameErrorBase):
  """Exception raised for invalid player."""

  pass


class InvalidMoveError(GameErrorBase):
  """Exception raised for invalid move."""

  pass


class GameInvalidStateError(GameErrorBase):
  """Exception raised for game in an invalid state. eg. incorrect number of player tokens on the board."""

  pass


class AgentErrorBase(Exception):
  """Base exception for agent errors."""

  pass


class AgentTimeoutError(AgentErrorBase):
  """Exception raised for agent timeout."""

  pass
