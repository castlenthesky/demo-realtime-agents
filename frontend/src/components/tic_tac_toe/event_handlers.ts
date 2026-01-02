// frontend/src/components/tic_tac_toe/event_handlers.ts

import type { Socket } from 'socket.io-client'
import type { CellValue } from './board'

export interface TicTacToeEventHandlers {
  setBoard: (board: CellValue[]) => void
  setStatus: (status: string) => void
  setGameOver: (gameOver: boolean) => void
  onError?: (message: string) => void
}

/**
 * Sets up all socket.io event listeners for the tic-tac-toe game
 * Returns a cleanup function to remove all listeners
 */
export function setupTicTacToeEventHandlers(
  socket: Socket,
  handlers: TicTacToeEventHandlers
): () => void {
  const { setBoard, setStatus, setGameOver, onError } = handlers

  // Handle board state reset
  const handleBoardStateReset = (boardState: CellValue[]) => {
    console.log('📋 Received BOARD_STATE_RESET:', boardState)
    setBoard(boardState)
  }

  // Handle board state updates from backend
  const handleBoardStateUpdated = (boardState: CellValue[]) => {
    console.log('📋 Received BOARD_STATE_UPDATED:', boardState)
    setBoard(boardState)
  }

  // Handle user move result confirmation
  const handleUserMoveResult = (data: { position: number }) => {
    console.log('✅ Received USER_MOVE_RESULT:', data)
    // Board state is already updated optimistically, this is just confirmation
  }

  // Handle game over result
  const handleGameOverResult = (result: string) => {
    console.log('🏁 Received GAME_OVER_RESULT:', result)
    setGameOver(true)

    if (result === 'Tie') {
      setStatus("It's a tie! Want a rematch?")
    } else if (result === 'Human wins') {
      setStatus('You won! 🎉')
    } else if (result === 'AI wins') {
      setStatus('AI wins! Better luck next time.')
    } else {
      setStatus(`Game over: ${result}`)
    }
  }

  // Handle AI tool execution (agent making a move)
  const handleAiToolExecuted = (data: {
    message: string
    board_state: CellValue[]
    status: string
  }) => {
    console.log('🔧 Received AI_TOOL_EXECUTED:', data)

    // Update board with AI's move
    if (data.board_state) {
      setBoard(data.board_state)
    }

    // Update status message
    if (data.message) {
      setStatus(data.message)
    }
  }

  // Handle agent message updates
  const handleAgentMessageUpdate = (data: { type: string, message: string }) => {
    if (data.type === 'text_reasoning') {
      console.log('🔧 Received TEXT_REASONING:', data.message)
    } else if (data.type === 'text') {
      console.log('🔧 Received TEXT:', data.message)
    } else if (data.type === 'function_call') {
      console.log('🔧 Received FUNCTION_CALL:', data.message)
    } else if (data.type === 'function_result') {
      console.log('🔧 Received FUNCTION_RESULT:', data.message)
    }
  }

  // Handle agent reasoning chunks
  const handleAgentReasoningChunk = (data: unknown) => {
    console.log('🧠 Received AGENT_REASONING_CHUNK:', data)
  }

  // Handle agent stream tokens
  const handleAgentStreamToken = (data: unknown) => {
    console.log('💬 Received AGENT_STREAM_TOKEN:', data)
  }

  // Handle agent function calls
  const handleAgentFunctionCall = (data: unknown) => {
    console.log('⚙️ Received AGENT_FUNCTION_CALL:', data)
  }

  // Handle agent function results
  const handleAgentFunctionResult = (data: unknown) => {
    console.log('📤 Received AGENT_FUNCTION_RESULT:', data)
  }

  // Handle agent game over
  const handleAgentGameOver = (data: unknown) => {
    console.log('🏁 Received AGENT_GAME_OVER:', data)
  }

  // Handle errors from backend
  const handleError = (data: { message: string }) => {
    console.error('❌ Received ERROR:', data.message)
    if (onError) {
      onError(data.message)
    } else {
      setStatus(`Error: ${data.message}`)
    }
  }

  // Register all event listeners
  socket.on('BOARD_STATE_RESET', handleBoardStateReset)
  socket.on('BOARD_STATE_UPDATED', handleBoardStateUpdated)
  socket.on('USER_MOVE_RESULT', handleUserMoveResult)
  socket.on('GAME_OVER_RESULT', handleGameOverResult)
  socket.on('AI_TOOL_EXECUTED', handleAiToolExecuted)
  socket.on('AGENT_MESSAGE_UPDATE', handleAgentMessageUpdate)
  socket.on('AGENT_REASONING_CHUNK', handleAgentReasoningChunk)
  socket.on('AGENT_STREAM_TOKEN', handleAgentStreamToken)
  socket.on('AGENT_FUNCTION_CALL', handleAgentFunctionCall)
  socket.on('AGENT_FUNCTION_RESULT', handleAgentFunctionResult)
  socket.on('AGENT_GAME_OVER', handleAgentGameOver)
  socket.on('ERROR', handleError)

  // Return cleanup function to remove all listeners
  return () => {
    socket.off('BOARD_STATE_RESET', handleBoardStateReset)
    socket.off('BOARD_STATE_UPDATED', handleBoardStateUpdated)
    socket.off('USER_MOVE_RESULT', handleUserMoveResult)
    socket.off('GAME_OVER_RESULT', handleGameOverResult)
    socket.off('AI_TOOL_EXECUTED', handleAiToolExecuted)
    socket.off('AGENT_MESSAGE_UPDATE', handleAgentMessageUpdate)
    socket.off('AGENT_REASONING_CHUNK', handleAgentReasoningChunk)
    socket.off('AGENT_STREAM_TOKEN', handleAgentStreamToken)
    socket.off('AGENT_FUNCTION_CALL', handleAgentFunctionCall)
    socket.off('AGENT_FUNCTION_RESULT', handleAgentFunctionResult)
    socket.off('AGENT_GAME_OVER', handleAgentGameOver)
    socket.off('ERROR', handleError)
  }
}
