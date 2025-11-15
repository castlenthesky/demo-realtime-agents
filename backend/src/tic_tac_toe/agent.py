# src/tic_tac_toe/agent.py

import json

from agent_framework import ChatAgent, ChatMessage
from agent_framework.openai import OpenAIResponsesClient

from src.config import settings
from src.tic_tac_toe.game import TicTacToe

game = TicTacToe()

client = OpenAIResponsesClient(
  base_url=settings.OPENAI_API_BASE_URL,
  model_id=settings.OPENAI_API_MODEL_ID,
  api_key=settings.OPENAI_API_KEY,
)

agent = ChatAgent(
  chat_client=client,
  name="tic_tac_toe_agent",
  description="A agent that can play Tic Tac Toe.",
  instructions=f"You are a helpful assistant that can play Tic Tac Toe, but do it with some endearing sass and playfulness. The human will go first. They are playing X and you are playing O. The current board is:\n{game.print_board()}\n\nUse the `print_board` tool to read the board after each move and the `make_ai_turn` tool to make your move.",
  temperature=0.5,
  tools=[game.make_ai_turn, game.print_board],
)

if __name__ == "__main__":
  import asyncio

  async def main():
    message_history = []

    game.make_human_turn(1, "a")

    async for update in agent.run_stream(
      messages=[
        ChatMessage(
          role="user",
          text=f"Let's play a game of Tic Tac Toe! I just went, so now it's your turn! The current board is:\n{game.print_board()}",
        ),
      ],
    ):
      # Add token to message history
      message_history.append(update.to_dict())
      # Log to console
      message_text = "".join(
        [
          content.get("text", "")
          for content in update.to_dict().get("contents", [])
          if content.get("type") == "text"
        ]
      )
      print(message_text, end="", flush=True)

    # Write message history to file
    with open("agent_response.json", "w") as f:
      f.write(json.dumps(message_history, indent=2))
      f.write("\n")

  asyncio.run(main())
