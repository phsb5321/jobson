from pymongo import MongoClient, errors
from ..config import Config


class MongoDBClient:
    _instance = None

    @staticmethod
    def get_instance():
        if MongoDBClient._instance is None:
            MongoDBClient()
        return MongoDBClient._instance

    def __init__(self):
        if MongoDBClient._instance is not None:
            raise SingletonException("This class is a singleton!")
        else:
            MongoDBClient._instance = self
            self.client = MongoClient(Config.MONGO_URI)
            self.db = self.client["jobson"]  # Connects to the 'jobson' database
            self._ensure_setup()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def _ensure_setup(self):
        # This method ensures that all the necessary setup is done, such as creating collections and indexes
        self._ensure_collection_exists(
            "jobs", [("job_id", 1)], unique_indexes=["job_id"]
        )
        self._ensure_collection_exists(
            "job_highlights", [("highlight_id", 1)], unique_indexes=["highlight_id"]
        )
        self._ensure_collection_exists(
            "api_responses",
            [("query", 1), ("state", 1), ("timestamp", 1)],
            unique_indexes=["query", "state"],
        )

    def _ensure_collection_exists(
        self, collection_name, index_list, unique_indexes=None
    ):
        # Check if the collection exists
        if collection_name not in self.db.list_collection_names():
            # Create the collection since it does not exist
            self.db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")

        collection = self.db[collection_name]

        # Setup indexes
        for index in index_list:
            try:
                if index[0] in unique_indexes:
                    collection.create_index([index], unique=True)
                else:
                    collection.create_index([index])
            except errors.OperationFailure as e:
                print(f"Failed to create index on {index[0]}: {e}")


class SingletonException(Exception):
    """Exception raised when a second instance of a Singleton class is created."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
