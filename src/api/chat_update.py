import uuid

from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import update
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import chat as chat_models
from src.utils import personal
from src.utils import const


async def handle(
    user_id: int,
    chat_info: chat_models.ChatUpdate,
    conn: AsyncSession,
):
    user = await personal.get_user_info(user_id=user_id)
    if const.MASTER_ADMIN_ROLE not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect role",
        )

    query = (
        update(chat_models.ChatBase).
        where(chat_models.ChatBase.id == chat_info.chat_id).
        values(
            name = chat_info.name,
            description = chat_info.description,
        )
    )
    await conn.exec(query)
    await conn.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
    )
