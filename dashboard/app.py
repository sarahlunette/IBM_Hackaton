import streamlit as st
from models.allocation_model import AllocationModel

st.title("Emergency Resource Allocator")
urgency = st.selectbox("Urgency", ["low", "medium", "high"])
location = st.text_input("Location", "downtown")
needs = st.multiselect("Resources Needed", ["ambulance", "medical_team", "rescue_team"])

if st.button("Predict Allocation"):
    model = AllocationModel()
    result = model.predict_allocation({
        "urgency_level": urgency,
        "location": location,
        "resources_needed": needs
    })
    st.success(result)
