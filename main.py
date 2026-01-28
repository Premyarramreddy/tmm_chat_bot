from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from database.session import get_db
from database.models import ChatMessage
from database.models import *
from modules.auth import get_current_user

from modules.chat import process_chat
from modules.questions import *

from schemas.chat import ChatRequest
from schemas.questions import QuestionsResponse

from config.logging import setup_logger


from config.settings import settings
from jose import jwt
from datetime import datetime, timedelta


logger = setup_logger()



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)



#for testing only
@app.get("/token")
def get_token(user_id: str):
    return {
        "token": create_test_token(user_id)
    }

# ======================
# TESTING ONLY
# ======================
def create_test_token(user_id: str):
    """
    Generate JWT for local testing only.
    Remove this in production.
    """
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=1),
        "iat": datetime.utcnow()
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)



from sqlalchemy import select


@app.get("/history")
async def get_chat_history(
    db=Depends(get_db),             
    user_id=Depends(get_current_user)
):

    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.channel_id == user_id)
        .order_by(ChatMessage.created_at.asc())
    )

    chats = result.scalars().all()

    return [
        {
            "id": str(chat.id),
            "channel_id": chat.channel_id,
            "from_user_id": chat.from_user_id,
            "message": chat.message,
            "created_at": chat.created_at.isoformat()
        }
        for chat in chats
    ]



BOT_ID = "chat_bot"


@app.post("/chat")
async def chat(
    req: ChatRequest,
    db=Depends(get_db),          # AsyncSession
    user_id=Depends(get_current_user)
):

    # 1️⃣ Save user message
    user_msg = ChatMessage(
        channel_id=user_id,
        from_user_id=user_id,
        message=req.message
    )

    db.add(user_msg)
    await db.commit()           


    # 2️⃣ Get bot reply
    reply = await process_chat(db, user_id, req.message)


    # 3️⃣ Save bot message
    bot_msg = ChatMessage(
        channel_id=user_id,
        from_user_id=BOT_ID,
        message=reply
    )

    db.add(bot_msg)
    await db.commit()           


    return {"reply": reply}

 

@app.get("/default-questions", response_model=QuestionsResponse)
def default_questions():

    return {"questions": DEFAULT_QUESTIONS}


@app.get("/related-questions", response_model=QuestionsResponse)
def related_questions(cat: str):

    return {
        "questions": RELATED_QUESTIONS.get(cat, [])
    }
