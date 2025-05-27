import json
import time
import os
import sys
sys.path.append(os.abspath(os.path.join(os.path.dirname(__file__), '..')))
from kafka import KafkaProducer

KAFKA_TOPIC = 'tweets_topic'
KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'  # nom du service kafka dans docker-compose

def load_tweets(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        tweets = json.load(f)
    return tweets

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
