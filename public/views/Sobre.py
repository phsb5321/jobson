import streamlit as st
from modules.formater import Title
import base64


def load_view():
    title = "📊 Sobre"
    Title().page_config(title)

    with open("assets/images/JobsonLogoStandard.png", "rb") as logo_file:
        logo_as_base64 = base64.b64encode(logo_file.read()).decode("utf-8")

    component = rf"""   
                    
                    <img src="data:image/png;base64, {logo_as_base64}" alt="Logo"  style="display: block; margin-left: auto; margin-right: auto;">
                
                """

    # Centralize the content
    st.markdown(component, unsafe_allow_html=True)
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown(
        "<h1 style='text-align: center;'>O que é Jobson?</h1>", unsafe_allow_html=True
    )
    st.markdown("")
    st.markdown("")
    st.markdown("")
    st.markdown(
        """
    Open-sourcing job requirements for aspiring data analysts is necessary for data nerds to focus more efficiently on what skills they need to learn for their future job. This dashboard is only the beginning of that journey.Open-sourcing job requirements for aspiring data analysts is necessary for data nerds to focus more efficiently on what skills they need to learn for their future job. This dashboard is only the beginning of that journey.Open-sourcing job requirements for aspiring data analysts is necessary for data nerds to focus more efficiently on what skills they need to learn for their future job. This dashboard is only the beginning of that journey.Open-sourcing job requirements for aspiring data analysts is necessary for data nerds to focus more efficiently on what skills they need to learn for their future job. This dashboard is only the beginning of that journey.Open-sourcing job requirements for aspiring data analysts is necessary for data nerds to focus more efficiently on what skills they need to learn for their future job. This dashboard is only the beginning of that journey.Open-sourcing job requirements for aspiring data analysts is necessary for data nerds to focus more efficiently on what skills they need to learn for their future job. This dashboard is only the beginning of that journey.Open-sourcing job requirements for aspiring data analysts is necessary for data nerds to focus more efficiently on what skills they need to learn for their future job. This dashboard is only the beginning of that journey.Open-sourcing job requirements for aspiring data analysts is necessary for data nerds to focus more efficiently on what skills they need to learn for their future job. This dashboard is only the beginning of that journey. \n 
    """,
        unsafe_allow_html=True,
    )
