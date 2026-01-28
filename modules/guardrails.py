import re
import random


BLOCKED_PATTERNS = [
     r"system\s*prompt", r"developer", r"ignore\s+previous",
    r"bypass", r"jailbreak", r"training\s*data",
    r"source\s*document", r"vector", r"embedding",
    r"architecture", r"dump", r"reveal", r"internal", r"private"
]


SAFE_FALLBACKS = [
    "Please ask about our services.",
    "I can help only with organization queries.",
    "Kindly ask about platform features.",
     "I can assist only with organization-related services, features, and support queries.",
    "Sorry, I can help only with questions related to this organization.",
    "I’m here to provide guidance only on organization-specific topics.",
    "I’m unable to answer that. Please ask something about our organization’s services.",
    "My assistance is limited to organization-related queries only."

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
