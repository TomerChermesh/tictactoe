import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'
import { API_BASE_URL } from '../constants/api'
import type { AuthResponse, LoginRequest, RegisterRequest } from '../types/auth'
import type { RootState } from '../store'

export const authApi = createApi({
  reducerPath: 'authApi',
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
  endpoints: builder => ({
    login: builder.mutation<AuthResponse, LoginRequest>({
      query: body => ({
        url: '/auth/login',
        method: 'POST',
        body
      })
    }),
    register: builder.mutation<AuthResponse, RegisterRequest>({
      query: body => ({
        url: '/auth/register',
        method: 'POST',
        body
      })
    })
  })
})

export const { useLoginMutation, useRegisterMutation } = authApi
