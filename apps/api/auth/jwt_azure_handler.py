from fastapi import HTTPException
from jose import jwt, JWTError
import httpx

MICROSOFT_OPENID_CONFIG_URL = "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration"

openid_config_cache = None

def decode_token_azure(token: str, jwks: dict) -> dict:
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token header")

    rsa_key = {}
    for key in jwks.get("keys", []):
        if key.get("kid") == unverified_header.get("kid"):
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
            break

    if not rsa_key:
        raise HTTPException(status_code=401, detail="Unable to find appropriate key")

    try:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience="api://{client_id}",
            options={"verify_aud": False},
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

    return payload


async def get_openid_config():
    global openid_config_cache
    if openid_config_cache is None:
        async with httpx.AsyncClient() as client:
            response = await client.get(MICROSOFT_OPENID_CONFIG_URL)
            openid_config_cache = response.json()
    return openid_config_cache


async def get_jwks(openid_config: dict):
    jwks_url = openid_config.get("jwks_uri")
    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url)
        return response.json()
