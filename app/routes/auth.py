from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.auth import Token
from app.services.auth import auth_service

router = APIRouter()


@router.post(
    "/access-token",
    response_model=Token,
    status_code=200,
    responses={
        200: {"description": "Access Token"},
    },
)
async def access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    token = await auth_service.authenticate(
        username=form_data.username, password=form_data.password
    )
    return token
