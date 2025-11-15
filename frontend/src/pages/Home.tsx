import { useSocket } from '../context/socket-provider'

export default function Home() {
  const socket = useSocket()

  const handlePing = () => {
    socket.emit('PING')
  }

  return (
    <div>
      <h1>Home Page</h1>
      <p>Welcome to the home page!</p>
      <button onClick={handlePing} class="ping-button">
        PING
      </button>
    </div>
  )
}

