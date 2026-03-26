import { mapAuthTokenResponse, type AuthTokens } from "@/lib/auth/types"

const DEFAULT_DOMAIN_API_URL = "http://localhost:8000"

function getDomainApiBaseUrl() {
  const configuredUrl = process.env.NEXT_PUBLIC_DOMAIN_API_URL?.trim()
  return (configuredUrl || DEFAULT_DOMAIN_API_URL).replace(/\/$/, "")
}

export async function loginWithPassword(email: string, password: string): Promise<AuthTokens> {
  const formData = new URLSearchParams()
  formData.set("username", email.trim())
  formData.set("password", password)

  const response = await fetch(`${getDomainApiBaseUrl()}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData.toString(),
  })

  const payload = (await response.json()) as { detail?: string; access_token?: string; refresh_token?: string }

  if (!response.ok || !payload.access_token || !payload.refresh_token) {
    throw new Error(payload.detail ?? "No se pudo iniciar sesión.")
  }

  return mapAuthTokenResponse({
    access_token: payload.access_token,
    refresh_token: payload.refresh_token,
  })
}
