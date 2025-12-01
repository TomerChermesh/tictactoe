import { configureStore } from '@reduxjs/toolkit'
import { authApi } from '../api/authApi'
import { gameApi } from '../api/gameApi'
import { matchupApi } from '../api/matchupApi'
import authReducer from './authSlice'
import matchupReducer from './matchupSlice'
import gameReducer from './gameSlice'

export const store = configureStore({
  reducer: {
    [authApi.reducerPath]: authApi.reducer,
    [gameApi.reducerPath]: gameApi.reducer,
    [matchupApi.reducerPath]: matchupApi.reducer,
    auth: authReducer,
    matchup: matchupReducer,
    game: gameReducer
  },
  middleware: getDefaultMiddleware =>
    getDefaultMiddleware().concat(authApi.middleware, gameApi.middleware, matchupApi.middleware)
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
