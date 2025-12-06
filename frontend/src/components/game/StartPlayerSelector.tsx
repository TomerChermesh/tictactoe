import React from 'react'
import { Box, Button, Stack, Typography } from '@mui/material'
import type { CellValue } from '../../types/game'

type Props = {
  value: CellValue
  onChange: (value: CellValue) => void
}

const StartPlayerSelector: React.FC<Props> = ({ value, onChange }) => {
  const isSelected = (v: CellValue) => value === v

  return (
    <Box>
      <Typography variant='body1' sx={{ my: 1, textAlign: 'center' }}>Who starts?</Typography>

      <Stack direction='row' spacing={1.5} justifyContent='center'>
        <Button variant={isSelected(1) ? 'contained' : 'outlined'} onClick={() => onChange(1)} sx={{ fontSize: '1.5rem' }}>X</Button>
        <Button variant={isSelected(0) ? 'contained' : 'outlined'} onClick={() => onChange(0)} sx={{ fontSize: '1.5rem' }}>🎲</Button>
        <Button variant={isSelected(2) ? 'contained' : 'outlined'} onClick={() => onChange(2)} sx={{ fontSize: '1.5rem' }}>O</Button> 
      </Stack>
    </Box>
  )
}

export default StartPlayerSelector
