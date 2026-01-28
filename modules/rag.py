from ragas import evaluate
from ragas.metrics import faithfulness
from datasets import Dataset
from ragas.llms import LangchainLLMWrapper
from modules.llm import llm


async def evaluate_answer(q, a, ctx):

    ds = Dataset.from_list([
        {
            "question": q,
            "answer": a,
            "contexts": [ctx]
        }
    ])

    eval_llm = LangchainLLMWrapper(llm)

    result = evaluate(
        ds,
        metrics=[faithfulness],
        llm=eval_llm
    )

    score = result["faithfulness"]

    # ✅ Handle both formats safely
    if isinstance(score, list):
        return float(score[0])

    if hasattr(score, "iloc"):   # pandas Series
        return float(score.iloc[0])

    return float(score)  # normal number
