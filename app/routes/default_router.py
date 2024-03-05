from typing import Dict, Tuple
from flask_restx import Namespace, Resource, fields
from ..use_cases.job_fetcher import JobFetcher
from ..config import Config

ns = Namespace("", description="Job operations")

# Serialization models
message_model = ns.model(
    "Message", {"message": fields.String(description="A simple message")}
)
error_model = ns.model(
    "Error", {"error": fields.String(description="An error message")}
)

job_fetcher = JobFetcher(Config.API_KEY, Config.JOB_QUERIES, Config.BRAZILIAN_STATES)


@ns.route("/")
class HelloWorld(Resource):
    @ns.marshal_with(message_model)
    def get(self) -> Dict[str, str]:
        """Endpoint to verify service is running."""
        return {"message": "The JobSon service is up and running!"}


@ns.route("/trigger-fetch")
class TriggerFetch(Resource):
    @ns.response(200, "Success", message_model)
    @ns.response(500, "Failed", error_model)
    def post(self) -> Tuple[Dict[str, str], int]:
        """Endpoint to manually trigger job data fetch."""
        try:
            job_fetcher.fetch_and_store_job_data()
            return {"message": "Job data fetch initiated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500
