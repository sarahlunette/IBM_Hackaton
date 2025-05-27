import json
from datetime import datetime, timedelta
import random
import uuid

# Sample locations with coordinates
locations = {
    "downtown": {"coordinates": [4.3517, 50.8503]},
    "northern area": {"coordinates": [4.3600, 50.8700]},
    "southern area": {"coordinates": [4.3400, 50.8300]},
    "central park": {"coordinates": [4.3550, 50.8450]},
    "riverbank": {"coordinates": [4.3450, 50.8550]},
}

# Sample tweet messages
messages = [
    "Urgent help needed in downtown, major flooding!",
    "Rescue boats required immediately at northern area!",
    "We need paramedics in southern area, situation is critical!",
    "Can someone send firefighters to the riverbank?",
    "Downtown is in chaos, people are injured and stuck!",
    "Ambulance required asap near central park!",
    "Multiple injuries reported at the northern area. Send help!",
    "Emergency situation developing in the southern area!",
    "Floodwaters rising quickly in downtown, urgent response needed!",
    "We are trapped and need rescue near the riverbank!",
]

# Generate 50 tweets
tweets = []
base_time = datetime.utcnow()

for i in range(50):
    message = random.choice(messages)
    location_name = random.choice(list(locations.keys()))
    coordinates = locations[location_name]["coordinates"]
    
    tweet = {
        "id": str(uuid.uuid4()),
        "text": message,
        "created_at": (base_time - timedelta(minutes=i)).isoformat() + "Z",
        "author_id": str(random.randint(1000, 9999)),
        "geo": {
            "coordinates": {
                "type": "Point",
                "coordinates": coordinates
            },
            "place": location_name
        },
        "lang": "en"
    }
    tweets.append(tweet)

# Save to JSON file
with open("simulated_tweets_with_geo.json", "w") as f:
    json.dump({"data": tweets}, f, indent=2)
