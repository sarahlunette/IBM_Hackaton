from fastapi import FastAPI
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.data_collector import SocialMediaDataCollector
from services.resource_allocator import ResourceAllocator
from services.resource_dispatcher import ResourceDispatcher
from logging_config import setup_logging

setup_logging()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Automated Resource Allocation API"}

@app.get("/collect")
def collect_tweets(query: str = "flood OR earthquake OR urgent"):
    collector = SocialMediaDataCollector()
    tweets = collector.collect_data(query=query)
    return {"tweets": tweets}

@app.post("/allocate")
def allocate_resources(location: str = "default region"):
    allocator = ResourceAllocator()
    allocation_results = allocator.analyze_and_allocate(location_filter=location)
    return {"allocations": allocation_results}