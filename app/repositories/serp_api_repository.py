import datetime
import uuid

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

    def process_and_insert_job_data(
        self, job, response_data, jobs_collection, highlights_collection
    ):
        """
        Process and insert job data into the database, checking for duplicates.
        """
        # Create a unique identifier for the job
        job_id = f"{job['title']}-{job['company_name']}-{job['location']}"
        existing_job = jobs_collection.find_one({"job_id": job_id})

        if not existing_job:
            job_highlights = job.get("job_highlights", [])
            highlight_id = str(uuid.uuid4())  # Generate a unique highlight_id

            if job_highlights:  # Check if job_highlights is not empty
                highlights_collection.insert_one(
                    {"highlight_id": highlight_id, "highlights": job_highlights}
                )

            job_data = {
                **job,
                "job_id": job_id,
                "search_metadata": response_data["search_metadata"],
                "search_parameters": response_data["search_parameters"],
                "job_highlights_id": highlight_id,
            }
            jobs_collection.insert_one(job_data)

    def fetch_job_data(self, query: str, state: str) -> Optional[dict]:
        """
        Fetches job data, utilizing cached data if available and relevant.
        """
        try:
            # Check for a cached response
            week_ago = datetime.datetime.utcnow() - datetime.timedelta(weeks=1)
            cached_response = self.mongo_client.db.api_responses.find_one(
                {"query": query, "state": state, "timestamp": {"$gte": week_ago}}
            )

            if cached_response:
                response_data = cached_response["data"]
            else:
                params = {
                    "engine": "google_jobs",
                    "q": query,
                    "l": state + ", Brazil",
                    "api_key": self.api_key,
                }
                response = requests.get(self.base_url, params=params)
                if not response.ok:
                    print(f"Error fetching job data: {response.text}")
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

            # Process the data (both cached and new responses)
            jobs_collection = self.mongo_client.db.jobs
            highlights_collection = self.mongo_client.db.job_highlights
            for job in response_data.get("jobs_results", []):
                try:
                    self.process_and_insert_job_data(
                        job, response_data, jobs_collection, highlights_collection
                    )
                    print(
                        f"Job data processed and stored successfully at {datetime.datetime.now()}"
                    )
                except Exception as e:
                    print(f"Error processing and storing job data: {e}")
        except Exception as e:
            print(f"An error occurred during job data fetch and processing: {e}")
            return None

        return response_data

    def fetch_and_store_job_data(self, job_queries, brazilian_states):
        """
        Orchestrates the fetching and storing of job data.
        """
        for job_query in job_queries:
            for state in brazilian_states:
                self.fetch_job_data(job_query, state)
        print(f"Job data fetched and stored successfully at {datetime.datetime.now()}")
