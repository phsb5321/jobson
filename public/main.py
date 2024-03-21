# main.py
import streamlit as st
from views import Empregos, Habilidades, Sobre, Time
import utils as utl

# Centralize the page configuration here.
st.set_page_config(layout="wide", page_title="Jobson Dashboard", page_icon="🚀")

# Apply custom CSS styles
utl.inject_custom_css()

# Display the custom navbar component
utl.navbar_component()


def navigate_route():
    """Direct user navigation based on the current route."""
    # Fetch the route from the query parameter 'nav'
    route = utl.get_current_route()

    # Route mapping to corresponding view loading functions
    routes_dict = {
        "empregos": Empregos.load_view,
        "habilidades": Habilidades.load_view,
        "sobre": Sobre.load_view,
        "time": Time.load_view,
        None: Empregos.load_view,  # Default route
    }

    # Execute the corresponding view loading function
    if route in routes_dict:
        routes_dict[route]()


# Execute navigation based on the current route
navigate_route()
