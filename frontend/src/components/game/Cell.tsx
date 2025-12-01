import React from 'react'
import { Button, Typography } from '@mui/material'
import type { CellValue } from '../../types/game'
import { toSymbol } from '../../utils/game'

interface CellProps {
  value: CellValue
  index: number
  onClick: (index: number) => void
  isWinning?: boolean
  disabled?: boolean
}

const Cell: React.FC<CellProps> = ({ value, index, onClick, isWinning = false, disabled = false }) => {
  const symbol = toSymbol(value)

  return (
    <Button
      variant='outlined'
      disabled={disabled}
      onClick={() => !disabled && onClick(index)}
      sx={{
        width: '100%',
        aspectRatio: '1 / 1',
        borderRadius: 3,
        borderColor: 'white',
        backgroundColor: isWinning ? '#c8f7c5' : '#f5efe6',
        transition: 'background-color 0.2s ease'
      }}
    >
      {symbol && (
        <Typography
          variant='h3'
          sx={{ fontWeight: 700, color: symbol === 'X' ? 'warning.main' : 'primary.main'}}
        >
          {symbol}
        </Typography>
      )}
    </Button>
  )
}

export default Cell
