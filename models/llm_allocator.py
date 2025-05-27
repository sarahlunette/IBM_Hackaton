import logging
from models.ibm_granite_integration import GraniteChatModel

logger = logging.getLogger(__name__)

class LLMResourceAllocator:
    def __init__(self):
        self.llm = GraniteChatModel()

    def allocate_with_llm(self, tweets):
        context = "\n".join(tweets)
        logger.info("Using LLM to generate a crisis summary and resource plan...")
        summary = self.llm.summarize_crisis(tweets)
        plan = self.llm.generate_response_plan(summary)
        logger.info(f"LLM Generated Plan: {plan}")
        return {"summary": summary, "plan": plan}
