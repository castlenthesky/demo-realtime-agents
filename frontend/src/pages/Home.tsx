import { useSocket } from '../context/socket'

export default function Home() {
  const socket = useSocket()

  const handleSendMessage = () => {
    socket.emit('CONNECTION_TEST', 'Hello, from the client!')
  }

  return (
    <div>
      <h1>Home Page</h1>
      <p>Giving your agents a mouth isn't enough - give them hands!</p>
      <button onClick={handleSendMessage} class="ping-button">
        SEND MESSAGE TO SERVER
      </button>
    </div>
  )
}

