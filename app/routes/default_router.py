from typing import Dict, Tuple
from flask_restx import Namespace, Resource, fields
from app.repositories.job_data_repository import JobNormalizationRepository
from app.use_cases.job_fetcher import JobFetcher
from app.config import Config

# Define a namespace for job-related operations with a descriptive overview
ns = Namespace(
    "jobs", description="Operations related to job data fetching and normalization"
)

# Define serialization models for successful and error messages
message_model = ns.model(
    "SuccessMessage",
    {
        "message": fields.String(
            required=True, description="A descriptive success message"
        )
    },
)

error_model = ns.model(
    "ErrorMessage",
    {"error": fields.String(required=True, description="A descriptive error message")},
)

# Initialize necessary instances from other components of the application
job_fetcher = JobFetcher(Config.API_KEY, Config.JOB_QUERIES, Config.BRAZILIAN_STATES)
jobson_repo = JobNormalizationRepository()


@ns.route("/trigger-fetch")
class TriggerFetch(Resource):
    @ns.doc("trigger_job_fetch")
    @ns.response(200, "Job data fetch successfully initiated", message_model)
    @ns.response(500, "Internal Server Error", error_model)
    def post(self) -> Tuple[Dict[str, str], int]:
        """
        Triggers the job data fetch process.

        Manually initiates the process of fetching job data from external APIs or databases. This endpoint should be used with caution as it can trigger intensive data fetching and processing operations.
        """
        try:
            job_fetcher.fetch_and_store_job_data()
            return {"message": "Job data fetch initiated successfully"}, 200
        except Exception as e:
            ns.logger.error(f"Failed to initiate job data fetch: {e}")
            return {"error": str(e)}, 500


@ns.route("/normalize-csv")
class NormalizeCSV(Resource):
    @ns.doc("normalize_job_csv")
    @ns.response(
        200,
        "Normalization and CSV saving process successfully initiated",
        message_model,
    )
    @ns.response(500, "Internal Server Error", error_model)
    def get(self):
        """
        Triggers the normalization and saving of job data to a CSV file.

        Manually initiates the process of normalizing job data and saving it into a CSV file. This is useful for preparing data for further analysis or backup purposes.
        """
        try:
            jobson_repo.normalize_and_save_job_data()
            return {
                "message": "Normalization process initiated and CSV saved successfully"
            }, 200
        except Exception as e:
            ns.logger.error(f"Failed to initiate normalization and CSV saving: {e}")
            return {"error": str(e)}, 500
