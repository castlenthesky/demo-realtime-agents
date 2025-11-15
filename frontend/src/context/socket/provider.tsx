import type { Socket } from 'socket.io-client'
import { io } from 'socket.io-client'
import type { ParentProps } from 'solid-js'
import { createContext, createSignal, onCleanup, onMount, useContext } from 'solid-js'
import { SOCKET_CONFIG } from './config'
import { setupConnectionListeners } from './handlers/connection'
import { setupEventListeners } from './handlers/events'

interface SocketContextValue {
  socket: Socket
  connected: () => boolean
  socketId: () => string | null
}

const SocketContext = createContext<SocketContextValue>()

/**
 * SocketProvider manages the Socket.IO connection and provides it to child components
 */
export function SocketProvider(props: ParentProps) {
  const [connected, setConnected] = createSignal(false)
  const [socketId, setSocketId] = createSignal<string | null>(null)

  // Create socket instance with autoConnect disabled
  // We'll connect manually in onMount to ensure proper lifecycle management
  const socket = io(SOCKET_CONFIG.url, SOCKET_CONFIG.options)

  onMount(() => {
    // Connect the socket
    socket.connect()

    // Setup connection state listeners
    const cleanupConnectionListeners = setupConnectionListeners(socket, {
      setConnected,
      setSocketId,
    })

    // Setup application event listeners
    const cleanupEventListeners = setupEventListeners(socket)

    // Register cleanup function
    onCleanup(() => {
      cleanupConnectionListeners()
      cleanupEventListeners()
      socket.disconnect()
    })
  })

  return (
    <SocketContext.Provider value={{ socket, connected, socketId }}>
      {props.children}
    </SocketContext.Provider>
  )
}

/**
 * Hook to access the socket instance
 * @throws {Error} If used outside SocketProvider
 */
export function useSocket(): Socket {
  const context = useContext(SocketContext)
  if (!context) {
    throw new Error('useSocket must be used within a SocketProvider')
  }
  return context.socket
}

/**
 * Hook to access socket connection status
 * @throws {Error} If used outside SocketProvider
 */
export function useSocketStatus() {
  const context = useContext(SocketContext)
  if (!context) {
    throw new Error('useSocketStatus must be used within a SocketProvider')
  }
  return {
    connected: context.connected,
    socketId: context.socketId,
  }
}

