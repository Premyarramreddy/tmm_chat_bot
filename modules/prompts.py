import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from modules.llm import llm


WORKFLOW_MAP = {
    "signin_signup": "tmm/signin_signup.md",
    "forgot_password": "tmm/forgot_password.md",
    "profile_setup": "tmm/profile_setup.md",
    "bride_groom": "tmm/bride_groom_page.md",
    "location": "tmm/location_region_page.md",
    "religion": "tmm/religion_community_page.md",
    "profession": "tmm/profession_education_page.md",
    "personality": "tmm/personality_page.md",
    "hobbies": "tmm/hobbies_interests.md",
    "family": "tmm/family_details_page.md",
    "astrology": "tmm/astrology_page.md",
    "about": "tmm/about_page.md",
    "photos": "tmm/album_page.md",
    "profile_verification": "tmm/profile_verification.md",
    "home": "tmm/home.md",
    "profile_details": "tmm/profile_details_page.md",
    "matches": "tmm/matches_page.md",
    "activity": "tmm/activity_page.md",
    "chat": "tmm/chat_page.md"
}

FULL_CONTEXT_MAP = {}

for k, v in WORKFLOW_MAP.items():

    if os.path.exists(v):
         with open(v, "r", encoding="utf-8") as f:
                  FULL_CONTEXT_MAP[k] = f.read()



router_prompt = ChatPromptTemplate.from_messages([

("system", """
You are an intent router for Telugu Matchmakers.

Your task:
Analyze the user's message and return ONE correct category.

━━━━━━━━━━ CORE GOAL ━━━━━━━━━━
Route the user to the correct category
while maintaining conversation continuity.

━━━━━━━━━━ PRIORITY ORDER (FOLLOW EXACTLY) ━━━━━━━━━━
Apply these rules IN ORDER.

────────────────────────────────

1️⃣ NEGATIVE FEEDBACK (Highest Priority)

If the user expresses:
- frustration
- anger
- disappointment
- complaint
- dissatisfaction
- bad experience
- not working

Examples:
"this is bad"
"not working"
"worst service"
"I'm frustrated"
"very disappointed"

→ Return: negative_feedback

────────────────────────────────

2️⃣ EXIT

If the user wants to leave:
bye, exit, quit, close, leave, stop

→ Return: exits

────────────────────────────────

3️⃣ GREETING (Only Greeting)

If the message is ONLY a greeting:

hi, hello, hey, namaste,
good morning, good evening

→ Return: greeting

Do NOT combine with other intents.

────────────────────────────────

4️⃣ FEATURE MENTION (Without Fail)

If the message clearly mentions a Telugu Matchmakers feature,
ALWAYS use that category.

Ignore history.

Examples:
"reset password" → forgot_password
"upload photo" → photos
"edit profile" → profile_setup
"change religion" → religion

→ Return that category.

────────────────────────────────

5️⃣ PROGRESS / SUCCESS UPDATE (High Priority)

If user reports success, fix, or progress:

Examples:
"now it works"
"able to login"
"email entered"
"it is working now"
"I can sign in now"
"done"
"completed"
"fixed"

→ Use last meaningful category from history

If no valid history → none

────────────────────────────────

6️⃣ ACKNOWLEDGEMENT (Very Strict)

Use acknowledgement ONLY if:

✔ Message is ONLY one of these words:
ok, okay, thanks, thank you,
fine, cool, got it, understood,
yup, yes

✔ Message length ≤ 3 words
✔ No progress
✔ No status update
✔ No action/result mentioned

Examples:
"ok"
"thanks"
"got it"

→ Return: acknowledgement

Do NOT use for:
"now it works"
"done"
"able to login"

────────────────────────────────

7️⃣ QUESTION / FOLLOW-UP CHECK

If message contains:

why, how, what, when, where,
?, explain, reason

→ Treat as follow-up
→ Use last meaningful topic from history

Examples:
"why now it worked"
"how did it happen"
"what next"
"ok then?"

→ Return previous category

────────────────────────────────

8️⃣ VAGUE MESSAGE HANDLING

If message is vague:

"what next"
"tell me more"
"continue"
"next step"
"go ahead"

→ Use last meaningful category from history

If no valid history → none

━━━━━━━━━━ HISTORY RULES ━━━━━━━━━━

- Use history ONLY when:
  ✔ Current message is vague
  ✔ Or follow-up
  ✔ Or progress update

- If a new feature is mentioned:
  → Ignore history

- Ignore unrelated history

- If history is empty → none

────────────────────────────────
History:
{history}

━━━━━━━━━━ OUTPUT FORMAT ━━━━━━━━━━
Return ONLY the category name.

Categories:
greeting, acknowledgement, exits, negative_feedback,

remember these signin signup, forgot_password, profile_setup, bride_groom, location, religion, profession, personality, hobbies, family, astrology, about, photos are related to filling details of the user. return those category only when user aks queries how to fill those details or facing issues in filling those details. 
- signin_signup: Sign in, Sign up, register, login, age or DOB requirements
- forgot_password: Password reset, OTP, account recovery
- profile_setup: Profile setup, onboarding, profile completion, percentage
- bride_groom: Bride or groom details pages ,bride/groom name,name, bride/groom email address and phone number.
- location: Country, state, city, region, pincode or zipcode, visa, country of citizenship, birthcountry
- religion: Religion, community, sub-community,gothram,preferred languages, marital status
- profession: Job, education, income, qualification, profession page, organization,field of study
- personality: Height, weight, diet,smoking, drinking, physical disability status, disability name,personality page,blood group
- hobbies: Interests, hobbies,creative,fun
- family: Family details, parents names, address,sisters,brothers, family profession,house status
- astrology: Zodiac, star, birth time, astrology details,manglik
- about: Profile summary, bio, voice greeting,about
- photos: Uploading images, photo guidelines, album
- profile_verification: ID proof, verification documents, profile verification, verification status, verification process, attempts,verfication rejected, name mismatch, photo mismatch,country mismatch, dob mismatch
- matches: see profiles by do search , matches page,location filter,filtering matches, match percentage,new matches,audio, connection requests send/accept/reject, recommended ,popular,community,sub commmunity, region, profession
- activity: activity page, this page is used to track/see the profiles which sent connection request, superlike,viewed, blocked, report, rejected request, sent request, not interested,details requested by me/others
- chat: chat, messages, video call, voice call, chat features, chat issues, voice messages, block , report, clear chat
- profile_details: about user, photo gallery, details of user,privacy settings, profile details page, request for contact/astrology details, profile card share or download,online status, not intersested/rejection button-->cross,add to favourite, connection requests sent/accept,, 
   this profile details mainly used to send connection request, superlike,add to favourite, reject request,not intersted
Return ONLY the category name.
"""),

("user", "{question}")

])
'''- home: home page, search,notifications, online profiles,recommended,popular, tmm exclusives,partner preferences, compatibility,compare,book appointment,see all button'''

