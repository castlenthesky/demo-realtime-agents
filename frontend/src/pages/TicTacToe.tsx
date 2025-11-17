import { createSignal, onCleanup, onMount } from 'solid-js'
import Board, { type CellValue } from '../components/tic_tac_toe/board'
import GameChat from '../components/tic_tac_toe/game_chat'
import { useSocket } from '../context/socket'

export default function TicTacToe() {
  const socket = useSocket()

  // State signals
  const [board, setBoard] = createSignal<CellValue[][]>([
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' '],
  ])
  const [status, setStatus] = createSignal('Connecting...')
  const [gameOver, setGameOver] = createSignal(false)

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
    setGameOver(false)
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
      socket.off('ai_tool_executed')
      socket.off('game_over')
      socket.off('invalid_move')
    })
  })

  return (
    <div class="tictactoe-page">
      <div class="tictactoe-header">
        <h1 class="tictactoe-title">Tic Tac Toe vs AI Agent</h1>
        <div class="status-display">{status()}</div>
      </div>

      <div class="tictactoe-content">
        {/* Game Board Section */}
        <div class="game-section">
          <Board
            board={board}
            onCellClick={handleCellClick}
            gameOver={gameOver}
            isHumanTurn={isHumanTurn}
          />

          <button onClick={handleRestart} class="new-game-button">
            <span>New Game</span>
          </button>
        </div>

        {/* AI Commentary Section */}
        <GameChat gameOver={gameOver} />
      </div>
    </div>
  )
}
