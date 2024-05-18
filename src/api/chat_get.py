import uuid

from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import chat as chat_models
from src.utils import personal
from src.utils import const



async def handle(
    user_id: int,
    chat_info: chat_models.ChatCreate,
    conn: AsyncSession,
):
    user = await personal.get_user_info(user_id=user_id)
    if const.MASTER_ADMIN_ROLE not in user.roles and const.CHAT_ROLE not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect role",
        )

    query = select(
        chat_models.ChatBase.id,
        chat_models.ChatBase.name,
        chat_models.ChatBase.description
    ).where(chat_models.ChatParticipants.user_id == user_id).join(
        chat_models.ChatParticipants,
        chat_models.ChatParticipants.chat_id == chat_models.ChatBase.id,
    )

    chats = (await conn.exec(query)).fetchall()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'items': [
                {
                    'id': chat.id,
                    'name': chat.name,
                    'description': chat.description,
                }
                for chat in chats
            ]
        }
    )
