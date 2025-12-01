import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import type { Game } from '../types/game'

const GAME_STORAGE_KEY = 'currentGame'

interface GameSliceState {
  currentGame: Game | null
}

const getInitialState = (): GameSliceState => {
  if (typeof window === 'undefined') {
    return { currentGame: null }
  }

  try {
    const raw = window.localStorage.getItem(GAME_STORAGE_KEY)
    if (!raw) {
      return { currentGame: null }
    }

    const parsed = JSON.parse(raw) as Game

    if (!parsed.id || !parsed.board) {
      window.localStorage.removeItem(GAME_STORAGE_KEY)
      return { currentGame: null }
    }

    return { currentGame: parsed }
  } catch {
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(GAME_STORAGE_KEY)
    }
    return { currentGame: null }
  }
}

const initialState: GameSliceState = getInitialState()

const gameSlice = createSlice({
  name: 'game',
  initialState,
  reducers: {
    setGame: (state, action: PayloadAction<Game>) => {
      state.currentGame = action.payload

      if (typeof window !== 'undefined') {
        window.localStorage.setItem(GAME_STORAGE_KEY, JSON.stringify(action.payload))
      }
    },
    updateGame: (state, action: PayloadAction<Game>) => {
      if (state.currentGame && state.currentGame.id === action.payload.id) {
        state.currentGame = action.payload

        if (typeof window !== 'undefined') {
          window.localStorage.setItem(GAME_STORAGE_KEY, JSON.stringify(action.payload))
        }
      }
    },
    updateBoard: (state, action: PayloadAction<{ cellIndex: number; value: number }>) => {
      if (state.currentGame) {
        state.currentGame.board[action.payload.cellIndex] = action.payload.value as 0 | 1 | 2

        if (typeof window !== 'undefined') {
          window.localStorage.setItem(GAME_STORAGE_KEY, JSON.stringify(state.currentGame))
        }
      }
    },
    clearGame: state => {
      state.currentGame = null

      if (typeof window !== 'undefined') {
        window.localStorage.removeItem(GAME_STORAGE_KEY)
      }
    }
  }
})

export const { setGame, updateGame, updateBoard, clearGame } = gameSlice.actions
export default gameSlice.reducer
