import React from 'react'
import { Box } from '@mui/material'
import Header from './Header'
import Footer from './Footer'

interface Props {
  children: React.ReactNode
}

const Layout: React.FC<Props> = ({ children }) => {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        width: '100vw',
        display: 'flex',
        flexDirection: 'column',
        backgroundImage: 'url("/ttt-bg.png")',
        backgroundRepeat: 'repeat',
        backgroundSize: 'auto',
        backgroundPosition: 'center'
      }}
    >
      <Box sx={{ width: '100%', px: 2, pt: 6, pb: 3 }}>
        <Box sx={{ width: '100%', maxWidth: 1200, mx: 'auto' }}>
          <Header />
        </Box>
      </Box>

      <Box sx={{ flex: 1, display: 'flex', px: 2, pb: 4 }}>
        <Box sx={{ width: '100%', maxWidth: 1200, mx: 'auto', display: 'flex', justifyContent: 'center' }}>
          {children}
        </Box>
      </Box>

      <Box sx={{ width: '100%', px: 2, pb: 2 }}>
        <Box sx={{ width: '100%', maxWidth: 1200, mx: 'auto' }}>
          <Footer />
        </Box>
      </Box>
    </Box>
  )
}

export default Layout
