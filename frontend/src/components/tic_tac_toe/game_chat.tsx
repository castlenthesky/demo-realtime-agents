import { createEffect, createSignal, For, onCleanup, onMount, Show } from 'solid-js'
import { useSocket } from '../../context/socket'

interface GameChatProps {
  gameOver: () => boolean
}

export default function GameChat(props: GameChatProps) {
  const socket = useSocket()
  const [messages, setMessages] = createSignal<string[]>([])
  const [postGameInput, setPostGameInput] = createSignal('')

  // Clear messages when a new game starts (gameOver goes from true to false)
  const [previousGameOver, setPreviousGameOver] = createSignal(props.gameOver())
  createEffect(() => {
    const currentGameOver = props.gameOver()
    const wasOver = previousGameOver()
    // If game was over and now it's not, a new game has started
    if (wasOver && !currentGameOver) {
      setMessages([])
      setPostGameInput('')
    }
    setPreviousGameOver(currentGameOver)
  })

  // Handle post-game query
  const handlePostGameQuery = () => {
    const query = postGameInput().trim()
    if (!query) return

    socket.emit('post_game_query', { query })
    setMessages(prev => [...prev, `You: ${query}`])
    setPostGameInput('')
  }

  // Setup socket listeners
  onMount(() => {
    socket.on('ai_message', (data: { text: string }) => {
      console.log('💬 Received ai_message:', data.text)
      setMessages(prev => [...prev, data.text])
    })

    // Cleanup listener
    onCleanup(() => {
      socket.off('ai_message')
    })
  })

  return (
    <div class="chat-section">
      <h2 class="chat-title">AI Commentary</h2>

      <div class="messages-container">
        <Show when={messages().length === 0}>
          <div class="empty-chat">
            <p>No messages yet. Start playing to see AI commentary!</p>
          </div>
        </Show>
        <For each={messages()}>
          {(message) => (
            <div class={`chat-message ${message.startsWith('You:') ? 'message-user' : 'message-ai'}`}>
              {message}
            </div>
          )}
        </For>
      </div>

      {/* Post-Game Chat Input */}
      <Show when={props.gameOver()}>
        <div class="chat-input-container">
          <input
            type="text"
            class="chat-input"
            value={postGameInput()}
            onInput={(e) => setPostGameInput(e.currentTarget.value)}
            onKeyPress={(e) => e.key === 'Enter' && handlePostGameQuery()}
            placeholder="Ask the AI about the game..."
          />
          <button onClick={handlePostGameQuery} class="chat-send-button">
            Send
          </button>
        </div>
      </Show>
    </div>
  )
}

