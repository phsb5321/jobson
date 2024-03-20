import streamlit as st
import pandas as pd
import altair as alt
from modules.formater import Title
from modules.importer import DataImport
from app.config import Config


def load_view():
    # Page Title
    title = "🛠️ Habilidades"
    Title().page_config(title)

    # Import and clean data
    jobs_df = DataImport().fetch_and_clean_data()

    # Convert description tokens from string to list if necessary
    jobs_df["description_tokens"] = jobs_df["description_tokens"].apply(eval)

    # Skill aggregation function
    def agg_skill_data(jobs_df):
        skill_data = pd.DataFrame(jobs_df.description_tokens.sum(), columns=["skill"])
        skill_data = skill_data[skill_data.skill.isin(Config.SKILL_LIST)]
        skill_count = skill_data["skill"].value_counts().reset_index()
        skill_count.columns = ["skill", "count"]
        skill_count["percentage"] = skill_count["count"] / len(jobs_df)
        return skill_count

    skill_count = agg_skill_data(jobs_df)

    # User options
    keyword_choice = st.selectbox(
        "Filter by skill category:", ["All"] + Config.SKILL_CATEGORIES
    )
    if keyword_choice != "All":
        skill_count = skill_count[
            skill_count["skill"].isin(Config.CATEGORY_SKILLS[keyword_choice])
        ]

    st.markdown("## 🛠️ Most Requested Skills")

    skill_count = skill_count.head(20)  # Display top 20 skills

    chart = (
        alt.Chart(skill_count)
        .mark_bar()
        .encode(
            x=alt.X("skill:N", sort="-y", title="Skill"),
            y=alt.Y("count:Q", title="Count"),
            tooltip=["skill", "count", alt.Tooltip("percentage", format=",.2%")],
        )
        .properties(width=800, height=400)
    )

    st.altair_chart(chart, use_container_width=True)


# Function call to load view
if __name__ == "__main__":
    load_view()
