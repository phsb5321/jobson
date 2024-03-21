from pandas import DataFrame
import streamlit as st
from modules.formater import Title
from modules.importer import DataImport


def load_view():
    """Load the Streamlit view for displaying job data."""
    Title.display("💸 Empregos")  # Update this to use the new `display` method
    jobs_data = DataImport().fetch_and_clean_data()

    # Since we now have more straightforward columns, let's create filters based on job modalities and salary range.
    job_modalities = generate_job_modalities_filter(jobs_data)

    # Generate filters for skills and job types using the new structure.
    skills = generate_skill_filter(jobs_data)
    job_types = generate_job_type_filter(
        jobs_data
    )  # Using the new columns for contract types

    st.markdown("## 💸 Empregos por faixa salarial")
    st.markdown("# 💰 Filters")
    display_filters(skills, job_modalities, job_types)


def configure_page_title(title):
    """Configure the Streamlit page title."""
    Title.display(title)


def load_and_clean_data():
    """Load job listings data."""
    return DataImport().fetch_and_clean_data()


def generate_skill_filter(jobs_data):
    """Generate a list of skills for filtering job listings."""
    skill_count = (
        DataFrame(jobs_data.description_tokens.sum())
        .value_counts()
        .rename_axis("keywords")
        .reset_index(name="counts")
    )
    skill_count = skill_count[skill_count.keywords != ""]
    return ["Select All"] + list(skill_count.keywords)


def generate_job_modalities_filter(jobs_data):
    """Generate filters for job modalities based on new columns."""
    modalities = {
        "Home Office": jobs_data["isHomeOffice"].any(),
        "Full Time": jobs_data["isFullTime"].any(),
        "Half Time": jobs_data["isHalfTime"].any(),
        "Internship": jobs_data["isInternship"].any(),
        "PJ": jobs_data["isPJ"].any(),
        "CLT": jobs_data["isCLT"].any(),
    }
    return ["Select All"] + [
        modality for modality, available in modalities.items() if available
    ]


def generate_job_type_filter(jobs_data):
    """This function can be adjusted or repurposed based on new data. Placeholder for now."""
    # Placeholder for potential filter based on job types or contract types
    return ["Select All"]


def display_filters(skills, job_modalities, job_types):
    """Display filters for job listings."""
    st.selectbox("Data Skill:", skills)
    st.multiselect("Job Modalities:", job_modalities)
    st.selectbox("Contract Type:", job_types)  # Example placeholder


if __name__ == "__main__":
    load_view()
