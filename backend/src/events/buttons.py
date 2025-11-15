import socketio


class ButtonHandler:
  def __init__(self, sio: socketio.AsyncServer):
    self.sio = sio
    self._register_handlers()

  def _register_handlers(self):
    """Register all event handlers with the socket.io server."""
    self.sio.on("BUTTON_PRESSED", self.handle_button_press)
    # Add more event registrations here as needed

  async def handle_button_press(self, sid: str, data: dict):
    """Handle button press events from clients."""
    print(f"Button pressed: {data['button']}")
    await self.sio.emit("message", {"message": f"Button pressed: {data['button']}"}, to=sid)
