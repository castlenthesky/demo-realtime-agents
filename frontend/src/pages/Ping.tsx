import { For, createSignal, onCleanup, onMount } from 'solid-js'
import { useSocket } from '../context/socket'

export default function Ping() {
  const socket = useSocket()
  const [messageHistory, setMessageHistory] = createSignal<string[]>([])
  const [pendingAck, setPendingAck] = createSignal<(() => void) | null>(null)

  onMount(() => {
    const handlePong = () => {
      console.log('PONG received')
      setMessageHistory(prev => [...prev, 'Received PONG'])
    }

    const handleConnectionTest = (data: unknown, ack?: () => void) => {
      console.log('CONNECTION_TEST received', data)
      setMessageHistory(prev => [...prev, 'Received CONNECTION_TEST'])
      
      // Store the acknowledgment function if provided
      if (ack) {
        setPendingAck(() => ack)
      }
    }

    socket.on('PONG', handlePong)
    socket.on('CONNECTION_TEST', handleConnectionTest)

    // Cleanup listeners on component unmount
    onCleanup(() => {
      socket.off('PONG', handlePong)
      socket.off('CONNECTION_TEST', handleConnectionTest)
    })
  })

  const handlePing = () => {
    socket.emit('PING')
    setMessageHistory(prev => [...prev, 'Emitting PING'])
  }

  const acknowledgeTest = () => {
    const ack = pendingAck()
    if (ack) {
      ack()
      setMessageHistory(prev => [...prev, 'Acknowledged CONNECTION_TEST'])
      setPendingAck(null)
    }
  }

  return (
    <div>
      <h1>Ping & Pong</h1>
      <p>Click the button to send a PING event to the server and receive a PONG response.</p>
      <button onClick={handlePing} class="ping-button">
        PING
      </button>
      <button 
        onClick={acknowledgeTest} 
        class="acknowledge-test-button"
        disabled={!pendingAck()}
      >
        ACKNOWLEDGE TEST
      </button>
      {pendingAck() && (
        <p class="pending-ack-notice">CONNECTION_TEST received - click to acknowledge</p>
      )}
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

