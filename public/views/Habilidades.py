import streamlit as st
import pandas as pd
import altair as alt
from modules.formater import Title
from modules.importer import DataImport
from config import Config


def load_view():

    jobs_df = DataImport().fetch_and_clean_data()

    # Check if DataFrame is empty and return a message if true
    if jobs_df.empty:
        st.error("No jobs data available.")
        return

    # Check if 'description_tokens' colum;n exists and is non-empty
    if (
        "description_tokens" in jobs_df.columns
        and not jobs_df["description_tokens"].empty
    ):
        # Convert description_tokens from string to list if necessary
        jobs_df["description_tokens"] = jobs_df["description_tokens"].apply(
            lambda x: eval(x) if isinstance(x, str) else x
        )
    else:
        st.error("Description tokens are missing or empty.")
        return

    skill_count = agg_skill_data(jobs_df)

    # User options for filtering by skill category
    keyword_choice = st.selectbox(
        "Filter by skill category:", ["All"] + Config.SKILL_CATEGORIES
    )
    if keyword_choice != "All":
        skill_count = filter_skills_by_category(skill_count, keyword_choice)

    st.markdown("## 🛠️ Most Requested Skills")
    chart = create_skills_chart(skill_count)
    st.altair_chart(chart, use_container_width=True)


def agg_skill_data(jobs_df):
    """Aggregate skill data from job descriptions."""
    # Ensure data is aggregated only if not empty
    if not jobs_df.empty and "description_tokens" in jobs_df:
        skill_data = pd.DataFrame(jobs_df.description_tokens.sum(), columns=["skill"])
    else:
        return pd.DataFrame(columns=["skill", "count", "percentage"])

    skill_data = skill_data[skill_data.skill.isin(Config.SKILL_LIST)]
    skill_count = skill_data["skill"].value_counts().reset_index()
    skill_count.columns = ["skill", "count"]
    skill_count["percentage"] = skill_count["count"] / len(jobs_df)
    return skill_count


def filter_skills_by_category(skill_count, category):
    """Filter skills by category based on Config settings."""
    filtered_skills = Config.CATEGORY_SKILLS.get(category, [])
    return skill_count[skill_count["skill"].isin(filtered_skills)]


def create_skills_chart(skill_count):
    """ "Create Altair chart for visualizing skills data."""
    chart = (
        alt.Chart(skill_count)
        .mark_bar()
        .encode(
            x=alt.X("skill:N", sort="-y", title="Skill"),
            y=alt.Y("count:Q", title="Count"),
            tooltip=["skill", "count", alt.Tooltip("percentage", format=".2%")],
        )
        .properties(width=600)
    )
    return chart


if __name__ == "__main__":
    load_view()
