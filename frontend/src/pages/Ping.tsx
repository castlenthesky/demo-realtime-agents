import { For, createSignal, onCleanup, onMount } from 'solid-js'
import { useSocket } from '../context/socket'

export default function Ping() {
  const socket = useSocket()
  const [messageHistory, setMessageHistory] = createSignal<string[]>([])

  onMount(() => {
    const handlePong = () => {
      console.log('PONG received')
      setMessageHistory(prev => [...prev, 'Received PONG'])
    }

    socket.on('PONG', handlePong)

    // Cleanup listener on component unmount
    onCleanup(() => {
      socket.off('PONG', handlePong)
    })
  })

  const handlePing = () => {
    socket.emit('PING')
    setMessageHistory(prev => [...prev, 'Emitting PING'])
  }

  return (
    <div>
      <h1>Ping & Pong</h1>
      <p>Click the button to send a PING event to the server and receive a PONG response.</p>
      <button onClick={handlePing} class="ping-button">
        PING
      </button>
      <div class="message-history">
        <h3>Message History</h3>
        {messageHistory().length === 0 ? (
          <p class="empty-state">No messages yet. Click PING to start!</p>
        ) : (
          <ul class="message-list">
            <For each={messageHistory()}>
              {(message) => (
                <li class="message-item">
                  <span class="message-text">{message}</span>
                </li>
              )}
            </For>
          </ul>
        )}
      </div>
    </div>
  )
}

