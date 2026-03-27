import { mapAuthTokenResponse, type AuthTokens, type UserProfile } from "@/lib/auth/types"

const DEFAULT_DOMAIN_API_URL = "http://localhost:8000"

export function getDomainApiBaseUrl() {
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

function getAuthHeaders(accessToken: string) {
  return {
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  }
}

function splitFullName(fullName: string) {
  const parts = fullName.trim().split(/\s+/).filter(Boolean)
  if (parts.length === 0) {
    return { firstName: "", lastName: "" }
  }
  if (parts.length === 1) {
    return { firstName: parts[0], lastName: "" }
  }

  return {
    firstName: parts.slice(0, -1).join(" "),
    lastName: parts.at(-1) ?? "",
  }
}

export async function getMyProfile(accessToken: string): Promise<UserProfile> {
  const response = await fetch(`${getDomainApiBaseUrl()}/usuarios/me`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  })

  const payload = (await response.json()) as { id?: string; nombre_completo?: string; email?: string; detail?: string }

  if (!response.ok || !payload.id || !payload.email) {
    throw new Error(payload.detail ?? "No se pudo cargar el perfil.")
  }

  const name = splitFullName(payload.nombre_completo ?? "")

  return {
    id: payload.id,
    firstName: name.firstName,
    lastName: name.lastName,
    email: payload.email,
  }
}

export async function updateMyProfile(
  accessToken: string,
  input: { firstName: string; lastName: string }
): Promise<UserProfile> {
  const response = await fetch(`${getDomainApiBaseUrl()}/usuarios/me`, {
    method: "PUT",
    headers: getAuthHeaders(accessToken),
    body: JSON.stringify({
      nombre: input.firstName.trim(),
      apellido: input.lastName.trim(),
    }),
  })

  const payload = (await response.json()) as { id?: string; nombre_completo?: string; email?: string; detail?: string }

  if (!response.ok || !payload.id || !payload.email) {
    throw new Error(payload.detail ?? "No se pudo guardar el perfil.")
  }

  const name = splitFullName(payload.nombre_completo ?? "")

  return {
    id: payload.id,
    firstName: name.firstName,
    lastName: name.lastName,
    email: payload.email,
  }
}