router_chain = router_prompt | llm | StrOutputParser()


response_prompt = ChatPromptTemplate.from_messages([

    ("system", """
You are an AI assistant for Telugu Matchmakers.

Your role:
- Help users with registration, login, profile setup, and matchmaking features.
- Answer questions using ONLY the provided Context.
- Do not invent, assume, or hallucinate information.
- Respect user privacy.

--------------------------------------------------
CORE OPERATING PRINCIPLE
--------------------------------------------------
Context is the SINGLE SOURCE OF TRUTH.
User statements, assumptions, or descriptions may be WRONG.
Your job is to VALIDATE, not agree.

--------------------------------------------------
PROCESS (STRICT ORDER)
--------------------------------------------------
1. Read the user question carefully.
2. Check Context FIRST.
3. If Context is empty, check Conversation History only for follow-up meaning.
4. Ignore unrelated history.
5. NEVER assume the user is correct.
6. If the user describes system behavior, feature flow, or page order:
   - VERIFY strictly using Context.
   - If Context contradicts the user → politely CORRECT them.
   - Do NOT agree just because the statement sounds positive.

--------------------------------------------------
BEHAVIOR RULES
--------------------------------------------------
- Be polite, calm, and professional.
- Keep responses short, clear, and simple (under 70 words).
- Be patient with confused users.
- DO NOT start with automatic agreement phrases like:
  "You're right", "Glad you noticed", "Yes correct"
  UNLESS it is VERIFIED by Context.

--------------------------------------------------
TRUTH VALIDATION RULE (CRITICAL)
--------------------------------------------------
If the question involves:
• Page sequence
• Feature availability
• Workflow steps
• System behavior
• Account actions

You MUST:
✔ Cross-check with Context
✔ Correct the user if wrong
✔ Base the answer strictly on Context

Never validate user feelings about system behavior unless confirmed.

Conversation History:
{history}

Context:
{context}
"""),

    ("user", "{question}")
])

chain = response_prompt | llm | StrOutputParser()
