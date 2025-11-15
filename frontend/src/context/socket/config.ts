/**
 * Socket.IO configuration
 */
export const SOCKET_CONFIG = {
  url: import.meta.env.VITE_SOCKET_URL || 'http://localhost:8000',
  options: {
    transports: ['websocket', 'polling'] as ('websocket' | 'polling')[],
    autoConnect: false, // We'll connect manually in onMount
  },
} as const

