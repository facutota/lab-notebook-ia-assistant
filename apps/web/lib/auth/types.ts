export interface AuthTokens {
  accessToken: string
  refreshToken: string
}

export interface AuthSession extends AuthTokens {
  email: string
}

export interface UserProfile {
  id: string
  firstName: string
  lastName: string
  email: string
}

interface AuthApiTokenResponse {
  access_token: string
  refresh_token: string
}

export function mapAuthTokenResponse(payload: AuthApiTokenResponse): AuthTokens {
  return {
    accessToken: payload.access_token,
    refreshToken: payload.refresh_token,
  }
}
