import logging

logger = logging.getLogger(__name__)

class AllocationModel:
    def __init__(self):
        # Simulate available resources by region, including volunteers
        self.resources = {
            "downtown": {
                "ambulance": 3,
                "medical_team": 4,
                "rescue_boat": 1,
                "firefighters": 2,
                "data_specialist": 0,
                "manual_worker": 0
            },
            "northern area": {
                "ambulance": 1,
                "medical_team": 2,
                "rescue_boat": 2,
                "firefighters": 1,
                "data_specialist": 0,
                "manual_worker": 0
            },
            "unknown": {
                "ambulance": 2,
                "medical_team": 2,
                "rescue_boat": 1,
                "firefighters": 2,
                "data_specialist": 0,
                "manual_worker": 0
            }
        }

    def predict_allocation(self, extracted_data):
        location = extracted_data["location"]
        resources_needed = extracted_data["resources_needed"]
        urgency = extracted_data["urgency_level"]

        if location not in self.resources:
            logger.warning(f"Unknown location: {location}. Using default resource pool.")
            location = "unknown"

        available = self.resources[location]
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
        location = volunteer_data["location"]
        roles = volunteer_data["roles_offered"]

        if location not in self.resources:
            location = "unknown"
            logger.warning(f"Unknown volunteer location: using default pool.")

        for role in roles:
            if role not in self.resources[location]:
                self.resources[location][role] = 0
            self.resources[location][role] += 1
            logger.info(f"Registered 1 {role} volunteer in {location}.")
