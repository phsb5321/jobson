from pymongo import MongoClient
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
            self.db = self.client.jobson

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


class SingletonException(Exception):
    """Exception raised when a second instance of a Singleton class is created."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
