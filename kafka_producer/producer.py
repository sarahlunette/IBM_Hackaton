import json
import time
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable

KAFKA_TOPIC = 'tweets_topic'
KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'  # nom du service kafka dans docker-compose

def load_tweets(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        tweets = json.load(f)
    return tweets

def create_producer_with_retry(retries=5, delay=5):
    for i in range(retries):
        try:
            producer = KafkaProducer(bootstrap_servers='kafka:9092')
            return producer
        except NoBrokersAvailable:
            print(f"Kafka broker not available, retry {i+1}/{retries} in {delay}s...")
            time.sleep(delay)
    raise RuntimeError("Kafka broker not available after retries")

def main():
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    tweets = load_tweets('/data/simulated_tweets_with_geo.json')
    print(f"Streaming {len(tweets)} tweets to Kafka topic '{KAFKA_TOPIC}'")

    for tweet in tweets:
        producer.send(KAFKA_TOPIC, tweet)
        print(f"Sent tweet: {tweet.get('id', 'unknown')}")
        time.sleep(1)  # pause 1s entre chaque tweet

    producer.flush()
    producer.close()

if __name__ == "__main__":
    main()
