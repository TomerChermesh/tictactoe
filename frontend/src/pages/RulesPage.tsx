import React from 'react'
import { Box, Card, CardContent, Typography, Stack, Divider } from '@mui/material'

const RulesPage: React.FC = () => {
  return (
    <Box sx={{ width: '100%', maxWidth: 800 }}>
      <Typography variant='h4' align='center' sx={{ mb: 2, color: 'black' }}>
        Rules
      </Typography>

      <Card sx={{ borderRadius: 3 }}>
        <CardContent>
          <Stack spacing={2}>
            <Box>

              <Box sx={{ p: 2, borderRadius: 3, backgroundColor: 'rgba(255, 152, 0, 0.1)', border: '2px solid', borderColor: 'warning.main' }}>
                <Typography variant='body1' sx={{ mb: 1.5 }}>
                  Tic-Tac-Toe is a classic two-player game played on a 3x3 grid.
                </Typography>
                <Typography variant='body1' sx={{ mb: 1.5 }}><u>Objective:</u></Typography> Be the first player to get three of your marks in a row (horizontally, vertically, or diagonally).
                <Typography variant='body1' sx={{ mt: 1.5, mb: 1.5 }}><u>How to Play:</u></Typography>
                <Box component='ul' sx={{ pl: 3, mb: 0 }}>
                  <li>
                    <Typography variant='body1' component='span'>
                      Players take turns placing their mark (X or O) in an empty cell.
                    </Typography>
                  </li>
                  <li>
                    <Typography variant='body1' component='span'>
                      Player 1 always plays as <Typography variant='body1' component='span' style={{ color: '#ff9800' }}>X</Typography> (orange).
                      </Typography>
                  </li>
                  <li>
                    <Typography variant='body1' component='span'>
                      Player 2 always plays as <Typography variant='body1' component='span' style={{ color: '#2196f3' }}>O</Typography> (blue).
                    </Typography>
                  </li>
                  <li>
                    <Typography variant='body1' component='span'>
                      The game ends when one player wins or all cells are filled (draw).
                    </Typography>
                  </li>
                </Box>
              </Box>
            </Box>

            <Divider />

            <Box>
              <Typography variant='h5' sx={{ mb: 1.5, color: 'black', fontWeight: 'bold' }}> Game Modes </Typography>
              <Stack spacing={2}>
                <Box sx={{ p: 2, borderRadius: 3, backgroundColor: 'rgba(33, 150, 243, 0.1)', border: '2px solid', borderColor: 'info.main' }}>
                  <Typography variant='h6' sx={{ mb: 1, color: 'info.dark', fontWeight: 'bold' }}>
                    Player vs AI
                  </Typography>
                  <Typography variant='body1'>
                    Play against an AI opponent powered by Google's Gemini AI. The AI will analyze the board and make strategic moves to try to win or block your winning moves.
                  </Typography>
                </Box>

                <Box sx={{ p: 2, borderRadius: 3, backgroundColor: 'rgba(255, 152, 0, 0.1)', border: '2px solid', borderColor: 'warning.main' }}>
                  <Typography variant='h6' sx={{ mb: 1, color: 'warning.dark', fontWeight: 'bold' }}>
                    Player vs Player
                  </Typography>
                  <Typography variant='body1'>
                    Play against a friend on the same device. Take turns making moves and see who can outsmart the other!
                  </Typography>
                </Box>
              </Stack>
            </Box>
          </Stack>
        </CardContent>
      </Card>
    </Box>
  )
}

export default RulesPage

