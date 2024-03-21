# formater.py
import streamlit as st


class Title:
    @staticmethod
    def display(title: str):
        """
        Displays a title in the Streamlit app.
        Arguments:
        - title: The title to display.
        """
        st.header(title)  # Using `st.header` to demonstrate a potential use-case
