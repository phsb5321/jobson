# file: repositories/job_normalization_repository.py

import pandas as pd
import numpy as np
import re
import os
from ..config import Config
from ..database.mongo_client import MongoDBClient


class JobNormalizationRepository:
    """A repository for normalizing and managing job listings data."""

    def __init__(self):
        """
        Initializes the JobNormalizationRepository with necessary configuration.
        """
        self.mongo_client = MongoDBClient.get_instance()
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "DATA")
        self.normalized_csv_filename = "FINAL.csv"
        self.normalized_csv_path = os.path.join(
            self.data_dir, self.normalized_csv_filename
        )

    def normalize_and_save_job_data(self):
        """Fetches, normalizes, and saves job data."""
        # Ensure data directory exists
        os.makedirs(self.data_dir, exist_ok=True)

        # Fetch job listings data from MongoDB
        jobson_df = self.mongo_client.fetch_jobs_data()
        self.mongo_client.save_jobs_data_to_csv(
            jobson_df, os.path.join(self.data_dir, "ORIGINAL.csv")
        )

        # Apply normalization steps
        jobson_df = self.normalize_data(jobson_df)

        # Save normalized data to CSV
        self.save_data_to_csv(jobson_df, self.normalized_csv_path)

    def normalize_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies normalization procedures to the DataFrame."""
        df[["min_salary", "max_salary"]] = (
            df["description"]
            .apply(lambda desc: self.extract_and_convert_salary(desc))
            .tolist()
        )

        df["isHomeOffice"] = df["description"].str.contains(
            self.generate_pattern(Config.REMOTE_WORK_TERMS), case=False, na=False
        )

        df["description_tokens"] = df["description"].apply(self.extract_skills)

        # Apply contract status patterns
        contract_status_patterns = self.get_contract_status_patterns()
        for status, pattern in contract_status_patterns.items():
            df[status] = df["description"].str.contains(pattern, case=False, na=False)

        return df[
            [
                "title",
                "description",
                "isHomeOffice",
                "description_tokens",
                "min_salary",
                "max_salary",
            ]
            + list(contract_status_patterns.keys())
        ]

    def extract_and_convert_salary(self, description: str) -> tuple:
        """Extracts and converts salary details from the job description."""
        salary_pattern = r"\$\d+K|\$\d+(?:,\d+)?(?: - \$\d+(?:,\d+)?)?"
        salaries = re.findall(
            salary_pattern, description.replace(",", "").replace("$", "")
        )

        if not salaries:
            return np.nan, np.nan
        salaries = [float(salary.replace("K", "000")) for salary in salaries]
        # Return the minimum and maximum salaries or 0 if only one salary is found
        return tuple(salaries) if len(salaries) == 2 else (salaries[0], 0)

    def extract_skills(self, description: str) -> list:
        """Extracts skills based on Config.SKILL_LIST from the job description."""
        pattern = self.generate_pattern(Config.SKILL_LIST)
        return [
            skill
            for skill in Config.SKILL_LIST
            if re.search(pattern, description, re.IGNORECASE)
        ]

    def generate_pattern(self, terms: list) -> str:
        """Generates a regex pattern from a list of terms."""
        return "|".join([f"\\b{re.escape(term)}\\b" for term in terms])

    def get_contract_status_patterns(self):
        """Defines regex patterns for different contract statuses."""
        return {
            "isPJ": r"\bPJ\b|\bPessoa Jurídica\b",
            "isCLT": r"\bCLT\b",
            "isInternship": r"\bInternship\b|\bEstágio\b",
            "isFullTime": r"\bFull[-]?Time\b",
            "isHalfTime": r"\bPart[-]?Time\b|\bMeio Período\b",
        }

    def save_data_to_csv(self, df: pd.DataFrame, file_path: str):
        """Saves the DataFrame to the specified CSV file path."""
        # Delete the description column
        df = df.drop(columns=["description"])
        print(f"Saving normalized job data to {file_path}.")
        df.to_csv(file_path, index=False)
