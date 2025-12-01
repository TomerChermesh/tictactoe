export interface User {
    id: string
    email: string
    created_at: string
    updated_at: string
  }
  
  export interface LoginRequest {
    email: string
    password: string
  }

  export interface RegisterRequest extends LoginRequest {}
  
  export interface AuthResponse {
    user: User
    accessToken: string
    tokenType: string
  }

  export interface LogoutResponse {
    ok: boolean
    message: string
  }