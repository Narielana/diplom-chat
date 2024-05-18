from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import chat as chat_models
from src.utils import personal
from src.utils import const


async def handle(
    user_id: int,
    chat_id: str,
    conn: AsyncSession,
):
    user = await personal.get_user_info(user_id=user_id)
    if const.MASTER_ADMIN_ROLE not in user.roles and const.CHAT_ROLE not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect role",
        )

    query = select(
        chat_models.ChatMessages.message,
        chat_models.ChatMessages.created_at,
        chat_models.ChatMessages.creator_user_id,
        chat_models.ChatMessages.chat_id,
    ).where(chat_models.ChatMessages.chat_id == chat_id)

    messages = (await conn.exec(query)).fetchall()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'items': [
                {
                    'message': item.message,
                    'created_at': item.created_at.isoformat(),
                    'creator_user_id': item.creator_user_id, # TO DO: get user names
                    'is_author': item.creator_user_id == user_id,
                }
                for item in messages
            ]
        }
    )
