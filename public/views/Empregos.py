# Empregos.py
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime
from modules.formater import Title
from modules.importer import DataImport
import utils as utl
import matplotlib.pyplot as plt
import random

def load_view():
    jobs_data = DataImport().fetch_and_clean_data()

    # Ensure jobs_data isn't empty before proceeds
    if jobs_data.empty:
        st.error("No job data available.")
        return

    # Skill sort, count, and filter list data
    select_all = "Select All"
    
    # Filter job types
    job_type = ["Select All", "Full-time", "Contractor", "Part Time", "Internship"]


    # Top page build
    st.markdown("## 💸 Empregos por faixa salarial")
    job_type_choice = st.radio("Job Type:", job_type, index=0, format_func=lambda x: 'Select All' if x == job_type[0] else x, horizontal=True)
    
    money_time_list = ["Anual", "Por hora"] 
    money_time_choice = st.radio('Escala temporal:', money_time_list, horizontal = True)
    
    # Filter jobs based on selected job type
    if job_type_choice == "Select All":
        filtered_jobs = jobs_data
    else:
        # Handle NaN values in 'schedule_type' column
        filtered_jobs['schedule_type'] = filtered_jobs['schedule_type'].fillna('Unknown')
        filtered_jobs = filtered_jobs[filtered_jobs['schedule_type'].str.contains(job_type_choice)]
    
    

    # Sort DataFrame by 'salary_yearly' in descending order and select top N job titles
    top_n = 10  # Choose the number of top job titles to display
    top_jobs_yearly = filtered_jobs.sort_values(by='max_salary', ascending=False).drop_duplicates('title').head(top_n)
    top_jobs_hourly = filtered_jobs.sort_values(by='max_salary', ascending=False).drop_duplicates('title').head(top_n)
    
    # Function to generate a random color
    def generate_random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'rgb({r},{g},{b})'

    # Generate random colors for each data point
    top_jobs_yearly['color'] = top_jobs_yearly.apply(lambda row: generate_random_color(), axis=1)
    top_jobs_hourly['color'] = top_jobs_hourly.apply(lambda row: generate_random_color(), axis=1)
        
    
    # yearly chart
    selector = alt.selection_single(encodings=['x', 'y'])
    yearly_chart = alt.Chart(top_jobs_yearly).mark_bar(cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10 ).encode(
        x=alt.X('max_salary:Q', sort=None, title="", axis=alt.Axis(labelFontSize=20) ),      
        y=alt.Y('title:N',title="Emprego", sort='x'),
         color=alt.Color('color:N', legend=None)  # Use the generated random colors
    ).properties(
        width=800,
        height=300
    ).add_selection(
            selector
    ).configure_view(
            strokeWidth=0
    )
    
    # hourly chart
    hourly_chart = alt.Chart(top_jobs_hourly).mark_bar(cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10 ).encode(
        x=alt.X('min_salary:Q', sort=None, title="", axis=alt.Axis(labelFontSize=20) ),      
        y=alt.Y('title:N',title="Emprego", sort='x'),
        color=alt.Color('color:N', legend=None)  # Use the generated random colors
    ).properties(
        width=800,
        height=300
    ).add_selection(
            selector
    ).configure_view(
            strokeWidth=0
    )
    


    
    if money_time_choice == money_time_list[0]:
        st.altair_chart(yearly_chart, use_container_width=True)
    else:
        st.altair_chart(hourly_chart, use_container_width=True)


if __name__ == "__main__":
    load_view()
