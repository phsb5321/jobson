import atexit
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_restx import Api, Resource, fields

from app.config import Config
from app.repositories.job_model_repository import JobRepository
from app.repositories.serp_api_repository import SerpApiRepository

app = Flask(__name__)
api = Api(app, version="1.0", title="JobSon API", description="A simple Job API")
ns = api.namespace("jobs", description="Job operations")

# Models for serialization
message_model = api.model(
    "Message", {"message": fields.String(description="A simple message")}
)

error_model = api.model(
    "Error", {"error": fields.String(description="An error message")}
)


def schedule_jobs():
    """Schedules job fetching and storage using a background scheduler."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        fetch_and_store_job_data,
        "cron",
        hour=0,
        minute=0,
        day="*/2",
        # next_run_time=datetime.now(),  # Start immediately upon server start
    )
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())


def fetch_and_store_job_data():
    """Fetches job data from SerpAPI and stores it in the database."""
    serp_repository = SerpApiRepository(Config.API_KEY)
    job_repo = JobRepository()

    for job_query in Config.JOB_QUERIES:
        for state in Config.BRAZILIAN_STATES:
            print(f"Fetching job data for {job_query} in {state} at {datetime.now()}")
            job_listings = serp_repository.process_job_data(job_query, state)
            job_repo.add_jobs(job_listings)

    print(f"Job data fetched and stored successfully at {datetime.now()}")


@ns.route("/")
class HelloWorld(Resource):
    @api.marshal_with(message_model)
    def get(self):
        """Returns a greeting indicating the service is running."""
        return {"message": "The JobSon service is up and running!"}


@ns.route("/trigger-fetch")
class TriggerFetch(Resource):
    @api.response(200, "Success", message_model)
    @api.response(500, "Failed", error_model)
    def post(self):
        """Manually triggers the fetching and storing of job data."""
        try:
            print(f"Manual job data fetch initiated at {datetime.now()}")
            fetch_and_store_job_data()
            return {"message": "Job data fetch initiated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500


if __name__ == "__main__":
    schedule_jobs()  # Schedule job fetching on application start
    app.run(host="0.0.0.0", port=3500)
