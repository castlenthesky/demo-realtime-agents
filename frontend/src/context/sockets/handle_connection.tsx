import type { Socket } from 'socket.io-client'

interface ConnectionHandlers {
  setConnected: (value: boolean) => void
  setSocketId: (value: string | null) => void
}

export function setupConnectionListeners(
  socket: Socket,
  handlers: ConnectionHandlers
): () => void {
  const { setConnected, setSocketId } = handlers

  const handleConnect = () => {
    setConnected(true)
    setSocketId(socket.id || null)
  }

  const handleDisconnect = () => {
    setConnected(false)
    setSocketId(null)
  }

  const handleConnectError = () => {
    setConnected(false)
    setSocketId(null)
  }

  socket.on('connect', handleConnect)
  socket.on('disconnect', handleDisconnect)
  socket.on('connect_error', handleConnectError)

  // Return cleanup function
  return () => {
    socket.off('connect', handleConnect)
    socket.off('disconnect', handleDisconnect)
    socket.off('connect_error', handleConnectError)
  }
}

