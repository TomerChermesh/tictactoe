import React, { useState } from 'react'
import { Box, Button, Card, CardContent, Stack, TextField, ToggleButton, ToggleButtonGroup, Typography } from '@mui/material'
import StartPlayerSelector from './StartPlayerSelector'
import { resolveStartingPlayer } from '../../utils/game'
import { useCreateNewMatchupMutation } from '../../api/matchupApi'
import { useAppDispatch } from '../../store/hooks'
import { setMatchup } from '../../store/matchupSlice'
import { setGame } from '../../store/gameSlice'
import type { CellValue } from '../../types/game'
import type { MatchupMode } from '../../types/matchup'
import type { PlayerID } from '../../types/players'

type Props = {
  onConfirm: () => void
}

const NewMatchupBox: React.FC<Props> = ({ onConfirm }) => {
  const dispatch = useAppDispatch()
  const [mode, setMode] = useState<MatchupMode>('ai')
  const [player1Name, setPlayer1Name] = useState<string>('Player 1')
  const [player2Name, setPlayer2Name] = useState<string>('AI Agent')
  const [startChoice, setStartChoice] = useState<CellValue>(0)
  const [createNewMatchup, { isLoading }] = useCreateNewMatchupMutation()

  const handleModeChange = (_: React.MouseEvent<HTMLElement>, value: MatchupMode | null) => {
    if (!value) return
    setMode(value)
    if (value === 'ai') {
      setPlayer2Name('AI Agent')
    } else {
      setPlayer2Name('Player 2')
    }
  }

  const handleConfirm = async () => {
    const startingPlayer: PlayerID = resolveStartingPlayer(startChoice)

    const finalPlayer1Name = player1Name.trim() || 'Player 1'
    const finalPlayer2Name = player2Name.trim() || (mode === 'ai' ? 'AI Agent' : 'Player 2')

    try {
      const response = await createNewMatchup({
        player1Name: finalPlayer1Name,
        player2Name: finalPlayer2Name,
        mode,
        startingPlayer
      }).unwrap()

      if (response.matchup) {
        dispatch(setMatchup(response.matchup))
      }
      if (response.game) {
        dispatch(setGame(response.game))
      }

      onConfirm()
    } catch (error) {
      console.error('Failed to create matchup:', error)
      alert(error)
    }
  }

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
      <Card sx={{ width: 'auto', maxWidth: 400, borderRadius: 3 }}>
        <CardContent>
          <Stack spacing={3}>
            <Typography variant='h5' align='center'>New Matchup</Typography>

            <Box>
              <ToggleButtonGroup value={mode} exclusive onChange={handleModeChange} fullWidth>
                <ToggleButton value='ai'>Player vs AI</ToggleButton>
                <ToggleButton value='friend'>Player vs Player</ToggleButton>
              </ToggleButtonGroup>
            </Box>

            <Stack spacing={2}>
              <TextField
                label='Player 1 name'
                fullWidth
                size='small'
                value={player1Name}
                onChange={e => setPlayer1Name(e.target.value)}
                slotProps={{ htmlInput: { maxLength: 20 } }}
              />
              {mode === 'friend' && (
                <TextField
                  label='Player 2 name'
                  fullWidth
                  size='small'
                  value={player2Name}
                  onChange={e => setPlayer2Name(e.target.value)}
                  slotProps={{ htmlInput: { maxLength: 20 } }}
                />
              )}
            </Stack>

            <StartPlayerSelector value={startChoice} onChange={setStartChoice} />

            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 1 }}>
              <Button variant='contained' onClick={handleConfirm} disabled={isLoading}>
                {isLoading ? 'Creating...' : 'Start game'}
              </Button>
            </Box>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  )
}

export default NewMatchupBox
