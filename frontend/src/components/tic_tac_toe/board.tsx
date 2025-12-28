// frontend/src/components/tic_tac_toe/board.tsx

import { For } from 'solid-js'

export type CellValue = 'X' | 'O' | null

interface BoardProps {
  board: () => CellValue[]
  onCellClick: (index: number) => void
  gameOver: () => boolean
  isHumanTurn: () => boolean
}

export default function Board(props: BoardProps) {
  return (
    <div class="board-container">
      <div class="board-grid">
        <For each={props.board()}>
          {(cell, index) => {
            const row = Math.floor(index() / 3)
            const col = index() % 3

            return (
              <button
                id={`cell-${row}-${col}`}
                class={`game-cell ${cell === 'X' ? 'cell-x' : cell === 'O' ? 'cell-o' : ''} ${cell !== null || props.gameOver() ? 'cell-filled' : ''}`}
                onClick={() => props.onCellClick(index())}
                disabled={cell !== null || props.gameOver() || !props.isHumanTurn()}
              >
                <span class="cell-content">
                  {cell === 'X' ? '❌' : cell === 'O' ? '⭕' : ''}
                </span>
              </button>
            )
          }}
        </For>
      </div>
    </div>
  )
}

