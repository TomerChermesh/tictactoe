import React from 'react'
import { Box, Button } from '@mui/material'

interface Props {
  isFinished: boolean
  winnerName: string | null
  backgroundColor?: string
  onNewGame: () => void
  isResetting: boolean
}

const GameOverStatus: React.FC<Props> = ({
  isFinished,
  winnerName,
  backgroundColor = '#f5efe6',
  onNewGame,
  isResetting
}) => {
  if (!isFinished) return null

  const hasWinner = !!winnerName

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        alignItems: 'center',
        pointerEvents: 'none' // let clicks pass through except on button
      }}
    >
      <Box
        sx={{
          backgroundColor: hasWinner ? backgroundColor : 'transparent',
          padding: 1.5,
          borderRadius: 3,
          fontWeight: 700,
          color: hasWinner ? 'white' : 'black'
        }}
      >
        {hasWinner
          ? `Game finished! ${winnerName} won`
          : 'Game finished as a draw'}
      </Box>

      <Button
        variant='outlined'
        onClick={onNewGame}
        disabled={isResetting}
        sx={{ pointerEvents: 'auto', backgroundColor: 'white' }}
      >
        {isResetting ? 'Creating new game...' : 'New Game'}
      </Button>
    </Box>
  )
}

export default GameOverStatus


