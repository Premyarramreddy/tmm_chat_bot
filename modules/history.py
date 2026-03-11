from sqlalchemy import select
from database.models import ChatMessage


# Must match main.py
BOT_ID = "chat_bot"


# -----------------------------
# Get Last 10 Messages (Async)
# -----------------------------
async def get_last_10_messages(db, channel_id):

    stmt = (
        select(ChatMessage)
        .where(ChatMessage.channel_id == channel_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(10)
    )

    result = await db.execute(stmt)

    return result.scalars().all()


# -----------------------------
# Build History Text (Safe + Trimmed)
# -----------------------------
def build_history_text(messages, max_chars=3000):

    """
    Builds LLM-friendly history
    with size limit
    """

    lines = []

    for m in reversed(messages):

        if not m.message:
            continue

        role = "Bot" if m.from_user_id == BOT_ID else "User"

        text = m.message.strip()

        lines.append(f"{role}: {text}")


    history = "\n".join(lines)


    # ✂️ Hard truncate for token safety
    if len(history) > max_chars:
        history = history[-max_chars:]


    return history
