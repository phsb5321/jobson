# Screen for 🛠️ Habilidades
import streamlit as st
import pandas as pd
import altair as alt
from modules.formater import Title
from modules.importer import DataImport
from config import Config


def load_view():
    title = "🛠️ Habilidades"
    Title.display(title)

    jobs_df = DataImport().fetch_and_clean_data()

    if jobs_df.empty:
        st.error("No jobs data available.")
        return

    if (
        "description_tokens" in jobs_df.columns
        and not jobs_df["description_tokens"].isnull().all()
    ):
        jobs_df["description_tokens"] = jobs_df["description_tokens"].apply(
            lambda x: eval(x) if isinstance(x, str) else x
        )
    else:
        st.error("Description tokens are missing or empty.")
        return

    skill_count = agg_skill_data(jobs_df)

    keyword_choice = st.selectbox(
        "Filter by skill category:", ["All"] + list(Config.SKILL_CATEGORIES.keys())
    )

    if keyword_choice != "All":
        skill_count = filter_skills_by_category(skill_count, keyword_choice)

    st.markdown("## 🛠️ Most Requested Skills")
    chart = create_skills_chart(skill_count)
    st.altair_chart(chart, use_container_width=True)


def agg_skill_data(jobs_df):
    if not jobs_df.empty:
        skill_data = pd.DataFrame(
            [skill for tokens in jobs_df["description_tokens"] for skill in tokens],
            columns=["skill"],
        )
        skill_data = skill_data[skill_data["skill"].isin(Config.SKILL_LIST)]
        skill_count = skill_data["skill"].value_counts().reset_index()
        skill_count.columns = ["skill", "count"]
        skill_count["percentage"] = skill_count["count"] / len(jobs_df)
        return skill_count
    return pd.DataFrame(columns=["skill", "count", "percentage"])


def filter_skills_by_category(skill_count, category):
    filtered_skills = Config.CATEGORY_SKILLS.get(category, [])
    return skill_count[skill_count["skill"].isin(filtered_skills)]


def create_skills_chart(skill_count):
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
