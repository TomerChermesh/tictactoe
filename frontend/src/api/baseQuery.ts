import { fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import type { FetchBaseQueryError } from '@reduxjs/toolkit/query'
import { API_BASE_URL } from '../constants/api'
import type { RootState } from '../store'
import { logout } from '../store/authSlice'
import { clearMatchup } from '../store/matchupSlice'
import { clearGame } from '../store/gameSlice'

const baseQuery = fetchBaseQuery({
  baseUrl: API_BASE_URL,
  credentials: 'include',
  prepareHeaders: (headers, { getState }) => {
    const token = (getState() as RootState).auth.accessToken
    if (token) {
      headers.set('authorization', `Bearer ${token}`)
    }
    return headers
  }
})

export const baseQueryWithReauth = async (args: any, api: any, extraOptions: any) => {
  const result = await baseQuery(args, api, extraOptions)
  
  if (result.error && (result.error as FetchBaseQueryError).status === 401) {
    api.dispatch(clearMatchup())
    api.dispatch(clearGame())
    api.dispatch(logout())
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }
  
  return result
}

