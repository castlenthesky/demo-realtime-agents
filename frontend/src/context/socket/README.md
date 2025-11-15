# Socket Context Module

This module provides Socket.IO integration for the application through a React/SolidJS context provider.

## Structure

```
socket/
├── index.tsx           # Main entry point - exports provider and hooks
├── provider.tsx        # Context provider implementation
├── config.ts           # Socket configuration
├── types.ts            # TypeScript type definitions
└── @handlers/          # Event handlers (grouped for better navigation)
    ├── connection.ts   # Connection state management
    └── events.ts        # Application event handlers
```

## Usage

### Import the Provider
```tsx
import { SocketProvider } from './context/socket'

<SocketProvider>
  <App />
</SocketProvider>
```

### Use the Hooks
```tsx
import { useSocket, useSocketStatus } from './context/socket'

// Get socket instance
const socket = useSocket()
socket.emit('event', data)

// Get connection status
const { connected, socketId } = useSocketStatus()
```

## Design Decisions

### Why a singular `socket` folder?
- **Cohesion**: All socket-related code lives together
- **Scalability**: Easy to add more contexts (e.g., `context/auth/`, `context/theme/`)
- **Convention**: Singular folder names are more conventional in React/SolidJS codebases
- **Discoverability**: Everything is in one place, easier to find

### Why `index.tsx` as entry point?
- **Clean imports**: `import { SocketProvider } from './context/socket'` instead of `'./context/socket/provider'`
- **Barrel export pattern**: Common pattern in modern JavaScript/TypeScript
- **Flexibility**: Can re-export multiple things or add module-level logic

### File naming conventions
- `provider.tsx` - The actual provider component
- `@handlers/` - Special directory prefix groups handlers together in file explorers
- `connection.ts` - Connection-related logic (not `handle_connection.tsx`)
- `events.ts` - Event handlers (not `handle_events.tsx`)
- Shorter, clearer names without redundant prefixes

### Why `@handlers` directory?
- **Visual grouping**: The `@` prefix groups related files together in most file explorers
- **Better navigation**: Handlers are clearly separated from core module files
- **Scalability**: Easy to add more handler files as the application grows
- **Organization**: Clear distinction between core logic and event handling logic

