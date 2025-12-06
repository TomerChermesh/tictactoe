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
  const [isAiThinking, setIsAiThinking] = useState<boolean>(false)

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

  useEffect(() => {
    if (
      currentMatchup.mode === 'ai' &&
      !currentGame.isFinished &&
      currentGame.currentTurn === currentMatchup.player2.id &&
      !isAiThinking &&
      !error
    ) {
      handleMove(true)
    }
  }, [currentGame.currentTurn])


  const handleError = (err: string) => {
    console.error(err)
    setError(err)
  }

  const handleMove = async (isAiMove: boolean, index?: number) => {
    if (isAiMove) {
      setIsAiThinking(true)
    }

    try {
      const response = await playerMove({
        gameId: currentGame.id,
        playerId: currentGame.currentTurn,
        cellIndex: index as CellIndex,
        isAiMove: isAiMove
      }).unwrap()
      if (response.game) {
        dispatch(setGame(response.game))
      }

      if (response.matchup) {
        dispatch(setMatchup(response.matchup))
      }

      setError(null)
    } catch (err: any) {
      handleError(err?.data?.detail ?? 'Failed to perform move')
    } finally {
      if (isAiMove) {
        setIsAiThinking(false)
      }
    }
  }


  const handleCellClick = async (index?: number) => {
    if (isAiThinking) {
      return
    }

    if (currentGame.isFinished) {
      handleError('The game is already finished')
      return
    }

    if (currentMatchup.mode === 'ai' && currentGame.currentTurn === currentMatchup.player2.id) {
      handleError('It is not your turn!')
      return
    }

    handleMove(false, index)
  }

  const handleUpdatePlayerName = async (playerId: PlayerID, name: string) => {
    if (!currentMatchup) return

    try {
      const response = await updatePlayerName({
        matchupId: currentMatchup.id,
        playerId,
        name
      }).unwrap()

      if (response.matchup) {
        dispatch(setMatchup(response.matchup))
      }
    } catch (err: any) {
      const msg = `Failed to update player name: ${err.data.detail}`
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
    } catch (err: any) {
      handleError(`Failed to start new game: ${err.data.detail}`)
    }
  }

  return (
    <Box sx={{ width: '100%', maxWidth: '100%', mt: 4, boxSizing: 'border-box', px: { xs: 1, sm: 0 } }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: { xs: 'column', md: 'row' },
          gap: { xs: 2, md: 6 },
          alignItems: 'flex-start',
          justifyContent: 'center',
          mb: 4,
          width: '100%',
          maxWidth: '100%',
          boxSizing: 'border-box'
        }}
      >
        <Box sx={{ width: { xs: '100%', md: '28%' }, maxWidth: { xs: '100%', md: 260 } }}>
          <PlayerPanel
            player={currentMatchup.player1}
            isActive={!currentGame.isFinished && currentGame.currentTurn === currentMatchup.player1.id}
            onNameChange={name => handleUpdatePlayerName(currentMatchup.player1.id, name)}
            isAi={false}
            isThinking={false}
          />
        </Box>

        <Box sx={{ width: { xs: '100%', md: '44%' }, maxWidth: { xs: '100%', md: 400 } }}>
          {error && (
              <SnackbarAlert
                open={true}
                onClose={() => setError(null)}
                severity='error'
                message={error}
              />
          )}

          <Board
            board={currentGame.board}
            onCellClick={handleCellClick}
            isFinished={currentGame.isFinished}
            winningTriplet={currentGame.winningTriplet ?? undefined}
          />

          <Box sx={{ mt: 2, minHeight: '60px', display: 'flex', flexDirection: 'column', gap: 2 }}> 
              {currentGame.isFinished && (
                  <GameOverStatus
                      backgroundColor={currentGame.winner === 1 ? 'warning.main' : 'primary.main'}
                      isFinished={currentGame.isFinished}
                      winnerName={winnerName}
                      onNewGame={handleResetBoard}
                      isResetting={isResetting}
                  />
              )}
          </Box>
        </Box>

        <Box sx={{ width: { xs: '100%', md: '28%' }, maxWidth: { xs: '100%', md: 260 } }}>
          <PlayerPanel
            player={currentMatchup.player2}
            isActive={!currentGame.isFinished && currentGame.currentTurn === currentMatchup.player2.id}
            onNameChange={name => handleUpdatePlayerName(currentMatchup.player2.id, name)}
            isAi={currentMatchup.mode === 'ai'}
            isThinking={
              currentMatchup.mode === 'ai' &&
              !currentGame.isFinished &&
              currentGame.currentTurn === currentMatchup.player2.id &&
              isAiThinking
            }
          />
        </Box>
      </Box>
    </Box>
  )
}

export default GamePage
