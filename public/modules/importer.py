# importer.py
import pandas as pd
import os


class DataImport:
    """
    A class for importing and cleaning job listing data from CSV files.
    """

    def __init__(self):
        """
        Initializes DataImport with the path to the directory containing data files.
        """
        self.data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "DATA")
        self.normalized_csv_filename = "FINAL.csv"

    def fetch_and_clean_data(self):
        """
        Reads data from a CSV file, cleans it, and returns a DataFrame.

        Returns:
        - A cleaned Pandas DataFrame containing job listings data.
        """
        data_file_path = os.path.join(self.data_dir, self.normalized_csv_filename)
        jobs_data = pd.read_csv(data_file_path)

        # Clean data
        jobs_data = jobs_data.dropna().reset_index(drop=True)
        jobs_data = self._clean_description_tokens(jobs_data)

        return jobs_data

    @staticmethod
    def _clean_description_tokens(df):
        """
        Cleans and processes the 'description_tokens' column in the DataFrame.

        Parameters:
        - df: DataFrame, job listings data including 'description_tokens' column.

        Returns:
        - DataFrame with processed 'description_tokens' column.
        """
        df.description_tokens = df.description_tokens.str.strip("[]").str.split(",")
        df.description_tokens = df.description_tokens.apply(
            lambda x: [i.strip().strip("'\"") for i in x]
        )
        return df
