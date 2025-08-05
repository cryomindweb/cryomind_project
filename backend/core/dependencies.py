from fastapi import Request, HTTPException, status
from authlib.jose import jwt
from core.config import settings

def verify_supabase_token(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no enviado")

    token = auth.split(" ")[1]

    try:
        claims = jwt.decode(
            token,
            settings.jwt_secret_key,  # usa el secret del .env
            claims_options={"exp": {"essential": True}}  # valida expiración
        )
        claims.validate()

        # Recupera el rol según cómo esté estructurado tu token
        role = claims.get("role") or claims.get("https://hasura.io/jwt/claims", {}).get("x-hasura-role")

        if role != "administrador":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado")

        return claims
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
