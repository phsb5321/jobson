from flask import Flask
from flask_restx import Api
from app.config import Config
from app.routes.default_router import ns

app = Flask(__name__)
api = Api(
    app, version="1.0", title="JobSon API", description="A simple Job API", doc="/docs"
)
api.add_namespace(ns, path="/jobs")

if __name__ == "__main__":
    from app.use_cases.job_fetcher import JobFetcher

    job_fetcher = JobFetcher(
        Config.API_KEY, Config.JOB_QUERIES, Config.BRAZILIAN_STATES
    )
    job_fetcher.schedule_jobs()
    app.run(host="0.0.0.0", port=Config.PORT)
