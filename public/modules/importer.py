# File: importer.py
import os
import pandas as pd


class DataImport:
    """
    Import and clean data from a local CSV file.
    """

    def __init__(self):
        # Define the directory path where the data file is located
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "DATA")
        self.normalized_csv_filename = "FINAL.csv"

    def fetch_and_clean_data(self):
        # Construct the full path to the CSV file
        data_file_path = os.path.join(self.data_dir, self.normalized_csv_filename)

        # Read data from the CSV file
        jobs_data = pd.read_csv(data_file_path).replace("'", "", regex=True)
        jobs_data = jobs_data.drop(
            labels=["Unnamed: 0", "index"], axis=1, errors="ignore"
        )
        jobs_data.description_tokens = jobs_data.description_tokens.str.strip(
            "[]"
        ).str.split(",")
        jobs_data.description_tokens = jobs_data.description_tokens.apply(
            lambda row: [x.strip(" ") for x in row]
        )

        return jobs_data
