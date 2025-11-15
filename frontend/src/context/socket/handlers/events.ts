import type { Socket } from 'socket.io-client'
import type { CleanupFunction } from '../types'

/**
 * Sets up application-specific event listeners for the socket
 * Returns a cleanup function to remove all listeners
 */
export function setupEventListeners(socket: Socket): CleanupFunction {
  const handleAgentMessage = (message: unknown) => {
    console.log('agent_message', message)
  }

  const handleServerMessage = (message: unknown) => {
    console.log('server_message', message)
  } 

  socket.on('agent_message', handleAgentMessage)
  socket.on('SERVER_MESSAGE', handleServerMessage)

  // Return cleanup function
  return () => {
    socket.off('agent_message', handleAgentMessage)
    socket.off('SERVER_MESSAGE', handleServerMessage)
  }
}

