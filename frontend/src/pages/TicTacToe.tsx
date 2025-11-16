import { createSignal, onCleanup, onMount, For, Show } from 'solid-js'
import { useSocket } from '../context/socket'

type CellValue = 'X' | 'O' | ' '

export default function TicTacToe() {
  const socket = useSocket()

  // State signals
  const [board, setBoard] = createSignal<CellValue[][]>([
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' '],
  ])
  const [messages, setMessages] = createSignal<string[]>([])
  const [status, setStatus] = createSignal('Connecting...')
  const [gameOver, setGameOver] = createSignal(false)
  const [result, setResult] = createSignal<{ winner: string | null; is_tie: boolean } | null>(null)
  const [postGameInput, setPostGameInput] = createSignal('')

  // Convert column index to letter
  const colIndexToLetter = (index: number): string => {
    return ['a', 'b', 'c'][index]
  }

  // Check if it's human's turn (count X vs O)
  const isHumanTurn = (): boolean => {
    const flatBoard = board().flat()
    const xCount = flatBoard.filter(c => c === 'X').length
    const oCount = flatBoard.filter(c => c === 'O').length
    return xCount === oCount && !gameOver()
  }

  // Handle cell click
  const handleCellClick = (row: number, col: number) => {
    const cell = board()[row][col]

    console.log(`👆 Cell clicked: [${row}, ${col}], current value: "${cell}"`)

    // Validate move
    if (cell !== ' ') {
      console.log('❌ Cell not empty')
      return
    }
    if (gameOver()) {
      console.log('❌ Game is over')
      return
    }
    if (!isHumanTurn()) {
      console.log('❌ Not human turn')
      return
    }

    console.log('✅ Move is valid, updating board')

    // Optimistic update: Update board instantly for immediate feedback
    const newBoard = board().map((r, i) =>
      i === row ? r.map((c, j) => j === col ? 'X' : c) : [...r]
    )
    setBoard(newBoard)

    // Update status
    setStatus('AI is thinking...')

    // Emit move to server for AI to respond
    const moveData = {
      row: row + 1,
      col: colIndexToLetter(col),
    }
    console.log('📤 Emitting human_move:', moveData)
    socket.emit('human_move', moveData)
  }

  // Handle restart
  const handleRestart = () => {
    socket.emit('restart_game')
    setMessages([])
    setGameOver(false)
    setResult(null)
    setPostGameInput('')
  }

  // Handle post-game query
  const handlePostGameQuery = () => {
    const query = postGameInput().trim()
    if (!query) return

    socket.emit('post_game_query', { query })
    setMessages(prev => [...prev, `You: ${query}`])
    setPostGameInput('')
  }

  // Flash animation for AI moves
  const flashCell = (row: number, col: number) => {
    const cellId = `cell-${row}-${col}`
    const element = document.getElementById(cellId)
    if (element) {
      element.classList.add('ai-flash')
      setTimeout(() => {
        element.classList.remove('ai-flash')
      }, 600)
    }
  }

  // Setup socket listeners
  onMount(() => {
    // Emit join_game event to initialize the game on the server
    console.log('🎮 Emitting join_game event')
    socket.emit('join_game')

    socket.on('board_update', (data: { board: CellValue[][] }) => {
      console.log('📋 Received board_update:', data.board)
      setBoard(data.board)
    })

    socket.on('status_update', (data: { text: string }) => {
      console.log('📢 Received status_update:', data.text)
      setStatus(data.text)
    })

    socket.on('ai_message', (data: { text: string }) => {
      console.log('💬 Received ai_message:', data.text)
      setMessages(prev => [...prev, data.text])
    })

    socket.on('ai_tool_executed', (data: { tool: string; row: number; col: string }) => {
      console.log('🔧 Received ai_tool_executed:', data)
      if (data.tool === 'make_ai_turn') {
        // Flash the cell (convert from 1-indexed to 0-indexed)
        const rowIndex = data.row - 1
        const colIndex = { a: 0, b: 1, c: 2 }[data.col as 'a' | 'b' | 'c'] ?? 0
        console.log(`⚡ Flashing cell at [${rowIndex}, ${colIndex}]`)
        flashCell(rowIndex, colIndex)
      }
    })

    socket.on('game_over', (data: { winner: string | null; is_tie: boolean }) => {
      console.log('🏁 Received game_over:', data)
      setGameOver(true)
      setResult(data)

      if (data.is_tie) {
        setStatus("It's a tie! Want a rematch?")
      } else if (data.winner === 'X') {
        setStatus('You won! 🎉')
      } else {
        setStatus('AI wins! Better luck next time.')
      }
    })

    socket.on('invalid_move', (data: { reason: string }) => {
      console.warn('❌ Invalid move:', data.reason)
    })

    // Cleanup listeners
    onCleanup(() => {
      socket.off('board_update')
      socket.off('status_update')
      socket.off('ai_message')
      socket.off('ai_tool_executed')
      socket.off('game_over')
      socket.off('invalid_move')
    })
  })

  return (
    <div class="tic-tac-toe-container" style={{ padding: '2rem', 'max-width': '1200px', margin: '0 auto' }}>
      <h1 style={{ 'text-align': 'center', 'margin-bottom': '1rem' }}>Tic Tac Toe vs AI Agent</h1>

      {/* Status */}
      <div
        class="status-display"
        style={{
          'text-align': 'center',
          'font-size': '1.25rem',
          'margin-bottom': '1.5rem',
          'font-weight': 'bold',
        }}
      >
        {status()}
      </div>

      <div style={{ display: 'flex', gap: '2rem', 'flex-wrap': 'wrap' }}>
        {/* Game Board */}
        <div style={{ flex: '1', 'min-width': '300px' }}>
          <div
            class="board"
            style={{
              display: 'grid',
              'grid-template-columns': 'repeat(3, 100px)',
              gap: '8px',
              'justify-content': 'center',
            }}
          >
            <For each={board()}>
              {(row, rowIndex) => (
                <For each={row}>
                  {(cell, colIndex) => (
                    <button
                      id={`cell-${rowIndex()}-${colIndex()}`}
                      class="cell"
                      onClick={() => handleCellClick(rowIndex(), colIndex())}
                      disabled={cell !== ' ' || gameOver() || !isHumanTurn()}
                      style={{
                        width: '100px',
                        height: '100px',
                        'font-size': '3rem',
                        'font-weight': 'bold',
                        border: '2px solid #333',
                        'border-radius': '8px',
                        background: cell !== ' ' || gameOver() ? '#2a2a2a' : '#1a1a1a',
                        color: cell === 'X' ? '#4ade80' : '#f87171',
                        cursor: cell === ' ' && !gameOver() && isHumanTurn() ? 'pointer' : 'not-allowed',
                        transition: 'all 0.2s',
                      }}
                    >
                      {cell === 'X' ? '❌' : cell === 'O' ? '⭕' : ''}
                    </button>
                  )}
                </For>
              )}
            </For>
          </div>

          {/* Restart Button */}
          <button
            onClick={handleRestart}
            style={{
              display: 'block',
              margin: '1.5rem auto 0',
              padding: '0.75rem 2rem',
              'font-size': '1rem',
              'font-weight': 'bold',
              background: '#4f46e5',
              color: 'white',
              border: 'none',
              'border-radius': '8px',
              cursor: 'pointer',
            }}
          >
            New Game
          </button>
        </div>

        {/* AI Messages / Chat */}
        <div style={{ flex: '1', 'min-width': '300px' }}>
          <h2 style={{ 'margin-bottom': '1rem' }}>AI Commentary</h2>

          <div
            class="messages-container"
            style={{
              height: '400px',
              'overflow-y': 'auto',
              background: '#1a1a1a',
              border: '2px solid #333',
              'border-radius': '8px',
              padding: '1rem',
              'margin-bottom': '1rem',
            }}
          >
            <For each={messages()}>
              {(message) => (
                <div
                  class="message"
                  style={{
                    background: message.startsWith('You:') ? '#2563eb' : '#7c3aed',
                    padding: '0.75rem',
                    'border-radius': '8px',
                    'margin-bottom': '0.5rem',
                    'margin-left': message.startsWith('You:') ? '0' : 'auto',
                    'margin-right': message.startsWith('You:') ? 'auto' : '0',
                    'max-width': '85%',
                    'text-align': message.startsWith('You:') ? 'left' : 'right',
                  }}
                >
                  {message}
                </div>
              )}
            </For>
          </div>

          {/* Post-Game Chat Input */}
          <Show when={gameOver()}>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="text"
                value={postGameInput()}
                onInput={(e) => setPostGameInput(e.currentTarget.value)}
                onKeyPress={(e) => e.key === 'Enter' && handlePostGameQuery()}
                placeholder="Ask the AI about the game..."
                style={{
                  flex: '1',
                  padding: '0.75rem',
                  background: '#2a2a2a',
                  border: '2px solid #333',
                  'border-radius': '8px',
                  color: 'white',
                  'font-size': '1rem',
                }}
              />
              <button
                onClick={handlePostGameQuery}
                style={{
                  padding: '0.75rem 1.5rem',
                  background: '#10b981',
                  color: 'white',
                  border: 'none',
                  'border-radius': '8px',
                  cursor: 'pointer',
                  'font-weight': 'bold',
                }}
              >
                Send
              </button>
            </div>
          </Show>
        </div>
      </div>

      {/* CSS for flash animation */}
      <style>{`
        .ai-flash {
          background: #fbbf24 !important;
          transition: background 0.6s ease-out;
        }

        .messages-container::-webkit-scrollbar {
          width: 8px;
        }

        .messages-container::-webkit-scrollbar-track {
          background: #2a2a2a;
          border-radius: 4px;
        }

        .messages-container::-webkit-scrollbar-thumb {
          background: #4f46e5;
          border-radius: 4px;
        }

        .cell:hover:not(:disabled) {
          background: #333 !important;
          transform: scale(1.05);
        }

        .cell:active:not(:disabled) {
          transform: scale(0.95);
        }
      `}</style>
    </div>
  )
}
