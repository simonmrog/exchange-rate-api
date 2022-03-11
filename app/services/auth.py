from typing import Dict, Any

import json
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from app.config import settings
from app.core.httpx import HTTPClient
from app.schemas.auth import Token
from app.schemas.user import UserAuth
from app.services.user import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/access-token")


class AuthService:
    def __init__(self):
        self.__client = HTTPClient()

    def __create_access_token(self, subject: Dict[str, Any]):
        content = {"sub": json.dumps(subject)}
        encoded_jwt = jwt.encode(
            content, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    async def authenticate(self, *, username: str, password: str) -> Token:
        user_in_db = await user_service.find(
            payload={"username": username, "password": password}
        )

        if not user_in_db:
            raise HTTPException(
                status_code=403, detail="Could not validate credentials"
            )

        user = user_in_db[0]
        token = self.__create_access_token(
            subject={
                "id": user.id,
                "username": user.username,
                "rate_limit": user.rate_limit,
            }
        )
        return Token(access_token=token, token_type="bearer")

    async def get_current_user(
        self, *, token: str = Depends(oauth2_scheme)
    ) -> UserAuth:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user = json.loads(payload.get("sub"))
            if user is None:
                raise credentials_exception
        except (JWTError, ValidationError):
            raise credentials_exception
        return UserAuth(username=user["username"], rate_limit=user["rate_limit"])


auth_service = AuthService()
