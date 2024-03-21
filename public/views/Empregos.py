# Empregos.py
from pandas import Series
import streamlit as st
from modules.formater import Title
from modules.importer import DataImport


def load_view():
    Title.display("💸 Empregos")  # Set title for the view
    jobs_data = DataImport().fetch_and_clean_data()

    # Print the jobs_data shape
    print(jobs_data.shape)

    # Ensure jobs_data isn't empty before proceeds
    if jobs_data.empty:
        st.error("No job data available.")
        return

    # Ensure 'description_tokens' column exists and has data
    if (
        "description_tokens" not in jobs_data.columns
        or jobs_data["description_tokens"].empty
    ):
        st.error("Description tokens are missing or empty.")
        return

    # Safely handle 'description_tokens' column to ensure it is a list of strings
    jobs_data["description_tokens"] = jobs_data["description_tokens"].apply(
        lambda x: eval(x) if isinstance(x, str) else x
    )

    # Compute and display skill filter options
    skills = generate_skill_filter(jobs_data)
    selected_skill = st.selectbox("Select a skill to filter by:", ["All"] + skills)

    display_job_data(jobs_data, selected_skill)


def generate_skill_filter(jobs_data):
    """Generate unique skills from the job listings for filtering."""
    # Flatten the list of all skills and convert to Series for unique() operation
    all_skills = Series(
        [skill for sublist in jobs_data["description_tokens"] for skill in sublist]
    )
    unique_skills = all_skills.unique()
    return list(unique_skills)


def display_job_data(jobs_data, selected_skill):
    """Filter and display job listings based on the selected skill."""
    if selected_skill != "All":
        filtered_jobs = jobs_data[
            jobs_data["description_tokens"].apply(lambda x: selected_skill in x)
        ]
        st.write(filtered_jobs)
    else:
        st.write(jobs_data)


if __name__ == "__main__":
    load_view()
