import { Box, Typography, IconButton, Tooltip } from '@mui/material'
import MeetingRoomIcon from '@mui/icons-material/MeetingRoom'
import HomeIcon from '@mui/icons-material/Home'
import { useLocation, useNavigate } from 'react-router-dom'
import { useLogoutMutation } from '../../api/authApi'

const Header = () => {
    const location = useLocation()
    const navigate = useNavigate()
    const [logout] = useLogoutMutation()

    const isLoginPage: boolean = location.pathname === '/login'

    const handleLogout = async () => {
        try {
            await logout().unwrap()
        } catch (error) {
            console.error('Logout error:', error)
        }
    }

    const handleHome = () => {
        navigate('/')
    }

    return (
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
            <Box sx={{ flex: 1 }} />
            
            <Typography 
                variant='h3'
                component='h1'
                onClick={handleHome} 
                sx={{ 
                    color: 'black',
                    backgroundColor: 'white',
                    borderRadius: '50%',
                    fontFamily: 'Jumps Winter',
                    letterSpacing: '0.15em',
                    textAlign: 'center',
                    flex: 1,
                    cursor: 'pointer'
                }}
            >
                Tic Tac Toe
            </Typography>

            {!isLoginPage && (
                <Box sx={{ display: 'flex', gap: 2, flex: 1, justifyContent: 'flex-end' }}>
                    
                    <Tooltip title='Home'> 
                        <IconButton onClick={handleHome} color='inherit' aria-label='home' sx={{ backgroundColor: 'white', borderRadius: '50%' }}>
                            <HomeIcon fontSize='large' />
                        </IconButton>
                    </Tooltip>
                    
                    <Tooltip title='Logout'> 
                        <IconButton onClick={handleLogout} color='inherit' aria-label='logout' sx={{ backgroundColor: 'white', borderRadius: '50%' }}>
                            <MeetingRoomIcon fontSize='large' />
                        </IconButton>
                    </Tooltip>
                </Box>
            )}

            {isLoginPage && <Box sx={{ flex: 1 }} />}
        </Box>
    )
}

export default Header