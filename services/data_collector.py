import requests
import json
from config import config

class SocialMediaDataCollector:
    def __init__(self, data_source):
        self.data_source = data_source
        self.api_url = self.get_api_url(data_source)
        
    def get_api_url(self, data_source):
        """
        Return the API URL based on the source (e.g., Twitter, Facebook).
        """
        if data_source == "twitter":
            return "https://api.twitter.com/2/tweets/search/recent"
        elif data_source == "facebook":
            return "https://graph.facebook.com/v11.0/me/feed"
        else:
            raise ValueError("Unsupported social media source")
    
    def collect_data(self, query_params):
        """
        Collect data from the social media API based on query parameters.
        """
        response = requests.get(self.api_url, params=query_params)
        return json.loads(response.text)

if __name__ == "__main__":
    collector = SocialMediaDataCollector(config.models['social_media_data_source'])
    data = collector.collect_data({"query": "help needed"})
    print(f"Collected Data: {data}")
