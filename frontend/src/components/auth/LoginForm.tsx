import React from 'react'
import { Stack, TextField, Button, Typography } from '@mui/material'
import type { LoginFormProps } from '../../types/forms'

const LoginForm: React.FC<LoginFormProps> = ({
  email,
  password,
  onChangeEmail,
  onChangePassword,
  onSubmit,
  isLoading,
  errorMessage
}) => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit()
  }

  return (
    <form onSubmit={handleSubmit}>
      <Stack spacing={2}>
        <TextField
          label='Email'
          type='email'
          fullWidth
          size='small'
          value={email}
          onChange={e => onChangeEmail(e.target.value)}
        />

        <TextField
          label='Password'
          type='password'
          fullWidth
          size='small'
          value={password}
          onChange={e => onChangePassword(e.target.value)}
        />

        <Button
          type='submit'
          variant='contained'
          fullWidth
          disabled={isLoading}
        >
          {isLoading ? 'Logging in...' : 'Log in'}
        </Button>

        {errorMessage && (
          <Typography color='error' sx={{ textAlign: 'center' }}>
            {errorMessage}
          </Typography>
        )}
      </Stack>
    </form>
  )
}

export default LoginForm
