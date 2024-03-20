# formater.py
import streamlit as st


class Title:
    """
    A helper class to manage page configuration including title and favicon.
    """

    def __init__(self, img_path="images/JobsonLogoNavbar.png"):
        """
        Initializes the Title object with an optional image path for the favicon.

        Parameters:
        - img_path: str, path to the favicon image.
        """
        self.img_path = img_path

    def page_config(self, title):
        """
        Sets the page title and favicon based on provided arguments.

        Parameters:
        - title: str, the title of the page to be set.
        """
        st.set_page_config(page_title=title, page_icon=self.img_path)
