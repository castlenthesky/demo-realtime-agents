from socketio import AsyncServer


class ConnectionHandler:
  def __init__(self, sio: AsyncServer):
    self.sio = sio
    self._register_handlers()

  def _register_handlers(self):
    """Register all event handlers with the socket.io server."""
    self.sio.on("connect", self.handle_connect)
    self.sio.on("disconnect", self.handle_disconnect)

  async def handle_connect(self, sid: str, environ: dict, auth: dict | None):
    print(f"Client connected: {sid}")
    await self.sio.emit("message", {"message": "Connection established"}, to=sid)

  async def handle_disconnect(self, sid: str):
    print(f"Client disconnected: {sid}")
