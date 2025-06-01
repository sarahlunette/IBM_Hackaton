import logging

logger = logging.getLogger(__name__)

class SocialMediaDataCollector:
    def __init__(self, data_source="kafka", tweets_buffer=None):
        self.data_source = data_source.lower()
        self.tweets_buffer = tweets_buffer if tweets_buffer is not None else []
        if self.data_source not in ["twitter", "kafka"]:
            raise ValueError(f"Unsupported social media source: {self.data_source}")

    def collect_data(self, query="emergency OR help needed", max_results=10):
        """
        Récupère des tweets selon la source choisie.

        - Si source kafka, récupère dans tweets_buffer les derniers max_results tweets.
        - Sinon, raise NotImplementedError (ou API Twitter si tu veux garder l'ancien code).
        """
        if self.data_source == "kafka":
            logger.info(f"Collecting up to {max_results} tweets from Kafka buffer")
            # Récupérer les derniers max_results tweets
            return self.tweets_buffer[-max_results:]
        
        elif self.data_source == "twitter":
            # Ici tu pourrais garder l’ancienne implémentation avec requests.get(...)
            # ou lever une erreur pour indiquer que ce n’est plus supporté
            raise NotImplementedError("Direct Twitter API fetching is disabled when using Kafka stream.")

        else:
            raise ValueError(f"Unsupported data source: {self.data_source}")
