import type { Socket } from 'socket.io-client'
import type { CleanupFunction } from '../types'

/**
 * Sets up application-specific event listeners for the socket
 * Returns a cleanup function to remove all listeners
 */
export function setupEventListeners(socket: Socket): CleanupFunction {
  const handleGlobalEvent = (message: unknown) => {
    console.log('global_event', message)
  }

  socket.on('global_event', handleGlobalEvent)

  // Return cleanup function
  return () => {
    socket.off('global_event', handleGlobalEvent)
  }
}

