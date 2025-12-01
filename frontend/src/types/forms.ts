export type AuthMode = 'login' | 'register'

export interface LoginFormProps {
    email: string
    password: string
    onChangeEmail: (v: string) => void
    onChangePassword: (v: string) => void
    onSubmit: () => void
    isLoading: boolean
    errorMessage: string | null
}

export interface RegisterFormProps extends LoginFormProps {
    confirmPassword: string
    onChangeConfirmPassword: (v: string) => void
}
