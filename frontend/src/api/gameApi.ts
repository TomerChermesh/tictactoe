import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { API_BASE_URL } from '../constants/api'
import type { UpdateResponse } from '../types/matchup'
import type { PlayerID } from '../types/players'
import type { CellIndex } from '../types/game'
import type { RootState } from '../store'
import { normalizeResponse } from '../utils/apiMappers'

export const gameApi = createApi({
  reducerPath: 'gameApi',
  baseQuery: fetchBaseQuery({
    baseUrl: API_BASE_URL,
    credentials: 'include',
    prepareHeaders: (headers, { getState }) => {
      const token = (getState() as RootState).auth.accessToken
      if (token) {
        headers.set('authorization', `Bearer ${token}`)
      }
      return headers
    }
  }),
  tagTypes: ['Game', 'Matchup'],

  endpoints: builder => ({

    createNewGame: builder.mutation<
      UpdateResponse,
      { matchupId: string; startingPlayer: PlayerID }
    >({
      query: body => ({
        url: '/game/new',
        method: 'POST',
        params: {
          matchup_id: body.matchupId,
          starting_player: body.startingPlayer
        }
      }),

      transformResponse: (response: any): UpdateResponse => (normalizeResponse(response)),

      invalidatesTags: ['Game']
    }),

    playerMove: builder.mutation<
      UpdateResponse,
      { gameId: string; playerId: PlayerID; cellIndex: CellIndex; isAiMove: boolean }
    >({
      query: body => ({
        url: `/game/${body.gameId}/move`,
        method: 'POST',
        params: {
          player_id: body.playerId,
          cell_index: body.cellIndex,
          is_ai_move: body.isAiMove
        }
      }),

      transformResponse: (response: any): UpdateResponse => (normalizeResponse(response)),

      invalidatesTags: ['Game', 'Matchup']
    })

  })
})

export const { useCreateNewGameMutation, usePlayerMoveMutation } = gameApi
