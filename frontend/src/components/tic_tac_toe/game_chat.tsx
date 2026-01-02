// frontend/src/components/tic_tac_toe/game_chat.tsx

import agentImage from '../../assets/agent.png'

export default function GameChat() {
  return (
    <div>
      <h1>Game Chat</h1>
      <div id="agent-chat-container">
        <div id="agent_image_container">
          <img src={agentImage} alt="Agent" />
        </div>
      </div>
    </div>
  )
}
