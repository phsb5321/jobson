import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import requests

from ..config import Config
from ..database.mongo_client import MongoDBClient


class SerpApiRepository:
    """A repository for fetching and processing job data from Serp API."""

    def __init__(self, api_key: str, base_url: str = Config.BASE_URL):
        """
        Initializes the SerpApiRepository with necessary configuration.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.mongo_client = MongoDBClient.get_instance()

    from bson.objectid import ObjectId

    def process_and_insert_job_data(
        self, job, response_data, jobs_collection, highlights_collection
    ):
        # Insert job highlights into its own collection
        highlight_id = highlights_collection.insert_one(
            job.get("job_highlights", {})
        ).inserted_id

        # Insert the job into the jobs collection with a reference to the highlight
        job_data = job.copy()
        job_data.update(
            {
                "search_metadata": response_data["search_metadata"],
                "search_parameters": response_data["search_parameters"],
                "job_highlights_id": highlight_id,
            }
        )
        jobs_collection.insert_one(job_data)

    def fetch_job_data(self, query: str, state: str) -> Optional[dict]:
        """Fetches job data from the API for a given query and state."""
        params = {
            "engine": "google_jobs",
            "q": query,
            "l": state + ", Brazil",
            "api_key": self.api_key,
        }
        response = requests.get(self.base_url, params=params)
        if not response.ok:
            return None

        response_data = response.json()
        with MongoDBClient.get_instance() as mongo_client:
            jobs_collection = mongo_client.db.jobs
            highlights_collection = mongo_client.db.job_highlights

            for job in response_data["jobs_results"]:
                self.process_and_insert_job_data(
                    job, response_data, jobs_collection, highlights_collection
                )
            return mongo_client.db.jobs.find()

    def fetch_and_store_job_data(self):
        """Fetches and stores job data from SerpAPI."""

        with ThreadPoolExecutor() as executor:
            for job_query in self.job_queries:
                for state in self.brazilian_states:
                    executor.submit(
                        self.serp_repository.process_job_data, job_query, state
                    )
        print(f"Job data fetched and stored successfully at {datetime.now()}")
