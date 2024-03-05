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
        # Check for a cached response
        week_ago = datetime.datetime.utcnow() - datetime.timedelta(weeks=1)
        cached_response = self.mongo_client.db.api_responses.find_one(
            {"query": query, "state": state, "timestamp": {"$gte": week_ago}}
        )

        if cached_response:
            return cached_response[
                "data"
            ]  # Return the cached data if it exists and is recent

        # If no cached data or it's outdated, proceed to make a new request
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

        # Cache the new response data with a timestamp
        self.mongo_client.db.api_responses.replace_one(
            {"query": query, "state": state},
            {
                "query": query,
                "state": state,
                "data": response_data,
                "timestamp": datetime.datetime.utcnow(),
            },
            upsert=True,
        )

        # Process the data as before
        with MongoDBClient.get_instance() as mongo_client:
            jobs_collection = mongo_client.db.jobs
            highlights_collection = mongo_client.db.job_highlights

            for job in response_data["jobs_results"]:
                self.process_and_insert_job_data(
                    job, response_data, jobs_collection, highlights_collection
                )

        return response_data  # Return the new response data

    def fetch_and_store_job_data(self):
        """Fetches and stores job data from SerpAPI."""

        with ThreadPoolExecutor() as executor:
            for job_query in self.job_queries:
                for state in self.brazilian_states:
                    executor.submit(
                        self.serp_repository.process_job_data, job_query, state
                    )
        print(f"Job data fetched and stored successfully at {datetime.now()}")
