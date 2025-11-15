import { createSignal, onCleanup, onMount } from 'solid-js'
import { useSocket } from '../context/socket'

export default function Home() {
  const socket = useSocket()
  const [messageHistory, setMessageHistory] = createSignal<string[]>([])

  onMount(() => {
    const handlePong = (message: string) => {
      console.log('PONG', message)
      setMessageHistory(prev => [...prev, `PONG: ${message}`])
    }

    socket.on('PONG', handlePong)

    // Cleanup listener on unmount
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
      <h1>Home Page</h1>
      <p>Welcome to the home page!</p>
      <button onClick={handlePing} class="ping-button">
        PING
      </button>
      {messageHistory().length > 0 && (
        <div>
          <h3>Message History:</h3>
          <ul>
            {messageHistory().map((message) => (
              <li>{message}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

