import { Alert, Snackbar } from "@mui/material";

interface Props {
    open: boolean
    onClose: () => void
    severity: 'info' | 'warning' | 'error' | 'success'
    message: string
}

const SnackbarAlert: React.FC<Props> = ({ open, onClose, severity, message }) => {
    return (
        <Snackbar
            open={open}
            autoHideDuration={3000}
            onClose={onClose}
            anchorOrigin={{ vertical: 'top', horizontal: 'left' }}
        >
            <Alert severity={severity} sx={{ width: '100%' }}>{message}</Alert>
        </Snackbar>
    )
}

export default SnackbarAlert
