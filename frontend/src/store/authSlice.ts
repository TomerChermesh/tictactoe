import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import type { PayloadAction } from '@reduxjs/toolkit'
import type { User, AuthResponse } from '../types/auth'
import { authApi } from '../api/authApi'
import { clearMatchup } from './matchupSlice'
import { clearGame } from './gameSlice'

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  accessToken: string | null
}

const AUTH_STORAGE_KEY = 'auth'

const getInitialState = (): AuthState => {
  if (typeof window === 'undefined') {
    return {
      user: null,
      isAuthenticated: false,
      accessToken: null
    }
  }

  try {
    const raw = window.localStorage.getItem(AUTH_STORAGE_KEY)
    if (!raw) {
      return {
        user: null,
        isAuthenticated: false,
        accessToken: null
      }
    }

    const parsed = JSON.parse(raw) as Partial<AuthState>

    return {
      user: parsed.user ?? null,
      isAuthenticated: !!parsed.user,
      accessToken: parsed.accessToken ?? null
    }
  } catch {
    return {
      user: null,
      isAuthenticated: false,
      accessToken: null
    }
  }
}

const initialState: AuthState = getInitialState()

export const logoutAndClearAll = createAsyncThunk(
  'auth/logoutAndClearAll',
  async (_, { dispatch }) => {
    dispatch(clearMatchup())
    dispatch(clearGame())
    dispatch(logout())
  }
)

const applyAuth = (state: AuthState, payload: AuthResponse) => {
  state.user = payload.user
  state.isAuthenticated = true
  state.accessToken = payload.accessToken ?? null

  if (typeof window !== 'undefined') {
    window.localStorage.setItem(
      AUTH_STORAGE_KEY,
      JSON.stringify({
        user: state.user,
        accessToken: state.accessToken
      })
    )
  }
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: state => {
      state.user = null
      state.isAuthenticated = false
      state.accessToken = null

      if (typeof window !== 'undefined') {
        window.localStorage.removeItem(AUTH_STORAGE_KEY)
        window.location.href = '/login'
      }
    },
    setAuth: (state, action: PayloadAction<AuthResponse>) => {
      applyAuth(state, action.payload)
    }
  },
  extraReducers: builder => {
    builder.addMatcher(
      authApi.endpoints.login.matchFulfilled,
      (state, { payload }) => {
        applyAuth(state, payload)
      }
    )

    builder.addMatcher(
      authApi.endpoints.register.matchFulfilled,
      (state, { payload }) => {
        applyAuth(state, payload)
      }
    )

    builder.addMatcher(
      authApi.endpoints.logout.matchFulfilled,
      state => {
        state.user = null
        state.isAuthenticated = false
        state.accessToken = null

        if (typeof window !== 'undefined') {
          window.localStorage.removeItem(AUTH_STORAGE_KEY)
          window.location.href = '/login'
        }
      }
    )
  }
})

export const { logout, setAuth } = authSlice.actions

export default authSlice.reducer
