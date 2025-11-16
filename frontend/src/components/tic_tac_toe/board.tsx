import { For } from 'solid-js'

export type CellValue = 'X' | 'O' | ' '

interface BoardProps {
  board: () => CellValue[][]
  onCellClick: (row: number, col: number) => void
  gameOver: () => boolean
  isHumanTurn: () => boolean
}

export default function Board(props: BoardProps) {
  return (
    <div class="board-container">
      <div class="board-grid">
        <For each={props.board()}>
          {(row, rowIndex) => (
            <For each={row}>
              {(cell, colIndex) => (
                <button
                  id={`cell-${rowIndex()}-${colIndex()}`}
                  class={`game-cell ${cell === 'X' ? 'cell-x' : cell === 'O' ? 'cell-o' : ''} ${cell !== ' ' || props.gameOver() ? 'cell-filled' : ''}`}
                  onClick={() => props.onCellClick(rowIndex(), colIndex())}
                  disabled={cell !== ' ' || props.gameOver() || !props.isHumanTurn()}
                >
                  <span class="cell-content">
                    {cell === 'X' ? '❌' : cell === 'O' ? '⭕' : ''}
                  </span>
                </button>
              )}
            </For>
          )}
        </For>
      </div>
    </div>
  )
}

