import logging
from services.resource_allocator import ResourceAllocator
from services.llm_allocator import LLMResourceAllocator

logger = logging.getLogger(__name__)

class CrisisCoordinator:
    def __init__(self, mode="classic"):
        self.mode = mode
        self.classic = ResourceAllocator()
        self.llm = LLMResourceAllocator()

    def run_allocation(self):
        if self.mode == "classic":
            return self.classic.analyze_and_allocate()
        elif self.mode == "llm":
            tweets = self.classic.collector.collect_data(query="emergency", max_results=10)
            return self.llm.allocate_with_llm(tweets)
        else:
            raise ValueError("Unsupported mode. Choose 'classic' or 'llm'.")
