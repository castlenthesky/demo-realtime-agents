import type { Socket } from 'socket.io-client'
import type { ConnectionStateHandlers, CleanupFunction } from '../types'

/**
 * Sets up connection-related event listeners for the socket
 * Returns a cleanup function to remove all listeners
 */
export function setupConnectionListeners(
  socket: Socket,
  handlers: ConnectionStateHandlers
): CleanupFunction {
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

