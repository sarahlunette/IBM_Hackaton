import logging
from models.allocation_model import AllocationModel
from services.data_collector import SocialMediaDataCollector
from resources.utilities import extract_needs_from_text

logger = logging.getLogger(__name__)

class ResourceAllocator:
    def __init__(self):
        self.model = AllocationModel()
        self.collector = SocialMediaDataCollector()

    def analyze_and_allocate(self, query="emergency", location_filter=None):
        logger.info("Collecting emergency-related tweets...")
        tweets = self.collector.collect_data(query=query, max_results=10)
        if not tweets:
            logger.warning("No tweets found for the specified query.")
            return

        for tweet in tweets:
            logger.info(f"Analyzing tweet: {tweet}")
            needs_data = extract_needs_from_text(tweet)

            if not needs_data:
                logger.info("No identifiable emergency resources needed in tweet.")
                continue

            logger.debug(f"Extracted needs: {needs_data}")
            suggestion = self.model.predict_allocation(needs_data)
            logger.info(f"Suggested Allocation: {suggestion}\n")
