import { configureStore, createListenerMiddleware } from '@reduxjs/toolkit'
import { authApi } from '../api/authApi'
import { gameApi } from '../api/gameApi'
import { matchupApi } from '../api/matchupApi'
import authReducer from './authSlice'
import matchupReducer from './matchupSlice'
import gameReducer from './gameSlice'
import { clearMatchup } from './matchupSlice'
import { clearGame } from './gameSlice'

// Create listener middleware to clear matchup and game on logout
const listenerMiddleware = createListenerMiddleware()

listenerMiddleware.startListening({
  matcher: authApi.endpoints.logout.matchFulfilled,
  effect: async (_action, listenerApi) => {
    listenerApi.dispatch(clearMatchup())
    listenerApi.dispatch(clearGame())
  }
})

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
    getDefaultMiddleware()
      .concat(authApi.middleware, gameApi.middleware, matchupApi.middleware)
      .prepend(listenerMiddleware.middleware)
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
