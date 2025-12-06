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
        height: '100vh',
        width: '100%',
        display: 'flex',
        flexDirection: 'column',
        backgroundImage: 'url("/ttt-bg.png")',
        backgroundRepeat: 'repeat',
        backgroundSize: 'auto',
        backgroundPosition: 'center',
        overflow: 'hidden',
        boxSizing: 'border-box'
      }}
    >
      <Box sx={{ width: '100%', pt: 6, pb: 3, px: 2, boxSizing: 'border-box', flexShrink: 0 }}>
        <Box sx={{ width: '100%', maxWidth: { xs: '100%', sm: 1200 }, mx: 'auto' }}>
          <Header />
        </Box>
      </Box>

      <Box sx={{ 
        flex: 1, 
        display: 'flex', 
        pb: 4, 
        width: '100%', 
        overflowY: 'auto',
        overflowX: 'hidden',
        px: 2,
        boxSizing: 'border-box'
      }}>
        <Box sx={{ 
          width: '100%', 
          maxWidth: { xs: '100%', sm: 1200 }, 
          mx: 'auto', 
          display: 'flex', 
          justifyContent: 'center',
          boxSizing: 'border-box'
        }}>
          {children}
        </Box>
      </Box>

      <Box sx={{ width: '100%', pb: 2, px: 2, boxSizing: 'border-box', flexShrink: 0 }}>
        <Box sx={{ width: '100%', maxWidth: { xs: '100%', sm: 1200 }, mx: 'auto' }}>
          <Footer />
        </Box>
      </Box>
    </Box>
  )
}

export default Layout
