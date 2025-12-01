import { createApi } from '@reduxjs/toolkit/query/react'
import type { AuthResponse, LoginRequest, RegisterRequest, LogoutResponse } from '../types/auth'
import { baseQueryWithReauth } from './baseQuery'

export const authApi = createApi({
  reducerPath: 'authApi',
  baseQuery: baseQueryWithReauth,
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
    }),
    logout: builder.mutation<LogoutResponse, void>({
      query: () => ({
        url: '/auth/logout',
        method: 'POST'
      })
    })
  })
})

export const { useLoginMutation, useRegisterMutation, useLogoutMutation } = authApi
