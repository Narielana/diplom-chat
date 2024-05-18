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
    new_user: chat_models.ChatNewUser,
    conn: AsyncSession,
):
    user = await personal.get_user_info(user_id=user_id)
    if const.MASTER_ADMIN_ROLE not in user.roles and const.CHAT_ROLE not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect role",
        )

    dst_user = await personal.get_user_info_by_email(email=new_user.email)
    if const.MASTER_ADMIN_ROLE not in dst_user.roles and const.CHAT_ROLE not in dst_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect role",
        )

    await conn.exec(
        insert(chat_models.ChatParticipants),
        [
            {
                'id': uuid.uuid4().hex,
                'chat_id': new_user.chat_id,
                'user_id': dst_user.user_id,
            }
        ],
    )
    await conn.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
    )
