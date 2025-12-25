# src/main.py
"""Main entry point for the application."""

from fastapi import FastAPI
from socketio import ASGIApp, AsyncServer

from src.config import settings
from src.handlers import ButtonHandler, ConnectionHandler
from src.tic_tac_toe import TicTacToeManager

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
# Abstracted Event Handlers
# #########################################################
connection_handler = ConnectionHandler(sio)
button_handler = ButtonHandler(sio)


# #########################################################
# Example Events for Demo
# #########################################################
@sio.event
async def PING(sid: str, data: dict | None = None):
  print(f"PING event: {sid}")
  await sio.emit("PONG", {}, to=sid)


@sio.event
async def CONNECTION_TEST(sid: str, data: dict | None = None):
  print(f"CONNECTION_TEST received from client: {sid} with data: {data}")


# #########################################################
# Game Event Handler for Demo
# #########################################################
tic_tac_toe_manager = TicTacToeManager(sio)


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
