import React from 'react'
import { Card, CardContent, Box } from '@mui/material'
import type { CellValue } from '../../types/game'
import Cell from './Cell'

interface BoardProps {
  board: CellValue[]
  onCellClick: (index: number) => void
}

const Board: React.FC<BoardProps> = ({ board, onCellClick }) => {
  return (
    <Card sx={{ borderRadius: 3 }}>
      <CardContent>
        <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 1, justifyContent: 'center' }}>
          {board.map((value, index) => (
            <Cell key={index} value={value} index={index} onClick={onCellClick}/>
          ))}
        </Box>
      </CardContent>
    </Card>
  )
}

export default Board
