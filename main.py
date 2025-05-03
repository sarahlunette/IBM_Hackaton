from models.allocation_model import AllocationModel
from resources.resource_dispatcher import ResourceDispatcher


def main():
    sample_needs = {
        "urgency_level": 9,
        "location": "Area A",
        "resources_needed": ["ambulance", "medical_team"]
    }

    model = AllocationModel()
    allocation = model.predict_allocation(sample_needs)

    print("Predicted Allocation:", allocation)

    dispatcher = ResourceDispatcher(allocation)
    dispatcher.dispatch_resources()


if __name__ == "__main__":
    main()