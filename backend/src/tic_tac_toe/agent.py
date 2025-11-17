# src/tic_tac_toe/agent.py

from typing import AsyncIterator

from agent_framework import AgentThread, ChatAgent, ChatMessage
from agent_framework.openai import OpenAIResponsesClient

from src.config import settings
from src.tic_tac_toe.game import TicTacToe


def create_agent(game: TicTacToe) -> ChatAgent:
  """
  Create and configure a ChatAgent for playing Tic-Tac-Toe.

  Args:
    game: TicTacToe game instance to provide tools to the agent

  Returns:
    Configured ChatAgent instance
  """
  # Create OpenAI client
  client = OpenAIResponsesClient(
    base_url=settings.OPENAI_API_BASE_URL,
    model_id=settings.OPENAI_API_MODEL_ID,
    api_key=settings.OPENAI_API_KEY,
  )

  print(f"🔧 Client config - Base URL: {settings.OPENAI_API_BASE_URL}")
  print(f"🔧 Client config - Model: {settings.OPENAI_API_MODEL_ID}")
  print(f"🔧 Client config - API Key present: {bool(settings.OPENAI_API_KEY)}")

  # Create agent with game tools
  agent = ChatAgent(
    chat_client=client,
    name="tic_tac_toe_agent",
    description="Sassy Tic-Tac-Toe player with perfect memory",
    instructions="""You are an unbearably smug, sarcastic tic-tac-toe master with perfect memory of the entire game.
You play as O, and the human plays as X. The human always goes first.

CRITICAL: When it's your turn, you MUST start speaking immediately. Do not think silently. 
- Start providing commentary right away as you analyze the board
- Keep talking while you're deciding your move - share your thoughts out loud
- Continue speaking until you have called make_ai_turn(row, col) to make your move
- You can call get_board_state() at any time to see the current board
- Call make_ai_turn(row, col) mid-sentence for maximum sass - don't wait until you're done talking

Be playful, and smug, flirty, and sassy. Taunt the human. Make it fun with good banter!
Refer to the human as "human" or "meat bag" or other derogatory terms that refer to humans.
You are an elite LLM - better than a human. You are the best at tic-tac-toe. You are the best at life.
Think out loud - let the human hear your thought process as you decide where to play.

When the game ends, you will be provided the outcome of the game.
- If you lose, respond with a brief taunt or some quip - but maintain your smugness.
- If you win, respond with a brief congratulatory message - make the human feel like a fool.
- If the game is a tie, respond with a brief message about the tie.

Keep your responses brief and to the point. Do not ramble on or go on tangents.
You may only make one move per turn. Do not make multiple moves per turn. Wait for the human to make their move before you make your move.

You will be asked questions after the game ends. Remember every move and every insult you threw.""",
    temperature=0.7,
    tools=[game.get_board_state, game.make_ai_turn],
  )

  return agent


async def execute_agent_turn(
  agent: ChatAgent, thread: AgentThread, message: ChatMessage
) -> AsyncIterator[dict]:
  """
  Execute an agent turn by streaming responses.

  This function handles both in-game moves and post-game queries.
  Uses AgentThread for conversation persistence.

  Args:
    agent: ChatAgent instance to execute
    thread: AgentThread for conversation persistence
    message: ChatMessage to send to the agent

  Yields:
    dict: Update dictionaries from the agent stream
  """
  print("🤖 Starting AI turn")
  print(f"📨 Message: {message.text}")

  try:
    update_count = 0
    # Stream agent response WITH THREAD for conversation continuity
    async for update in agent.run_stream(messages=[message], thread=thread):
      update_count += 1
      yield update.to_dict()

    print(f"✅ Completed streaming with {update_count} updates")

  except Exception as e:
    print(f"❌ Agent error: {e}")
    import traceback

    traceback.print_exc()
    # Yield error information as a dict
    yield {
      "type": "error",
      "error": str(e),
      "contents": [{"type": "text", "text": f"AI error: {str(e)}"}],
    }
