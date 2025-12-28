// src/pages/TicTacToe.tsx

import { createSignal, onCleanup, onMount } from 'solid-js'
import Board, { type CellValue } from '../components/tic_tac_toe/board'
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
    socket.emit('restart_game')
    setGameOver(false)
  }

  // Setup socket listeners
  onMount(() => {
    // Emit join_game event to initialize the game on the server
    console.log('🎮 Emitting join_game event')
    socket.emit('join_game')

    // Handle board updates from backend (backend sends flat array)
    socket.on('BOARD_STATE_UPDATED', (boardState: CellValue[]) => {
      console.log('📋 Received BOARD_STATE_UPDATED:', boardState)
      setBoard(boardState)
    })

    socket.on('board_update', (data: { board: CellValue[] }) => {
      console.log('📋 Received board_update:', data.board)
      setBoard(data.board)
    })

    socket.on('status_update', (data: { text: string }) => {
      console.log('📢 Received status_update:', data.text)
      setStatus(data.text)
    })

    socket.on('ai_tool_executed', (data: { message: string; board_state: CellValue[]; status: string }) => {
      console.log('🔧 Received ai_tool_executed:', data)

      // Update board with AI's move
      if (data.board_state) {
        setBoard(data.board_state)
      }

      // Update status message
      if (data.message) {
        setStatus(data.message)
      }
    })

    socket.on('game_over', (data: { winner: string | null; is_tie: boolean }) => {
      console.log('🏁 Received game_over:', data)
      setGameOver(true)

      if (data.is_tie) {
        setStatus("It's a tie! Want a rematch?")
      } else if (data.winner === 'O') {
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
      socket.off('BOARD_STATE_UPDATED')
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
