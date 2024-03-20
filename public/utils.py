import streamlit as st
import base64
from streamlit.components.v1 import html

from PATHS import NAVBAR_PATHS


def inject_custom_css():
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def get_current_route():
    try:
        query = st.query_params.to_dict()
        nav_value = query.get("nav")
        print(nav_value)
        return nav_value
    except:
        return None


def navbar_component():
    with open("assets/images/JobsonLogoNavbar.png", "rb") as logo_file:
        logo_as_base64 = base64.b64encode(logo_file.read()).decode("utf-8")

    navbar_items = ""
    for key, value in NAVBAR_PATHS.items():
        navbar_items += f'<a class="navitem" href="/?nav={value}">{key}</a>'

    component = rf"""
            <nav class="container navbar" id="navbar">
                <ul class="navlist">
                    <a class="navitem1" href="/?nav=empregos">EMPREGOS</a>
                    <a class="navitem2" href="/?nav=habilidades">HABILIDADES</a>
                </ul>
                <div class="logo">
                    <a href="/?nav=empregos"><img src="data:image/png;base64, {logo_as_base64}" alt="Logo" class="logo-img"></a>
                </div>
                <ul class="navlistRight">
                    <a class="navitem3" href="/?nav=sobre">SOBRE</a>
                    <a class="navitem4" href="/?nav=time">TIME</a>
                </ul>
            </nav>
            """
    st.markdown(component, unsafe_allow_html=True)

    js = """
    <script>
        // navbar elements
        var navigationTabs = window.parent.document.querySelectorAll('.navitem, .navitem1, .navitem2, .navitem3, .navitem4');
        var cleanNavbar = function(navigation_element) {
            navigation_element.removeAttribute('target')
        }
        for (var i = 0; i < navigationTabs.length; i++) {
            cleanNavbar(navigationTabs[i]);
        }
        // Close menu if clicked outside
        document.addEventListener("click", function(event) {
            var navbar = document.getElementById("navbar");
            if (!event.target.matches("#sandwichMenu") && !event.target.matches(".navitem, .navitem1, .navitem2, .navitem3, .navitem4")) {
                navbar.classList.remove("show-menu");
            }
        });
        // Dropdown hide / show
        var dropdown = document.getElementById("sandwichMenu");
        dropdown.onclick = function() {
            var navbar = document.getElementById("navbar");
            if (navbar.classList.contains("show-menu")){
                navbar.classList.remove("show-menu");
            } else {
                navbar.classList.add("show-menu");
            }
        };
    </script>
    """
    html(js)
