import React from 'react'
import { Card, CardContent, Box } from '@mui/material'
import type { CellIndex, CellValue } from '../../types/game'
import Cell from './Cell'

interface BoardProps {
  board: CellValue[]
  onCellClick: (index: number) => void
  isFinished: boolean
  winningTriplet: CellIndex[] | undefined
}

const Board: React.FC<BoardProps> = ({ board, onCellClick, isFinished, winningTriplet }) => {
  const handleCellClick = (index: number) => {
    if (isFinished) return
    onCellClick(index)
  }

  return (
    <Card sx={{ borderRadius: 3 }}>
      <CardContent>
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: 1,
            justifyContent: 'center'
          }}
        >
          {board.map((value, index) => (
            <Cell
              key={index}
              value={value}
              index={index}
              onClick={handleCellClick}
              isWinning={winningTriplet?.includes(index as CellIndex)}
              disabled={isFinished}
            />
          ))}
        </Box>
      </CardContent>
    </Card>
  )
}

export default Board
