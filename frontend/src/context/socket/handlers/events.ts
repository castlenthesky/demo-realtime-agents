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

  const handleMessage = (message: unknown) => {
    console.log('message', message)
  }

  const handleError = (error: Error) => {
    console.error('Socket error:', error)
  }

  const handleClose = () => {
    console.log('Socket closed')
  }

  socket.on('agent_message', handleAgentMessage)
  socket.on('message', handleMessage)
  socket.on('error', handleError)
  socket.on('close', handleClose)

  // Return cleanup function
  return () => {
    socket.off('agent_message', handleAgentMessage)
    socket.off('message', handleMessage)
    socket.off('error', handleError)
    socket.off('close', handleClose)
  }
}

