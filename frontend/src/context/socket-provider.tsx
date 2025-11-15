import type { Socket } from 'socket.io-client'
import { io } from 'socket.io-client'
import type { ParentProps } from 'solid-js'
import { createContext, createSignal, onCleanup, onMount, useContext } from 'solid-js'
import { setupConnectionListeners } from './sockets/handle_connection'

interface SocketContextValue {
  socket: Socket
  connected: () => boolean
  socketId: () => string | null
}

const SocketContext = createContext<SocketContextValue>()

export function SocketProvider(props: ParentProps) {
  const [connected, setConnected] = createSignal(false)
  const [socketId, setSocketId] = createSignal<string | null>(null)

  const socket = io('http://localhost:8085', {
    transports: ['websocket', 'polling']
  })

  onMount(() => {
    socket.connect()

    // Setup connection listeners
    const cleanupConnectionListeners = setupConnectionListeners(socket, {
      setConnected,
      setSocketId
    })

    // Other socket listeners
    socket.on('agent_message', (message) => {
      console.log('agent_message', message)
    })

    socket.on('message', (message) => {
      console.log('message', message)
    })

    socket.on('error', (error) => {
      console.error('error', error)
    })

    socket.on('close', () => {
      console.log('close')
    })

    // Register cleanup
    onCleanup(() => {
      cleanupConnectionListeners()
      socket.disconnect()
    })
  })

  return (
    <SocketContext.Provider value={{ socket, connected, socketId }}>
      {props.children}
    </SocketContext.Provider>
  )
}

// This hook is used to get the socket instance
export function useSocket() {
  const context = useContext(SocketContext)
  if (!context) {
    throw new Error('useSocket must be used within a SocketProvider')
  }
  return context.socket
}

// This hook is used to get the socket status
export function useSocketStatus() {
  const context = useContext(SocketContext)
  if (!context) {
    throw new Error('useSocketStatus must be used within a SocketProvider')
  }
  return {
    connected: context.connected,
    socketId: context.socketId
  }
}

