import httpx
from fastapi import HTTPException, status

from src.models import user as user_models


URL_SERVER = 'http://127.0.0.1:8080/personal'


async def get_user_info(user_id: int) -> user_models.UserInfo:
    async with httpx.AsyncClient() as client:
        response = await client.get(URL_SERVER + '/v1/user_info', params={'user_id': user_id})
        user: user_models.UserInfo = response.json()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User doesn't exists",
            )

        return user


async def get_user_info_by_email(email: str) -> user_models.UserInfo:
    async with httpx.AsyncClient() as client:
        response = await client.get(URL_SERVER + '/v1/user_info/email', params={'email': email})
        user: user_models.UserInfo = response.json()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User doesn't exists",
            )

        return user
