import type { Socket } from 'socket.io-client'

/**
 * Socket event types for type safety
 */
export interface SocketEvents {
  agent_message: (message: unknown) => void
  message: (message: unknown) => void
  error: (error: Error) => void
  close: () => void
}

/**
 * Connection state handlers
 */
export interface ConnectionStateHandlers {
  setConnected: (value: boolean) => void
  setSocketId: (value: string | null) => void
}

/**
 * Cleanup function type
 */
export type CleanupFunction = () => void

