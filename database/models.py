import uuid
from sqlalchemy import Column, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from database.base import Base
from sqlalchemy import select

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    channel_id = Column(Text, nullable=False)      # user_id from JWT
    from_user_id = Column(Text, nullable=False)    # human OR 'chatbot'
    message = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )