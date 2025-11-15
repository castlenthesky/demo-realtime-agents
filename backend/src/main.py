from fastapi import FastAPI
from socketio import ASGIApp, AsyncServer

from src.config import settings
from src.events.buttons import ButtonHandler

app = FastAPI(title="Realtime Demo")

sio = AsyncServer(
  async_mode="asgi",
  cors_allowed_origins=["*"],
)

sio_app = ASGIApp(
  socketio_server=sio,
  other_asgi_app=app,
  socketio_path="/socket.io/",
)


# #########################################################
# Socket.IO Connection Events
# #########################################################
@sio.event
async def connect(sid: str, environ: dict, auth: dict | None):
  print(f"Client connected: {sid}")
  await sio.emit("message", {"message": "Welcome to the server"}, to=sid)


@sio.event
async def disconnect(sid: str):
  print(f"Client disconnected: {sid}")


# #########################################################
# Socket.IO Example Event
# #########################################################
@sio.event
async def PING(sid: str, data: dict | None = None):
  print(f"PING event: {sid}")
  await sio.emit("PONG", {}, to=sid)


# #########################################################
# Abstracted Event Handlers
# #########################################################
button_handler = ButtonHandler(sio)


if __name__ == "__main__":
  import uvicorn

  # Hot-reload is enabled by default, disabled only in production
  hot_reload = not settings.is_production

  print(f"Starting API server: {app.title}")
  print(f"  Environment: {settings.ENVIRONMENT}")
  print(f"  Hot-reload: {hot_reload}")

  uvicorn.run(
    "src.main:sio_app",
    host="0.0.0.0",
    port=settings.API_PORT,
    reload=hot_reload,
    reload_dirs=["src"],
    reload_excludes=["__pycache__", "*.pyc", "*.pyo", "*.pyd", "*.pyw", "*.pyz"],
  )
