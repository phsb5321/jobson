from pymongo import MongoClient, errors
from ..config import Config
from pandas import DataFrame
import os


class MongoDBClient:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoDBClient._instance is None:
            MongoDBClient._instance = MongoDBClient()
        return MongoDBClient._instance

    def __init__(self):
        if MongoDBClient._instance is not None:
            raise SingletonException("This class is a singleton!")
        else:
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client["jobson"]  # Connects to the 'jobson' database
            self._ensure_setup()

    def _ensure_setup(self):
        # This method ensures that all the necessary setup is done, such as creating collections and indexes
        self._ensure_collection_exists(
            "jobs", [("job_id", 1)], unique_indexes=["job_id"]
        )
        self._ensure_collection_exists("job_highlights", [])

    def _ensure_collection_exists(
        self, collection_name, index_list, unique_indexes=None
    ):
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")

        collection = self.db[collection_name]
        for index in index_list:
            try:
                if unique_indexes and index[0] in unique_indexes:
                    collection.create_index([index], unique=True)
                else:
                    collection.create_index([index])
            except errors.OperationFailure as e:
                print(f"Failed to create index on {index[0]}: {e}")

    def fetch_jobs_data(self) -> DataFrame:
        jobs_cursor = self.db.jobs.find({})
        df = DataFrame(list(jobs_cursor))
        return df

    def save_jobs_data_to_csv(self, df: DataFrame, file_path: str):
        """Saves the given DataFrame to a CSV file."""
        # Ensure the directory exists where the file will be saved
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        print(f"Saved job listings data to CSV at {file_path}.")


class SingletonException(Exception):
    """Exception raised when a second instance of a Singleton class is created."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
