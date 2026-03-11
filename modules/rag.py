import logging
from ragas import evaluate
from ragas.metrics import faithfulness
from datasets import Dataset
from ragas.llms import LangchainLLMWrapper
from modules.llm import llm


logger = logging.getLogger("ragas_eval")


async def evaluate_answer(q, a, ctx):

    logger.info("Starting RAGAS evaluation")

    try:
        logger.debug(f"Question: {q}")
        logger.debug(f"Answer length: {len(a)} chars")
        logger.debug(f"Context length: {len(ctx)} chars")


        # Build dataset
        ds = Dataset.from_list([
            {
                "question": q,
                "answer": a,
                "contexts": [ctx]
            }
        ])

        logger.info("Dataset prepared for evaluation")


        # Wrap LLM
        eval_llm = LangchainLLMWrapper(llm)

        logger.info("LLM wrapped for RAGAS evaluation")


        # Run evaluation
        logger.info("Running RAGAS faithfulness metric")

        result = evaluate(
            ds,
            metrics=[faithfulness],
            llm=eval_llm
        )

        logger.info("RAGAS evaluation completed")


        # Extract score
        score = result["faithfulness"]

        logger.debug(f"Raw faithfulness result: {score}")


        # Normalize output
        if isinstance(score, list):
            final_score = float(score[0])

        elif hasattr(score, "iloc"):   # pandas Series
            final_score = float(score.iloc[0])

        else:
            final_score = float(score)


        logger.info(f"Final faithfulness score: {final_score:.4f}")

        return final_score


    except Exception as e:

        logger.exception("RAGAS evaluation failed")

        return 0.0
