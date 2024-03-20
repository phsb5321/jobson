from flask import Flask
from flask_restx import Api
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# Import local modules
from app.repositories.job_data_repository import JobNormalizationRepository
from app.use_cases.job_fetcher import JobFetcher
from app.config import Config
from app.routes.default_router import ns

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="JobSon API",
    description="A simple Job API for fetching and normalizing job listings.",
    doc="/docs",
)

# Register namespace with the Flask-RESTx API
api.add_namespace(ns, path="/jobs")

# Initialize repository and use case instances
jobson_repo = JobNormalizationRepository()
job_fetcher = JobFetcher(Config.API_KEY, Config.JOB_QUERIES, Config.BRAZILIAN_STATES)


def normalize_job_data():
    """Scheduled task to fetch and normalize job data."""
    jobson_repo.normalize_and_save_job_data()


def fetch_job_data():
    """Scheduled task to fetch job data from external sources."""
    job_fetcher.fetch_and_store_job_data()


def schedule_jobs():
    """Sets up and starts the scheduler with defined jobs."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_job_data, "cron", day="*/2", hour=0, minute=0, misfire_grace_time=900
    )
    scheduler.add_job(
        normalize_job_data, "cron", day="*/2", hour=1, minute=0, misfire_grace_time=900
    )
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    schedule_jobs()
    port = Config.PORT if Config.PORT else 5000
    app.run(host="0.0.0.0", port=port, debug=True)
