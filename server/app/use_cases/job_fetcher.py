import atexit
from concurrent.futures import Future, ThreadPoolExecutor
from datetime import datetime
from typing import Any, List
from apscheduler.schedulers.background import BackgroundScheduler
from ..repositories.serp_api_repository import SerpApiRepository


class JobFetcher:
    def __init__(
        self, api_key: str, job_queries: List[str], brazilian_states: List[str]
    ) -> None:
        self.api_key: str = api_key
        self.job_queries: List[str] = job_queries
        self.brazilian_states: List[str] = brazilian_states
        self.serp_repository: SerpApiRepository = SerpApiRepository(api_key)

    def schedule_jobs(self) -> None:
        """Schedules automatic job data fetch."""
        scheduler: BackgroundScheduler = BackgroundScheduler()
        scheduler.add_job(
            self.fetch_and_store_job_data, "cron", hour=0, minute=0, day="*/2"
        )
        scheduler.start()
        atexit.register(lambda: scheduler.shutdown())

    def fetch_and_store_job_data(self) -> None:
        """Fetches and stores job data from SerpAPI."""

        with ThreadPoolExecutor() as executor:
            futures: List[Future[Any]] = []
            for job_query in self.job_queries:
                for state in self.brazilian_states:
                    future: Future[Any] = executor.submit(
                        self.serp_repository.fetch_job_data, job_query, state
                    )
                    futures.append(future)

        for future in futures:
            future.result()

        print(f"Job data fetched and stored successfully at {datetime.now()}")
