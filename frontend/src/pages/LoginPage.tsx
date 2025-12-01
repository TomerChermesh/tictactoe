import React, { useState } from 'react'
import { Box, Card, CardContent, Tab, Tabs, Typography } from '@mui/material'
import { useNavigate, type NavigateFunction } from 'react-router-dom'
import { useLoginMutation, useRegisterMutation } from '../api/authApi'
import LoginForm from '../components/auth/LoginForm'
import RegisterForm from '../components/auth/RegisterForm'
import type { AuthMode } from '../types/forms'

const LoginPage: React.FC = () => {
  const navigate: NavigateFunction = useNavigate()

  const [mode, setMode] = useState<AuthMode>('login')

  const [email, setEmail] = useState<string>('')
  const [password, setPassword] = useState<string>('')
  const [confirmPassword, setConfirmPassword] = useState<string>('')

  const [authError, setAuthError] = useState<string | null>(null)

  const [login, { isLoading: loginLoading }] = useLoginMutation()
  const [register, { isLoading: registerLoading }] = useRegisterMutation()

  const isLoading: boolean = loginLoading || registerLoading

  const extractErrorMessage = (err: any): string => {
    if (err?.data?.detail) {
      return err.data.detail
    }

    return 'Something went wrong. Please try again.'
  }

  const handleLogin = async () => {
    setAuthError(null)

    try {
      await login({ email, password }).unwrap()
      navigate('/')
    } catch (e) {
      console.error('Login error:', e)
      setAuthError(extractErrorMessage(e))
    }
  }

  const handleRegister = async () => {
    setAuthError(null)

    try {
      await register({ email, password }).unwrap()
      navigate('/')
    } catch (e) {
      console.error('Register error:', e)
      setAuthError(extractErrorMessage(e))
    }
  }

  return (
    <Box sx={{ width: '100%', maxWidth: 400, mt: 4 }}>
      <Card sx={{ width: '100%', borderRadius: 3 }}>
        <CardContent>
          <Typography variant='h5' align='center' sx={{ mb: 2 }}>
            Welcome
          </Typography>

          <Tabs
            value={mode}
            onChange={(_, v) => {
              setMode(v)
              setAuthError(null)
            }}
            variant='fullWidth'
            sx={{ mb: 3 }}
          >
            <Tab label='Log in' value='login' />
            <Tab label='Register' value='register' />
          </Tabs>

          {mode === 'login' ? (
            <LoginForm
              email={email}
              password={password}
              onChangeEmail={setEmail}
              onChangePassword={setPassword}
              onSubmit={handleLogin}
              isLoading={isLoading}
              errorMessage={authError}
            />
          ) : (
            <RegisterForm
              email={email}
              password={password}
              confirmPassword={confirmPassword}
              onChangeEmail={setEmail}
              onChangePassword={setPassword}
              onChangeConfirmPassword={setConfirmPassword}
              onSubmit={handleRegister}
              isLoading={isLoading}
              errorMessage={authError}
            />
          )}
        </CardContent>
      </Card>
    </Box>
  )
}

export default LoginPage
