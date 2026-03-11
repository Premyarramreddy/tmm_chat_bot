import re

from modules.prompts import router_chain, chain, FULL_CONTEXT_MAP
from modules.guardrails import *
from modules.rag import evaluate_answer
from modules.history import *

async def process_chat(db, user_id, msg):

    # 1️⃣ Block unsafe input
    if is_blocked(msg):
        return get_safe_fallback()


    # 2️⃣ Classify question
    messages = await get_last_10_messages(db, user_id) 
    history=build_history_text(messages)
    
    category = router_chain.invoke({
        "question": msg,
        "history": history
    })


    category = re.sub(r"[^a-z_]", "", category.lower())
    print(category)

    if category == "greeting":
       return random.choice(GREETINGS)

    elif category == "acknowledgement":
        return random.choice(ACKS)

    elif category == "exits":
          return random.choice(EXITS)
    elif category == "negative_feedback":
        return random.choice(NEGATIVE_FEEDBACK_TEMPLATES)
    elif category=='none':
       return get_safe_fallback()
        
    # 3️⃣ Get context
    context = FULL_CONTEXT_MAP.get(category)

   ## if not context:
       # return get_safe_fallback()
    
    #  If router failed → try with history
    #if not context :
        #context=history
        

    # 4️⃣ Generate response'''
    reply = chain.invoke({
        "context": context,
        "question": msg,
        "history":history
        
    })


    # 5️⃣ Clean output
    reply = sanitize(reply)
    return reply
    
    print(reply)
    # 6️⃣ Quality check
    score = await evaluate_answer(msg, reply, context)

    if score < 0.6:
       reply = get_safe_fallback()

    return reply
 