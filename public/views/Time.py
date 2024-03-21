import streamlit as st
from modules.formater import Title
import base64


def load_view():
    # Title page

    # Function to display image in circular shape
    def circular_image(image_path, size=200):
        return f'<img src="{image_path}" style="border-radius: 50%; width: {size}px; height: {size}px;">'

    # Path to your image file
    image_path = "static/MatheusDalia.jpeg"

    with open("public/assets/images/MatheusDalia.jpeg", "rb") as logo_file:
        matheus_as_base64 = base64.b64encode(logo_file.read()).decode("utf-8")
    with open("public/assets/images/PedroBalbino.jpeg", "rb") as logo_file:
        pedro_as_base64 = base64.b64encode(logo_file.read()).decode("utf-8")  
    with open("public/assets/images/NewtonNeto.jpeg", "rb") as logo_file:
        newton_as_base64 = base64.b64encode(logo_file.read()).decode("utf-8")    
    with open("public/assets/images/Alexandre.jpeg", "rb") as logo_file:
        alexandre_as_base64 = base64.b64encode(logo_file.read()).decode("utf-8")              
    component = rf"""   
                    <div class="member-line" style="display: flex; justify-content: center;">
                        <style>
                            @media screen and (max-width: 1400px) {{
                                .member-line {{
                                    flex-wrap: wrap;
                                }}
                                .member-individual {{
                                    margin-right: 80px;
                                }}
                            }}
                        </style>
                        <div class="member-individual" style="margin-right: 80px; flex: 0 0 auto; text-align: center;">
                            <img src="data:image/png;base64, {matheus_as_base64}" alt="Logo" class="member-photo" style="border-radius: 50%; width: 200px; height: 200px;">
                            <h2>Matheus Dalia</h2>
                            <p class="text-member" style="max-width: 300px; text-align: center;">Matheus Dalia é o desenvolvedor front-end.</p>
                        </div>
                        <div class="member-individual" style="margin-right: 80px; flex: 0 0 auto; text-align: center;">
                            <img src="data:image/png;base64, {pedro_as_base64}" alt="Logo" class="member-photo" style="border-radius: 50%; width: 200px; height: 200px;">
                            <h2>Pedro Balbino</h2>
                            <p class="text-member" style="max-width: 300px; text-align: center;">Pedro Balbino é o líder e desenvolvedor back-end.</p>
                        </div>
                        <div class="member-individual" style="margin-right: 80px;flex: 0 0 auto; text-align: center;">
                            <img src="data:image/png;base64, {newton_as_base64}" alt="Logo" class="member-photo" style="border-radius: 50%; width: 200px; height: 200px;">
                            <h2>Newton</h2>
                            <p class="text-member" style="max-width: 200px; text-align: center; ">Newton é um dos gerentes do projeto.</p>
                        </div>
                        <div class="member-individual" style=" flex: 0 0 auto;text-align: center;">
                            <img src="data:image/png;base64, {alexandre_as_base64}" alt="Logo" class="member-photo" style="border-radius: 50%; width: 200px; height: 200px;">
                            <h2>Alexandre</h2>
                            <p class="text-member" style="max-width: 200px; text-align: center;">Alexandre é um dos gerentes do projeto.</p>
                        </div>
                    
                    </div>
                """

    # Centralize the content
    st.markdown(component, unsafe_allow_html=True)
