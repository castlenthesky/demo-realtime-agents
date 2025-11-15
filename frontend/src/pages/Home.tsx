import { useSocket } from '../context/socket'

export default function Home() {
  const socket = useSocket()

  const handleSendMessage = () => {
    socket.emit('CLIENT_MESSAGE', 'Hello, server!')
  }

  return (
    <div>
      <h1>Home Page</h1>
      <p>Welcome to today's demo!</p>
      <button onClick={handleSendMessage} class="ping-button">
        SEND MESSAGE TO SERVER
      </button>
    </div>
  )
}

