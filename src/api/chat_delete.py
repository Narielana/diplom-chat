import uuid

from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import delete
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
    if const.MASTER_ADMIN_ROLE not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect role",
        )
    try:
        await conn.exec(
            delete(chat_models.ChatBase).
            where(chat_models.ChatBase.id == chat_id)
        )
        await conn.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
    )
