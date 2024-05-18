import datetime
import typing as tp

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import (
    Column, DateTime, Integer, Text, ForeignKey
)
from sqlalchemy_utils import EmailType, force_auto_coercion

from src import db_base

force_auto_coercion()


class ChatCreate(BaseModel):
    name: str
    description: str


class MessageCreate(BaseModel):
    chat_id: str
    message: str


class ChatNewUser(BaseModel):
    chat_id: str
    email: str


class ChatUpdate(ChatCreate):
    chat_id: str


class ChatBase(db_base.Base):
    __tablename__ = "chats"

    id = Column(Text, primary_key=True, index=True)
    name = Column(Text,  nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc))


class ChatParticipants(db_base.Base):
    __tablename__ = "chat_participants"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Text, ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, nullable=False)


class ChatMessages(db_base.Base):
    __tablename__ = "chat_messages"

    id = Column(Text, primary_key=True, index=True)
    chat_id = Column(Text, ForeignKey('chats.id', ondelete='CASCADE'), nullable=False)
    creator_user_id = Column(Integer, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
