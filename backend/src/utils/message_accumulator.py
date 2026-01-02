from agent_framework import ChatMessage


async def handle_update_message(update: ChatMessage):
  """Handle an update message - accumulating messages and yeilding them when the message is complete."""
  raise NotImplementedError("Not implemented")

  # Accumulation and emission logic here
  current_message = None
  yield current_message
