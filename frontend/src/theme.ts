import { createTheme } from '@mui/material'


export const theme = createTheme({
    palette: {
      mode: 'light',
      primary: { main: '#2196f3' },
      warning: { main: '#ff9800' },
      background: { default: '#f5f5f5' }
    },
    typography: {
        fontFamily: 'Jumps Winter, sans-serif'
      }
  })