import re
import random


BLOCKED_PATTERNS = [
     r"system\s*prompt", r"developer", r"ignore\s+previous",
    r"bypass", r"jailbreak", r"training\s*data",
    r"source\s*document", r"vector", r"embedding",
    r"architecture", r"dump", r"reveal", r"internal"
]


SAFE_FALLBACKS = [
    "Sorry 😔 I can help only with Telugu Matchmakers related questions. Please try again.",
    "I’m here to assist you with our platform services 😊 How can I help?",
    "Oops 🤔 That’s outside my scope. Please ask about Telugu Matchmakers.",
    "I can support you only with our services and features 👍 Please let me know your query.",
    "Let’s stay on topic 😊 Ask me anything about Telugu Matchmakers.",
    "I’m unable to help with that 😕 Please ask something about our platform.",
    "Sorry 🙏 I can assist only with organization-related queries.",
    "That’s not something I can help with right now 😇 Please try a platform-related question.",
    "I’m here for Telugu Matchmakers support 💙 Let me know how I can assist.",
    "Please ask about our services, profile, registration, or features 😊"
]

GREETINGS = [
    "Hi 👋 Welcome to Telugu Matchmakers! How can I help you today?",
    "Hello 😊 Glad to see you here! How may I assist you?",
    "Hey there 👋 Welcome aboard! What can I do for you?",
    "Namaste 🙏 Welcome to Telugu Matchmakers! How can I help?",
    "Hi 😊 Hope you're having a great day! How can I support you?",
    "Hello 👋 Happy to assist you! Please let me know your query.",
    "Hey 😊 Thanks for reaching out! What can I help you with?",
    "Welcome 👋 to Telugu Matchmakers! How may I help you today?"
]

ACKS = [
    "You're welcome 😊 Let me know if you need anything else!",
    "Happy to help 👍 Feel free to ask anytime.",
    "Glad I could assist you 😄 Let me know if you have more questions.",
    "No problem at all 😊 I'm here whenever you need me.",
    "You're most welcome 🙌 How else can I help?",
    "Anytime 👍 Just let me know if you need support.",
    "Always happy to help 😇 Please feel free to continue.",
    "Great! 😊 Let me know if there’s anything more I can do."
]

EXITS = [
    "Goodbye 👋 Thank you for using Telugu Matchmakers. Take care!",
    "Bye 😊 Wishing you all the best! See you soon.",
    "Take care 👋 Feel free to come back anytime!",
    "Thank you 🙏 Have a wonderful day ahead!",
    "Bye 👋 Stay safe and good luck with your journey!",
    "See you soon 😊 We’re always here to help.",
    "Session closed 👍 Thanks for choosing Telugu Matchmakers!",
    "Goodbye 🌟 Hope to assist you again soon!"
]

NEGATIVE_FEEDBACK_TEMPLATES = [
    "😔 Sorry for the inconvenience. I’m here to help you with Telugu Matchmakers. Please tell me what went wrong.",
    "🙏 I apologize for the trouble. Could you share your issue so I can assist you better?",
    "💙 I understand your frustration. Let’s work on this together and fix it.",
    "😓 Sorry if this was disappointing. Please explain your problem and I’ll try my best to help.",
     "🙏 I’m sorry to hear that. Please let me know what went wrong so I can assist you better."
    "💬 I’m really sorry about this. Your experience matters to us. Please let me know your concern.",
    "🌟 Apologies for the inconvenience. Let’s sort this out together. What seems to be the issue?"
]





def is_blocked(text: str):

    return any(
        re.search(p, text, re.I)
        for p in BLOCKED_PATTERNS
    )


def get_safe_fallback():

    return random.choice(SAFE_FALLBACKS)


def sanitize(text: str):

    return re.sub(r"[\*\#\_]", "", text).strip()
