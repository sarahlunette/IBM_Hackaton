# services/resource_allocator.py

import os
import re
import logging
from models.allocation_model import AllocationModel
from services.data_collector import fetch_emergency_tweets
from resources.utilities import extract_needs_from_text

logger = logging.getLogger(__name__)

class ResourceAllocator:
    def __init__(self):
        self.model = AllocationModel()

    def analyze_and_allocate(self, location_filter="default region"):
        logger.info("Fetching emergency tweets...")
        tweets = fetch_emergency_tweets(location_filter=location_filter)
        if not tweets:
            logger.warning("No tweets found for the specified location.")
            return

        for tweet in tweets:
            logger.info(f"Analyzing tweet: {tweet}")
            needs_data = extract_needs_from_text(tweet)

            if not needs_data:
                logger.info("No clear emergency data found in tweet.")
                continue

            logger.debug(f"Extracted needs: {needs_data}")
            suggestion = self.model.predict_allocation(needs_data)
            logger.info(f"Suggested Allocation: {suggestion}\n")

