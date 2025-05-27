import pandas as pd
import logging

logger = logging.getLogger(__name__)

class AllocationModel:
    def __init__(self, csv_path="data/resources.csv"):
        self.resources = self.load_resources_from_csv(csv_path)

    def load_resources_from_csv(self, path):
        try:
            df = pd.read_csv(path)
            df.fillna(0, inplace=True)

            resource_dict = {}
            for _, row in df.iterrows():
                location = row['location'].strip().lower()
                resource_dict[location] = {
                    "ambulance": int(row.get("ambulance", 0)),
                    "medical_team": int(row.get("medical_team", 0)),
                    "rescue_boat": int(row.get("rescue_boat", 0)),
                    "firefighters": int(row.get("firefighters", 0)),
                    "data_specialist": int(row.get("data_specialist", 0)),
                    "manual_worker": int(row.get("manual_worker", 0)),
                }
            return resource_dict

        except Exception as e:
            logger.error(f"Failed to load resources from CSV: {e}")
            return {}

    def predict_allocation(self, extracted_data):
        location = extracted_data["location"].strip().lower()
        resources_needed = extracted_data["resources_needed"]
        urgency = extracted_data["urgency_level"]

        if location not in self.resources:
            logger.warning(f"Unknown location: {location}. Using default resource pool.")
            location = "unknown"

        available = self.resources.get(location, {})
        allocation = {}

        for resource in resources_needed:
            if resource in available and available[resource] > 0:
                count = 2 if urgency == "high" else 1
                allocated = min(count, available[resource])
                allocation[resource] = allocated
                self.resources[location][resource] -= allocated
                logger.info(f"Allocated {allocated} {resource}(s) to {location}.")
            else:
                logger.warning(f"{resource} not available in {location}.")
                allocation[resource] = 0

        return allocation

    def register_volunteers(self, volunteer_data):
        location = volunteer_data["location"].strip().lower()
        roles = volunteer_data["roles_offered"]

        if location not in self.resources:
            self.resources[location] = {}

        for role in roles:
            if role not in self.resources[location]:
                self.resources[location][role] = 0
            self.resources[location][role] += 1
            logger.info(f"Registered volunteer for {role} in {location}.")
