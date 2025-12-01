import React, { useState, useEffect } from 'react'
import { Box, Card, CardContent, Paper, Stack, TextField, Typography } from '@mui/material'
import type { Player } from '../../types/players'
import { toSymbol } from '../../utils/game'
import type { SymbolValue } from '../../types/game'

type PlayerPanelProps = {
  player: Player
  onNameChange: (name: string) => void
  isActive: boolean
}

const PlayerPanel: React.FC<PlayerPanelProps> = ({ player, onNameChange, isActive }) => {
  const [localName, setLocalName] = useState(player.name)
  
  useEffect(() => {
    setLocalName(player.name)
  }, [player.name])

  const symbol: SymbolValue = toSymbol(player.id)
  const isX: boolean = symbol === 'X'
  const chipBg = isX ? 'warning.main' : 'primary.main'

  const handleNameBlur = () => {
    const trimmedName = localName.trim()
    if (trimmedName.length > 0) {
      onNameChange(trimmedName)
    } else {
      setLocalName(player.name)
    }
  }

  return (
    <Stack spacing={2}>
      <Box
        sx={{
          px: 3,
          py: 1,
          borderRadius: 999,
          borderColor: 'white',
          bgcolor: chipBg,
          color: 'white',
          minWidth: 120,
          display: 'flex',
          justifyContent: 'center',
          alignSelf: 'center'
        }}
      >
        <Typography variant='h5' sx={{ letterSpacing: '0.25em' }}>
          {symbol}
        </Typography>
      </Box>

      <Card
        sx={{
            minWidth: 200,
            borderRadius: 3,
            borderWidth: 2,
            borderStyle: 'solid',
            borderColor: isActive ? 'green' : 'transparent'
        }}
      >
        <CardContent>
          <Stack spacing={2}>
            <TextField
              label='Player name'
              variant='standard'
              fullWidth
              value={localName}
              onChange={e => setLocalName(e.target.value)}
              onBlur={handleNameBlur}
              error={localName.trim().length === 0}
              helperText={localName.trim().length === 0 ? 'Player name cannot be empty' : ''}
              slotProps={{ htmlInput: { maxLength: 20 } }}
            />

            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.5 }}>
              <Typography variant='body2' sx={{ fontWeight: 500 }}>
                Score
              </Typography>

              <Paper
                elevation={0}
                sx={{
                  bgcolor: '#ffffff',
                  color: '#111827',
                  borderRadius: 2,
                  px: 2,
                  py: 1.5,
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center'
                }}
              >
                <Typography variant='h4' sx={{ fontFamily: '"Digital-7", monospace', letterSpacing: '0.1em' }} >
                  {player.score}
                </Typography>
              </Paper>
            </Box>
            
          </Stack>
        </CardContent>
      </Card>
    </Stack>
  )
}

export default PlayerPanel
