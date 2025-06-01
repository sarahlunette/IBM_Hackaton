import streamlit as st
import os
import sys
import threading
import time
import logging
import json
from kafka import KafkaConsumer

# Pour que l'app trouve bien tes modules custom
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from resources.utilities import extract_needs_from_text, extract_volunteer_offers
from models.allocation_model import AllocationModel
from services.data_collector import SocialMediaDataCollector
from models.llm_allocator import LLMResourceAllocator  # <-- NEW IMPORT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Emergency Resource Allocator", layout="wide")
st.title("🚨 Emergency Resource Allocator")

# Init model + LLM allocator
model = AllocationModel()
llm_allocator = LLMResourceAllocator()

# Buffer partagé pour stocker les tweets Kafka reçus
tweets_buffer = []

# Thread Kafka consumer
def kafka_consumer_thread():
    consumer = KafkaConsumer(
        'tweets_topic',
        bootstrap_servers='kafka:9092',    # docker-compose hostname
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='streamlit-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    logger.info("Kafka consumer started, waiting for messages...")
    for msg in consumer:
        tweets_buffer.append(msg.value)
        logger.info(f"Received tweet ID: {msg.value.get('id', 'unknown')}")

# Démarrer le thread consommateur kafka en daemon
threading.Thread(target=kafka_consumer_thread, daemon=True).start()

# Sidebar pour options (gardées pour info, mais on ne fetch plus ici)
st.sidebar.header("Social Media Data Collection (via Kafka stream)")
max_display = st.sidebar.slider("Max tweets to display/process", min_value=5, max_value=50, value=10)

# Main interface
st.header("Tweets reçus via Kafka (en temps réel)")

# Bouton pour recharger / traiter les tweets en buffer
if st.button("Traiter les tweets reçus"):
    collector = SocialMediaDataCollector(data_source="kafka", tweets_buffer=tweets_buffer)
    # Récupérer les derniers tweets depuis Kafka via la classe
    recent_tweets = collector.collect_data(max_results=max_display)

    needs_count = 0
    volunteers_count = 0

    for tweet in recent_tweets:
        needs = extract_needs_from_text(tweet)
        if needs:
            needs_count += 1

            llm_result = llm_allocator.allocate_with_llm([tweet])
            st.write(f"**Tweet:** {tweet}")
            st.write(f"**LLM Crisis Summary:** {llm_result['summary']}")
            st.write(f"**LLM Suggested Allocation Plan:** {llm_result['plan']}")
            st.markdown("---")

        volunteers = extract_volunteer_offers(tweet)
        if volunteers:
            volunteers_count += 1
            model.register_volunteers(volunteers)

            needs_text = ", ".join(volunteers.get("roles_offered", []))
            location = volunteers.get("location", "unknown")
            llm_response = llm_allocator.llm.generate_call_to_action(needs_text, location)
            st.write(f"**Volunteer Tweet:** {tweet}")
            st.write(f"**LLM Response to Volunteer:** {llm_response}")
            st.markdown("---")

    st.success(f"Processed {needs_count} need(s) and registered {volunteers_count} volunteer offer(s).")

# Afficher ressources courantes
st.header("Current Available Resources by Location")
for location, resources in model.resources.items():
    st.subheader(f"{location.capitalize()}")
    for resource, count in resources.items():
        st.write(f"- {resource}: {count}")
