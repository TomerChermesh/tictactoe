import React, { useState } from 'react'
import { Box, Button, Card, CardContent, Stack } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import NewMatchupBox from '../components/game/NewMatchupBox'

const HomePage: React.FC = () => {
  const navigate = useNavigate()
  const [showNewMatchup, setShowNewMatchup] = useState<boolean>(false)

  const handleResume = () => {
    navigate('/game')
  }

  const handleRules = () => {
    alert('Rules יתווסף בהמשך')
  }

  const handleNewMatchupClick = () => {
    setShowNewMatchup(true)
  }

  const handleNewMatchupConfirm = () => {
    setShowNewMatchup(false)
    navigate('/game')
  }

  if (showNewMatchup) {
    return (
      <NewMatchupBox onConfirm={handleNewMatchupConfirm}/>
    )
  }

  return (
    <Box sx={{ width: '100%', maxWidth: 320, mt: 4 }}>
      <Card sx={{ width: '100%', borderRadius: 3 }}>
        <CardContent>
          <Stack spacing={1.5}>
            <Button variant='outlined' fullWidth onClick={handleResume}>
              Resume Game
            </Button>

            <Button variant='contained' fullWidth color='warning' onClick={handleNewMatchupClick}>
              New Matchup
            </Button>

            <Button variant='outlined' fullWidth onClick={handleRules}>
              Rules
            </Button>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  )
}

export default HomePage
