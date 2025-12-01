import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { API_BASE_URL } from '../constants/api'
import type { UpdateResponse, MatchupMode } from '../types/matchup'
import type { PlayerID } from '../types/players'
import type { RootState } from '../store'
import { normalizeResponse } from '../utils/apiMappers'

export const matchupApi = createApi({
  reducerPath: 'matchupApi',
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
  tagTypes: ['Matchup', 'Game'],
  endpoints: builder => ({
    createNewMatchup: builder.mutation<
      UpdateResponse,
      { player1Name: string; player2Name: string; mode: MatchupMode; startingPlayer: PlayerID }
    >({
      query: body => ({
        url: '/matchup/new',
        method: 'POST',
        params: {
          player1_name: body.player1Name,
          player2_name: body.player2Name,
          mode: body.mode,
          starting_player: body.startingPlayer
        }
      }),
      transformResponse: (response: any): UpdateResponse => (normalizeResponse(response)),
      invalidatesTags: ['Matchup', 'Game']
    }),
    getMatchup: builder.query<UpdateResponse, string>({
      query: matchupId => `/matchup/${matchupId}`,
      transformResponse: (response: any): UpdateResponse => (normalizeResponse(response)),
      providesTags: (_result, _error, matchupId) => [{ type: 'Matchup', id: matchupId }]
    }),
    updatePlayerName: builder.mutation<
      UpdateResponse,
      { matchupId: string; playerId: PlayerID; name: string }
    >({
      query: body => ({
        url: `/matchup/${body.matchupId}/update_player_name`,
        method: 'PUT',
        params: {
          player_id: body.playerId,
          name: body.name
        }
      }),
      transformResponse: (response: any): UpdateResponse => (normalizeResponse(response)),
      invalidatesTags: (_result, _error, arg) => [{ type: 'Matchup', id: arg.matchupId }]
    })
  })
})

export const { useCreateNewMatchupMutation, useGetMatchupQuery, useUpdatePlayerNameMutation } =
  matchupApi

