import streamlit as st
from modules.formater import Title
import base64


def load_view():

    with open("public/assets/images/JobsonLogoStandard.png", "rb") as logo_file:
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
    O Jobson é uma plataforma que oferece análises profundas e intuitivas sobre o mercado de trabalho atual na área de TI, utilizando capacidades de Análise de Dados. Sua relevância está na geração de insights estratégicos para indivíduos e organizações interessados em entender o panorama do mercado, identificando tendências, demandas de emprego, salários, habilidades e qualificações em alta. Destaca-se por uma Interface de Usuário interativa e acessível, facilitando o acesso a visualizações dinâmicas de dados sobre o mercado de trabalho em TI. Utiliza uma infraestrutura de Back-end sofisticada para coletar dados do Google Jobs de forma automatizada, garantindo análises abrangentes e atualizadas. Em resumo, o Jobson é uma plataforma de dashboard que oferece ao usuário insights valiosos sobre o mercado de trabalho em TI, incluindo tendências e padrões salariais. \n 
    """,
        unsafe_allow_html=True,
    )
