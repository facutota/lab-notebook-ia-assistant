import { PublicClientApplication, type AuthenticationResult, type Configuration } from "@azure/msal-browser"

const loginRequest = {
  scopes: ["openid", "profile", "email"],
}

let msalInstance: PublicClientApplication | null = null

function getRequiredEnv(name: "NEXT_PUBLIC_ENTRA_CLIENT_ID" | "NEXT_PUBLIC_ENTRA_TENANT_ID") {
  const value =
    name === "NEXT_PUBLIC_ENTRA_CLIENT_ID"
      ? process.env.NEXT_PUBLIC_ENTRA_CLIENT_ID?.trim()
      : process.env.NEXT_PUBLIC_ENTRA_TENANT_ID?.trim()

  if (!value) {
    throw new Error(`Falta configurar ${name}.`)
  }

  return value
}

function getMsalConfig(): Configuration {
  const clientId = getRequiredEnv("NEXT_PUBLIC_ENTRA_CLIENT_ID")
  const tenantId = getRequiredEnv("NEXT_PUBLIC_ENTRA_TENANT_ID")
  const redirectUri =
    process.env.NEXT_PUBLIC_ENTRA_REDIRECT_URI?.trim() ||
    (typeof window !== "undefined" ? window.location.origin : undefined)

  return {
    auth: {
      clientId,
      authority: `https://login.microsoftonline.com/${tenantId}`,
      redirectUri,
    },
    cache: {
      cacheLocation: "sessionStorage",
    },
  }
}

async function getMsalInstance() {
  if (!msalInstance) {
    msalInstance = new PublicClientApplication(getMsalConfig())
    await msalInstance.initialize()
  }

  return msalInstance
}

function getAccountEmail(result: AuthenticationResult) {
  const claims = result.idTokenClaims as Record<string, unknown> | undefined

  return (
    result.account?.username ||
    (typeof claims?.preferred_username === "string" ? claims.preferred_username : undefined) ||
    (typeof claims?.email === "string" ? claims.email : undefined)
  )
}

export async function loginWithMicrosoftPopup() {
  const instance = await getMsalInstance()
  const result = await instance.loginPopup(loginRequest)
  const email = getAccountEmail(result)

  if (!result.idToken || !email) {
    throw new Error("Microsoft Entra ID no devolvió un token o email válido.")
  }

  return {
    email,
    idToken: result.idToken,
  }
}
