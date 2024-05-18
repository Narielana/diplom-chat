import uuid

from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import insert
from sqlmodel.ext.asyncio.session import AsyncSession

from src.models import chat as chat_models
from src.utils import personal
from src.utils import const



async def handle(
    user_id: int,
    message: chat_models.MessageCreate,
    conn: AsyncSession,
):
    user = await personal.get_user_info(user_id=user_id)
    if const.MASTER_ADMIN_ROLE not in user.roles and const.CHAT_ROLE not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect role",
        )

    await conn.exec(
        insert(chat_models.ChatMessages),
        [
            {
                'chat_id': message.chat_id,
                'message': message.message,
                'creator_user_id': user_id,
            }
        ],
    )
    await conn.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
    )
