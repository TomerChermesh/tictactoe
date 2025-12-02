import { createApi } from '@reduxjs/toolkit/query/react'
import type { UpdateResponse } from '../types/matchup'
import type { PlayerID } from '../types/players'
import type { CellIndex, Game } from '../types/game'
import { normalizeResponse, normalizeGame } from '../utils/apiMappers'
import { baseQueryWithReauth } from './baseQuery'

export const gameApi = createApi({
  reducerPath: 'gameApi',
  baseQuery: baseQueryWithReauth,
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

      transformResponse: (response: any): UpdateResponse => normalizeResponse(response),

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

      transformResponse: (response: any): UpdateResponse => normalizeResponse(response),

      invalidatesTags: ['Game', 'Matchup']
    }),

    getLastGameForMatchup: builder.query<Game, string>({
      query: matchupId => ({
        url: '/game/last_for_matchup',
        method: 'GET',
        params: { matchup_id: matchupId }
      }),
      transformResponse: (response: any): Game => normalizeGame(response)
    })

  })
})

export const {
  useCreateNewGameMutation,
  usePlayerMoveMutation,
  useLazyGetLastGameForMatchupQuery
} = gameApi
