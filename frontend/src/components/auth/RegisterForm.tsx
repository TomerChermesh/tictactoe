import React from 'react'
import { Stack, TextField, Button, Typography } from '@mui/material'
import type { RegisterFormProps } from '../../types/forms'


const RegisterForm: React.FC<RegisterFormProps> = ({
  email,
  password,
  confirmPassword,
  onChangeEmail,
  onChangePassword,
  onChangeConfirmPassword,
  onSubmit,
  isLoading,
  errorMessage
}) => {
  const passwordsDontMatch =
    password.length > 0 &&
    confirmPassword.length > 0 &&
    password !== confirmPassword

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!passwordsDontMatch) {
      onSubmit()
    }
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

        <TextField
          label='Confirm password'
          type='password'
          fullWidth
          size='small'
          value={confirmPassword}
          onChange={e => onChangeConfirmPassword(e.target.value)}
          error={passwordsDontMatch}
          helperText={
            passwordsDontMatch ? 'Passwords do not match' : ' '
          }
        />

        <Button
          type='submit'
          variant='contained'
          fullWidth
          disabled={isLoading || passwordsDontMatch}
        >
          {isLoading ? 'Registering...' : 'Register'}
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

export default RegisterForm
