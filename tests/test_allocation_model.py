import pytest
import pandas as pd
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.allocation_model import AllocationModel

# ---- SETUP ----
TEST_CSV_PATH = "tests/mock_resources.csv"

# Create a mock CSV for testing
@pytest.fixture(scope="module", autouse=True)
def mock_csv_file():
    df = pd.DataFrame({
        "location": ["downtown", "northern area", "unknown"],
        "ambulance": [3, 1, 2],
        "medical_team": [4, 2, 2],
        "rescue_boat": [1, 2, 1],
        "firefighters": [2, 1, 2],
        "data_specialist": [0, 0, 0],
        "manual_worker": [0, 0, 0],
    })
    df.to_csv(TEST_CSV_PATH, index=False)
    yield
    os.remove(TEST_CSV_PATH)

# ---- TESTS ----

def test_load_resources():
    model = AllocationModel(csv_path=TEST_CSV_PATH)
    assert "downtown" in model.resources
    assert model.resources["downtown"]["ambulance"] == 3
    assert model.resources["northern area"]["rescue_boat"] == 2

def test_predict_allocation_known_location():
    model = AllocationModel(csv_path=TEST_CSV_PATH)
    extracted_data = {
        "location": "downtown",
        "resources_needed": ["ambulance", "medical_team"],
        "urgency_level": "high"
    }
    result = model.predict_allocation(extracted_data)
    assert result["ambulance"] == 2
    assert result["medical_team"] == 2
    assert model.resources["downtown"]["ambulance"] == 1  # Updated after allocation

def test_predict_allocation_unknown_location():
    model = AllocationModel(csv_path=TEST_CSV_PATH)
    extracted_data = {
        "location": "nonexistent place",
        "resources_needed": ["firefighters"],
        "urgency_level": "medium"
    }
    result = model.predict_allocation(extracted_data)
    assert result["firefighters"] in [1, 2, 0]  # Based on 'unknown' pool

def test_predict_allocation_no_available_resource():
    model = AllocationModel(csv_path=TEST_CSV_PATH)
    extracted_data = {
        "location": "northern area",
        "resources_needed": ["data_specialist"],
        "urgency_level": "high"
    }
    result = model.predict_allocation(extracted_data)
    assert result["data_specialist"] == 0
