import re

from modules.prompts import router_chain, chain, FULL_CONTEXT_MAP
from modules.guardrails import *
from modules.rag import evaluate_answer


async def process_chat(db, user_id, msg):

    # 1️⃣ Block unsafe input
    if is_blocked(msg):
        return get_safe_fallback()


    # 2️⃣ Classify question
    category = router_chain.invoke({"question": msg})

    category = re.sub(r"[^a-z_]", "", category.lower())


    # 3️⃣ Get context
    context = FULL_CONTEXT_MAP.get(category)

    if not context:
        return get_safe_fallback()


    # 4️⃣ Generate response
    reply = chain.invoke({
        "context": context,
        "question": msg
    })


    # 5️⃣ Clean output
    reply = sanitize(reply)


    # 6️⃣ Quality check
    score = await evaluate_answer(msg, reply, context)

    if score < 0.6:
        reply = get_safe_fallback()


    return reply
