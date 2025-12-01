import React, { useEffect, useState, useMemo } from 'react'
import { Box } from '@mui/material'
import Board from '../components/game/Board'
import PlayerPanel from '../components/game/PlayerPanel'
import { useNavigate } from 'react-router-dom'
import { useAppDispatch, useAppSelector } from '../store/hooks'
import { setGame } from '../store/gameSlice'
import { setMatchup } from '../store/matchupSlice'
import { usePlayerMoveMutation, useCreateNewGameMutation } from '../api/gameApi'
import { useUpdatePlayerNameMutation } from '../api/matchupApi'
import type { CellIndex } from '../types/game'
import type { PlayerID } from '../types/players'
import SnackbarAlert from '../components/general/SnackBarAlert'
import GameOverStatus from '../components/game/GameOverStatus'

const GamePage: React.FC = () => {
  const navigate = useNavigate()
  const dispatch = useAppDispatch()

  const currentGame = useAppSelector(state => state.game.currentGame)
  const currentMatchup = useAppSelector(state => state.matchup.currentMatchup)

  const [playerMove] = usePlayerMoveMutation()
  const [updatePlayerName] = useUpdatePlayerNameMutation()
  const [createNewGame, { isLoading: isResetting }] = useCreateNewGameMutation()

  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!currentGame || !currentMatchup) {
      navigate('/', { replace: true })
    }
  }, [currentGame, currentMatchup, navigate])

  if (!currentGame || !currentMatchup) {
    return null
  }

  const winnerName: string | null = useMemo(() => {
    if (!currentGame.isFinished || !currentGame.winner) return null

    if (currentMatchup.player1.id === currentGame.winner) {
      return currentMatchup.player1.name
    }

    if (currentMatchup.player2.id === currentGame.winner) {
      return currentMatchup.player2.name
    }

    return null
  }, [currentGame, currentMatchup])


  const handleError = (err: string) => {
    console.error(err)
    setError(err)
  }

  const handleCellClick = async (index: number) => {
    if (currentGame.isFinished) {
      handleError('The game is already finished')
      return
    }

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

      setError(null)
    } catch (err: any) {
      handleError(err.data.detail)
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
    } catch (err) {
      const msg = `Failed to update player name: ${err}`
      console.error(msg)
      handleError(msg)
    }
  }

  const handleResetBoard = async () => {
    try {
      const response = await createNewGame({
        matchupId: currentMatchup.id,
        startingPlayer: currentGame.currentTurn === 1 ? 2 : 1
      }).unwrap()

      if (response.game) {
        dispatch(setGame(response.game))
      }

      if (response.matchup) {
        dispatch(setMatchup(response.matchup))
      }

      setError(null)
    } catch (err) {
      handleError(`Failed to start new game: ${err}`)
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
            isActive={!currentGame.isFinished && currentGame.currentTurn === currentMatchup.player1.id}
            onNameChange={handlePlayer1NameChange}
          />
        </Box>

        <Box sx={{ width: { xs: '100%', md: '44%' }, maxWidth: 520 }}>
          {error && (
            <Box sx={{ mb: 2 }}>
              <SnackbarAlert
                open={true}
                onClose={() => setError(null)}
                severity='error'
                message={error}
              />
            </Box>
          )}

          <Board
            board={currentGame.board}
            onCellClick={handleCellClick}
            isFinished={currentGame.isFinished}
            winningTriplet={currentGame.winningTriplet ?? undefined}
          />

          {currentGame.isFinished && (
            <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
              <GameOverStatus
                backgroundColor={currentGame.winner === 1 ? 'warning.main' : 'primary.main'}
                isFinished={currentGame.isFinished}
                winnerName={winnerName}
                onNewGame={handleResetBoard}
                isResetting={isResetting}
              />
            </Box>
          )}
        </Box>

        <Box sx={{ width: { xs: '100%', md: '28%' }, maxWidth: 260 }}>
          <PlayerPanel
            player={currentMatchup.player2}
            isActive={
              !currentGame.isFinished &&
              currentMatchup.mode !== 'ai' &&
              currentGame.currentTurn === currentMatchup.player2.id
            }
            onNameChange={handlePlayer2NameChange}
          />
        </Box>
      </Box>
    </Box>
  )
}

export default GamePage
