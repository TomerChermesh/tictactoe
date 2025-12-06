import React from 'react'
import { Box, Typography } from '@mui/material'

const Footer: React.FC = () => {
  return (
    <Box component='footer' sx={{ py: 2, textAlign: 'center' }}>
      <Typography variant='body2'>© 2025 by Tomer Chermesh</Typography>
    </Box>
  )
}

export default Footer
