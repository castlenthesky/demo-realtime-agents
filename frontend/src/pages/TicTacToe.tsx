// src/pages/TicTacToe.tsx

import { createSignal, onCleanup, onMount } from 'solid-js'
import Board, { type CellValue } from '../components/tic_tac_toe/board'
import { setupTicTacToeEventHandlers } from '../components/tic_tac_toe/event_handlers'
import GameChat from '../components/tic_tac_toe/game_chat'
import { useSocket } from '../context/socket'

export default function TicTacToe() {
  const socket = useSocket()

  // State signals
  const [board, setBoard] = createSignal<CellValue[]>([
    null, null, null,
    null, null, null,
    null, null, null,
  ])
  const [status, setStatus] = createSignal('Connecting...')
  const [gameOver, setGameOver] = createSignal(false)

  // Check if it's human's turn (O is human, X is AI)
  const isHumanTurn = (): boolean => {
    const xCount = board().filter(c => c === 'X').length
    const oCount = board().filter(c => c === 'O').length
    return oCount === xCount && !gameOver()
  }

  // Handle cell click
  const handleCellClick = (index: number) => {
    const cell = board()[index]

    console.log(`👆 Cell clicked: position ${index}, current value: "${cell}"`)

    // Validate move
    if (cell !== null) {
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
    const newBoard = board().map((c, i) => i === index ? 'O' : c)
    setBoard(newBoard)

    // Update status
    setStatus('AI is thinking...')

    // Emit move to server for AI to respond
    const moveData = { position: index }
    console.log('📤 Emitting USER_MOVE:', moveData)
    socket.emit('USER_MOVE', moveData)
  }

  // Handle restart
  const handleRestart = () => {
    socket.emit('GAME_RESET', {})
    setGameOver(false)
  }

  // Setup socket listeners
  onMount(() => {
    // Emit join_game event to initialize the game on the server
    console.log('🎮 Emitting join_game event')
    socket.emit('join_game')

    // Setup centralized event handlers
    const cleanup = setupTicTacToeEventHandlers(socket, {
      setBoard,
      setStatus,
      setGameOver,
    })

    // Cleanup listeners on component unmount
    onCleanup(cleanup)
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
