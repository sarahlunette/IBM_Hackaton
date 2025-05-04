# main.py

from models.allocation_model import AllocationModel

def main():
    needs_data = {
        "urgency_level": "high",
        "location": "downtown area",
        "resources_needed": ["ambulance", "medical_team"]
    }

    allocation_model = AllocationModel()
    prediction = allocation_model.predict_allocation(needs_data)

    print("Suggested Allocation:", prediction)

if __name__ == "__main__":
    main()

