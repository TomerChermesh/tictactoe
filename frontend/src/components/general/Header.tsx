import { Box, Typography } from '@mui/material'

const Header = () => {
    return (
        <Box sx={{ display: 'flex', justifyContent: 'center', mb: 4 }}>
            <Typography variant='h3' component='h1' sx={{ color: 'black', fontFamily: 'Jumps Winter', letterSpacing: '0.15em', textTransform: 'uppercase', textAlign: 'center' }}>
                Tic Tac Toe
            </Typography>
        </Box>
    )
}

export default Header