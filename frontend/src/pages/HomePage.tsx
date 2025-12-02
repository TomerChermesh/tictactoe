import React, { useState, useEffect } from 'react'
import { Box, Button, Card, CardContent, Stack } from '@mui/material'
import { useNavigate, useLocation } from 'react-router-dom'
import NewMatchupBox from '../components/game/NewMatchupBox'
import SnackbarAlert from '../components/general/SnackBarAlert'

const HomePage: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const [showNewMatchup, setShowNewMatchup] = useState<boolean>(false)
  const [showRulesAlert, setShowRulesAlert] = useState<boolean>(false)

  useEffect(() => {
    if (location.pathname === '/' && showNewMatchup) {
      setShowNewMatchup(false)
    }
  }, [location.key, location.pathname])

  const handleResume = () => {
    navigate('/game')
  }

  const handleRules = () => {
    navigate('/rules')
  }

  const handleNewMatchupClick = () => {
    setShowNewMatchup(true)
  }

  const handleNewMatchupConfirm = () => {
    setShowNewMatchup(false)
    navigate('/game')
  }

  const handleMatchupsList = () => {
    navigate('/matchups')
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
            {showRulesAlert && (
              <SnackbarAlert
                open={true}
                onClose={() => setShowRulesAlert(false)}
                severity='info'
                message='Rules will be added later.'
              />
            )}

            <Button variant='contained' color='success' fullWidth onClick={handleResume}>
              Resume Game
            </Button>

            <Button variant='contained' fullWidth color='info' onClick={handleNewMatchupClick}>
              New Matchup
            </Button>

            <Button variant='outlined' color='warning' fullWidth onClick={handleRules}>
              Rules
            </Button>

            <Button variant='outlined' color='secondary' fullWidth onClick={handleMatchupsList}>
              Matchups List
            </Button>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  )
}

export default HomePage
