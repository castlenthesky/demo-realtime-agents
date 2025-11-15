import { createSignal, For, Show } from 'solid-js'

type CellValue = 'X' | 'O' | ''

export default function TicTacToe() {
  const [board, setBoard] = createSignal<CellValue[][]>([
    ['', '', ''],
    ['', '', ''],
    ['', '', ''],
  ])
  const [currentPlayer, setCurrentPlayer] = createSignal<'X' | 'O'>('X')
  const [winner, setWinner] = createSignal<CellValue | null>(null)

  const checkWinner = (board: CellValue[][]): CellValue | null => {
    // Check rows
    for (let i = 0; i < 3; i++) {
      if (board[i][0] && board[i][0] === board[i][1] && board[i][1] === board[i][2]) {
        return board[i][0]
      }
    }
    // Check columns
    for (let i = 0; i < 3; i++) {
      if (board[0][i] && board[0][i] === board[1][i] && board[1][i] === board[2][i]) {
        return board[0][i]
      }
    }
    // Check diagonals
    if (board[0][0] && board[0][0] === board[1][1] && board[1][1] === board[2][2]) {
      return board[0][0]
    }
    if (board[0][2] && board[0][2] === board[1][1] && board[1][1] === board[2][0]) {
      return board[0][2]
    }
    return null
  }

  const handleCellClick = (row: number, col: number) => {
    if (winner() || board()[row][col]) return

    const player = currentPlayer()
    const newBoard = board().map(r => [...r])
    newBoard[row][col] = player
    
    setBoard(newBoard)

    // Check for winner
    const newWinner = checkWinner(newBoard)
    if (newWinner) {
      setWinner(newWinner)
    } else {
      setCurrentPlayer(prev => prev === 'X' ? 'O' : 'X')
    }
  }

  const resetGame = () => {
    setBoard([
      ['', '', ''],
      ['', '', ''],
      ['', '', ''],
    ])
    setCurrentPlayer('X')
    setWinner(null)
  }

  return (
    <div class="tic-tac-toe-container">
      <h1>Tic Tac Toe</h1>
      <Show when={winner()}>
        <div class="winner-message">
          <p>Player {winner()} wins!</p>
        </div>
      </Show>
      <Show when={!winner()}>
        <p class="current-player">Current Player: <strong>{currentPlayer()}</strong></p>
      </Show>
      
      <div class="board">
        <For each={board()}>
          {(row, rowIndex) => (
            <div class="board-row">
              <For each={row}>
                {(cell, colIndex) => (
                  <button
                    class="cell"
                    onClick={() => handleCellClick(rowIndex(), colIndex())}
                    disabled={!!cell || !!winner()}
                  >
                    {cell}
                  </button>
                )}
              </For>
            </div>
          )}
        </For>
      </div>

      <button onClick={resetGame} class="reset-button">
        Reset Game
      </button>
    </div>
  )
}