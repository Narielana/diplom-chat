import typing as tp

from fastapi import APIRouter, Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from src import db
from src.api import chat_create, chat_delete, chat_update, chat_get
from src.models import chat as chat_models


router = APIRouter()


@router.post("/api/v1/chat")
async def create_chat(
    user_id: int,
    chat_info: chat_models.ChatCreate,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await chat_create.handle(user_id=user_id, chat_info=chat_info, conn=conn)


@router.get("/api/v1/chat")
async def get_chats(
    user_id: int,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await chat_get.handle(user_id=user_id, conn=conn)


@router.put("/api/v1/chat")
async def update_chat(
    user_id: int,
    chat_info: chat_models.ChatUpdate,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await chat_update.handle(user_id=user_id, chat_info=chat_info, conn=conn)


@router.delete("/api/v1/chat")
async def delete_chat(
    user_id: int,
    chat_id: str,
    conn: tp.Annotated[AsyncSession, Depends(db.get_db)],
):
    return await chat_delete.handle(user_id=user_id, chat_id=chat_id, conn=conn)
