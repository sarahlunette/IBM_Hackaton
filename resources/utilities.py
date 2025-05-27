import re

def extract_needs_from_text(text: str):
    urgency_keywords = ["asap", "urgent", "emergency", "immediately", "critical", "massive"]
    resource_keywords = {
        "ambulance": ["ambulance", "paramedic", "emergency vehicle"],
        "medical_team": ["doctor", "nurse", "medic", "paramedic"],
        "rescue_boat": ["rescue boat", "raft", "flood boat"],
        "firefighters": ["firefighter", "fire crew"]
    }

    urgency_level = "medium"
    for word in urgency_keywords:
        if word in text.lower():
            urgency_level = "high"
            break

    detected_resources = []
    for resource, synonyms in resource_keywords.items():
        for synonym in synonyms:
            if synonym in text.lower():
                detected_resources.append(resource)
                break

    location = "unknown"
    if "downtown" in text.lower():
        location = "downtown"
    elif "northern" in text.lower():
        location = "northern area"

    if not detected_resources:
        return None

    return {
        "urgency_level": urgency_level,
        "location": location,
        "resources_needed": list(set(detected_resources))
    }

def extract_volunteer_offers(text: str):
    volunteer_keywords = {
        "data_specialist": ["data analyst", "data scientist", "data engineer", "data team"],
        "manual_worker": ["volunteer", "manual labor", "cleanup", "clean debris", "helping hand"]
    }
    # Implement extraction logic as needed
