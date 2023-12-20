# %%
import json
import os

import pandas as pd
import requests

# %%
# Constants
API_KEY = "API_CODE_HERE"
BASE_URL = "https://serpapi.com/search.json"
DATA_DIR = "DATA"  # Centralizing the data directory for easy modification
CSV_FILE_PATH = (
    "/mnt/data/job_data.csv"  # Centralizing the csv file path for easy future changes
)

# %%
# Helper functions

def get_job_data(query, location, api_key=API_KEY):
    """Fetches job data from the API based on the query and location.

    Args:
        query (str): The job title to search for.
        location (str): The location where the job is based.
        api_key (str): The API key for authentication. Defaults to a constant API_KEY.

    Returns:
        dict or None: The JSON response parsed into a dictionary if the call was successful, otherwise None.
    """
    params = {
        "engine": "google_jobs",
        "q": query,
        "location": location,
        "api_key": api_key,
    }
    response = requests.get(BASE_URL, params=params)
    return response.json() if response.ok else None


def save_data_as_json(data, filename, directory=DATA_DIR):
    """Saves provided data as a JSON file in the given directory with the specified filename.

    Args:
        data (dict): The data to save as JSON.
        filename (str): The name of the file to create.
        directory (str): The directory where the file will be saved. Defaults to a `DATA_DIR`.

    Side-effects:
        Creates a directory and writes a file to the filesystem.
    """
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)


def extract_job_info(job):
    """Extracts relevant information from a single job posting.

    Args:
        job (dict): The job posting data.

    Returns:
        dict: A dictionary containing structured job information.
    """
    extensions = job.get("detected_extensions", {})
    return {
        "Job Title": job.get("title", ""),
        "Company Name": job.get("company_name", ""),
        "Location": job.get("location", "").strip(),
        "Description": job.get("description", ""),
        "Salary": extensions.get("salary", ""),
        "Job Type": extensions.get("schedule_type", ""),
        "Date Posted": extensions.get("posted_at", ""),
        "Benefits": ", ".join(job.get("extensions", [])),
        "Application Link": job.get("apply_link", {}).get("link", ""),
        "Related Links": ", ".join(
            link.get("link", "") for link in job.get("related_links", [])
        ),
        "Job ID": job.get("job_id", ""),
    }


def get_and_display_job_data(search_query, search_location):
    """Fetches job data based on search parameters and displays a part of the response.

    Args:
        search_query (str): The job title to search for.
        search_location (str): The location of the job.

    Returns:
        str: The identification of the saved CSV file or an error message.
    """
    job_data = get_job_data(search_query, search_location)
    print(
        job_data["jobs_results"][:2]
        if job_data and "jobs_results" in job_data
        else "No data or invalid API key"
    )
    return job_data


def save_job_data_to_csv(job_data, csv_file_path):
    """Saves job data to a CSV file with a given path.

    Args:
        job_data (dict): A dictionary containing job data.
        csv_file_path (str): Where the CSV file will be stored.

    Side-effects:
        Creates a CSV file to the filesystem.
    """
    job_listings = [extract_job_info(job) for job in job_data.get("jobs_results", [])]
    df = pd.DataFrame(job_listings)
    df.to_csv(csv_file_path, index=False)


# %%
# This code block is used to perform the operations

# Example search - Replace with actual search query and location
search_query = "Software Engineer"  # Your desired job title
search_location = "San Francisco, CA"  # Your desired location

# Get data and display part of it
job_data = get_and_display_job_data(search_query, search_location)

# Save to JSON if data is available
if job_data:
    save_data_as_json(job_data, "job_data.json")

    # Save to CSV and return path
    save_job_data_to_csv(job_data, CSV_FILE_PATH)
    print(f"CSV file saved at {CSV_FILE_PATH}")
else:
    print("No data to save or invalid API key")
