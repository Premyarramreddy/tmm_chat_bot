from pydantic import BaseModel
from typing import List


class QuestionsResponse(BaseModel):

    questions: List[str]
