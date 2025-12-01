import React, { useEffect } from 'react'
import { Box } from '@mui/material'
import Board from '../components/game/Board'
import PlayerPanel from '../components/game/PlayerPanel'
import { useNavigate } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from '../store/hooks'
import { setGame } from '../store/gameSlice'
import { setMatchup } from '../store/matchupSlice'
import { usePlayerMoveMutation } from '../api/gameApi'
import { useUpdatePlayerNameMutation } from '../api/matchupApi'
import type { CellIndex } from '../types/game'
import type { PlayerID } from '../types/players'

const GamePage: React.FC = () => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()

  const currentGame = useAppSelector(state => state.game.currentGame)
  const currentMatchup = useAppSelector(state => state.matchup.currentMatchup)
  const [playerMove] = usePlayerMoveMutation()
  const [updatePlayerName] = useUpdatePlayerNameMutation()

  useEffect(() => {
    if (!currentGame || !currentMatchup) {
      navigate('/', { replace: true })
    }
  }, [currentGame, currentMatchup, navigate])

  if (!currentGame || !currentMatchup) {
    return null
  }

  const handleCellClick = async (index: number) => {
    try {
      const response = await playerMove({
        gameId: currentGame.id,
        playerId: currentGame.currentTurn,
        cellIndex: index as CellIndex
      }).unwrap()

      if (response.game) {
        dispatch(setGame(response.game))
      }

      if (response.matchup) {
        dispatch(setMatchup(response.matchup))
      }
    } catch (error) {
      console.error('Failed to make move:', error)
      alert(error)
    }
  }

  const handlePlayer1NameChange = async (name: string) => {
    if (!currentMatchup) return
    await handleUpdatePlayerName(currentMatchup.player1.id, name)
  }

  const handlePlayer2NameChange = async (name: string) => {
    if (!currentMatchup || currentMatchup.mode === 'ai') return
    await handleUpdatePlayerName(currentMatchup.player2.id, name)
  }

  const handleUpdatePlayerName = async (playerId: PlayerID, name: string) => {
    try {
      const response = await updatePlayerName({
        matchupId: currentMatchup.id,
        playerId,
        name
      }).unwrap()

      if (response.matchup) {
        dispatch(setMatchup(response.matchup))
      }
    } catch (error) {
      console.error('Failed to update player name:', error)
      alert(error)
    }
  }

  return (
    <Box sx={{ width: '100%', mt: 4 }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: { xs: 'column', md: 'row' },
          gap: 5,
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        <Box sx={{ width: { xs: '100%', md: '28%' }, maxWidth: 260 }}>
          <PlayerPanel
            player={currentMatchup.player1}
            isActive={currentGame.currentTurn === currentMatchup.player1.id}
            onNameChange={handlePlayer1NameChange}
          />
        </Box>

        <Box sx={{ width: { xs: '100%', md: '44%' }, maxWidth: 520 }}>
          <Board
            board={currentGame.board}
            onCellClick={handleCellClick}
          />
        </Box>

        <Box sx={{ width: { xs: '100%', md: '28%' }, maxWidth: 260 }}>
          <PlayerPanel
            player={currentMatchup.player2}
            isActive={currentGame.currentTurn === currentMatchup.player2.id}
            onNameChange={handlePlayer2NameChange}
          />
        </Box>
      </Box>
    </Box>
  )
}

export default GamePage
