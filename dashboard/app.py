import streamlit as st
from resources.utilities import extract_needs_from_text, extract_volunteer_offers
from services.allocation import AllocationModel
from services.social_media_collector import SocialMediaDataCollector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Emergency Resource Allocator", layout="wide")

st.title("🚨 Emergency Resource Allocator")

model = AllocationModel()
collector = SocialMediaDataCollector(data_source="twitter")

st.sidebar.header("Social Media Data Collection")
query = st.sidebar.text_input("Search Query", value="flood OR earthquake OR urgent")
max_results = st.sidebar.slider("Max Tweets to Fetch", min_value=5, max_value=50, value=10)

if st.sidebar.button("Fetch and Process Social Media Data"):
    st.info("Collecting tweets...")
    tweets = collector.collect_data(query=query, max_results=max_results)
    st.write(f"Fetched {len(tweets)} tweets")

    # Process tweets for needs and volunteers
    needs_count = 0
    volunteers_count = 0

    for tweet in tweets:
        needs = extract_needs_from_text(tweet)
        if needs:
            needs_count += 1
            allocation = model.predict_allocation(needs)
            st.write(f"Needs detected in tweet: {tweet}")
            st.write(f"Requested: {needs['resources_needed']} | Urgency: {needs['urgency_level']} | Location: {needs['location']}")
            st.write(f"Allocation: {allocation}")
            st.markdown("---")

        volunteers = extract_volunteer_offers(tweet)
        if volunteers:
            volunteers_count += 1
            model.register_volunteers(volunteers)
            st.write(f"Volunteer offer detected in tweet: {tweet}")
            st.write(f"Offered roles: {volunteers['roles_offered']} | Location: {volunteers['location']}")
            st.markdown("---")

    st.success(f"Processed {needs_count} need(s) and registered {volunteers_count} volunteer offer(s).")

st.header("Current Available Resources by Location")

for location, resources in model.resources.items():
    st.subheader(f"{location.capitalize()}")
    for resource, count in resources.items():
        st.write(f"- {resource}: {count}")
