# app/database/database_manager.py
"""This module initializes database configurations and provides a session manager."""

from contextlib import contextmanager

from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import Config

engine = create_engine(Config.DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client.jobson  # 'jobson' is the database name

    def save_raw_response(self, collection_name, data):
        collection = self.db[collection_name]
        collection.insert_one(data)
