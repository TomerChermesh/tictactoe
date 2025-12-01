import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import type { Matchup } from '../types/matchup'

const MATCHUP_STORAGE_KEY = 'currentMatchup'

interface MatchupSliceState {
  currentMatchup: Matchup | null
}

const getInitialState = (): MatchupSliceState => {
  if (typeof window === 'undefined') {
    return { currentMatchup: null }
  }

  try {
    const raw = window.localStorage.getItem(MATCHUP_STORAGE_KEY)
    if (!raw) {
      return { currentMatchup: null }
    }

    const parsed = JSON.parse(raw) as Matchup

    if (!parsed.id || !parsed.player1 || !parsed.player2) {
      window.localStorage.removeItem(MATCHUP_STORAGE_KEY)
      return { currentMatchup: null }
    }

    return { currentMatchup: parsed }
  } catch {
    if (typeof window !== 'undefined') {
      window.localStorage.removeItem(MATCHUP_STORAGE_KEY)
    }
    return { currentMatchup: null }
  }
}

const initialState: MatchupSliceState = getInitialState()

const matchupSlice = createSlice({
  name: 'matchup',
  initialState,
  reducers: {
    setMatchup: (state, action: PayloadAction<Matchup>) => {
      state.currentMatchup = action.payload

      if (typeof window !== 'undefined') {
        window.localStorage.setItem(MATCHUP_STORAGE_KEY, JSON.stringify(action.payload))
      }
    },
    updateMatchup: (state, action: PayloadAction<Matchup>) => {
      if (state.currentMatchup && state.currentMatchup.id === action.payload.id) {
        state.currentMatchup = action.payload

        if (typeof window !== 'undefined') {
          window.localStorage.setItem(MATCHUP_STORAGE_KEY, JSON.stringify(action.payload))
        }
      }
    },
    updatePlayerName: (
      state,
      action: PayloadAction<{ playerId: 1 | 2; name: string }>
    ) => {
      if (state.currentMatchup) {
        if (action.payload.playerId === 1) {
          state.currentMatchup.player1.name = action.payload.name
        } else {
          state.currentMatchup.player2.name = action.payload.name
        }

        if (typeof window !== 'undefined') {
          window.localStorage.setItem(
            MATCHUP_STORAGE_KEY,
            JSON.stringify(state.currentMatchup)
          )
        }
      }
    },
    updatePlayerScore: (
      state,
      action: PayloadAction<{ playerId: 1 | 2; score: number }>
    ) => {
      if (state.currentMatchup) {
        if (action.payload.playerId === 1) {
          state.currentMatchup.player1.score = action.payload.score
        } else {
          state.currentMatchup.player2.score = action.payload.score
        }

        if (typeof window !== 'undefined') {
          window.localStorage.setItem(
            MATCHUP_STORAGE_KEY,
            JSON.stringify(state.currentMatchup)    
          )
        }
      }
    },
    clearMatchup: state => {
      state.currentMatchup = null

      if (typeof window !== 'undefined') {
        window.localStorage.removeItem(MATCHUP_STORAGE_KEY)
      }
    }
  }
})

export const {
  setMatchup,
  updateMatchup,
  updatePlayerName,
  updatePlayerScore,
  clearMatchup
} = matchupSlice.actions
export default matchupSlice.reducer

