import React from 'react'
import { Button, Typography } from '@mui/material'
import type { CellValue } from '../../types/game'
import { toSymbol } from '../../utils/game'

interface CellProps {
  value: CellValue
  index: number
  onClick: (index: number) => void
}

const Cell: React.FC<CellProps> = ({ value, index, onClick }) => {
  const symbol = toSymbol(value)

  return (
    <Button
      variant='outlined'
      onClick={() => onClick(index)}
      sx={{ width: '100%', backgroundColor: '#f5efe6', borderColor: 'white', aspectRatio: '1 / 1', borderRadius: 3 }}
    >
      {symbol && (
        <Typography
          variant='h3'
          sx={{
            fontWeight: 700,
            color: symbol === 'X' ? 'warning.main' : 'primary.main'
          }}
        >
          {symbol}
        </Typography>
      )}
    </Button>
  )
}

export default Cell
