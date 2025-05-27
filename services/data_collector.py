import requests
import json
import logging
from config import config

logger = logging.getLogger(__name__)

class SocialMediaDataCollector:
    def __init__(self, data_source="twitter"):
        self.data_source = data_source.lower()
        self.api_url = self.get_api_url()
        self.headers = self.get_headers()

    def get_api_url(self):
        if self.data_source == "twitter":
            return "https://api.twitter.com/2/tweets/search/recent"
        elif self.data_source == "facebook":
            return "https://graph.facebook.com/v11.0/me/feed"
        else:
            raise ValueError(f"Unsupported social media source: {self.data_source}")

    def get_headers(self):
        if self.data_source == "twitter":
            bearer_token = config.models.get('twitter_bearer_token', '')
            return {"Authorization": f"Bearer {bearer_token}"}
        return {}

    def collect_data(self, query="emergency OR help needed", max_results=10):
        if self.data_source == "twitter":
            params = {
                "query": query,
                "max_results": max_results,
                "tweet.fields": "created_at,text,author_id"
            }
        else:
            raise NotImplementedError("Only Twitter is currently supported.")

        try:
            logger.info(f"Requesting {self.data_source} posts with query: {query}")
            response = requests.get(self.api_url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            posts = [tweet["text"] for tweet in data.get("data", [])]
            return posts
        except requests.RequestException as e:
            logger.error(f"Failed to fetch data from {self.data_source}: {e}")
            return []
