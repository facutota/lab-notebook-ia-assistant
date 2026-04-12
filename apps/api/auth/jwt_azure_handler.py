import httpx
from fastapi import HTTPException
from jose import JWTError, jwt

MICROSOFT_OPENID_CONFIG_URL_TEMPLATE = (
    "https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration"
)

openid_config_cache: dict[str, dict] = {}
jwks_cache: dict[str, dict] = {}


def decode_token_azure(token: str, jwks: dict, audience: str, issuer: str) -> dict:
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
            audience=audience,
            issuer=issuer,
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

    return payload


async def get_openid_config(tenant_id: str):
    if tenant_id not in openid_config_cache:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                MICROSOFT_OPENID_CONFIG_URL_TEMPLATE.format(tenant_id=tenant_id)
            )
            response.raise_for_status()
            openid_config_cache[tenant_id] = response.json()
    return openid_config_cache[tenant_id]


async def get_jwks(jwks_url: str):
    if jwks_url not in jwks_cache:
        async with httpx.AsyncClient() as client:
            response = await client.get(jwks_url)
            response.raise_for_status()
            jwks_cache[jwks_url] = response.json()
    return jwks_cache[jwks_url]
