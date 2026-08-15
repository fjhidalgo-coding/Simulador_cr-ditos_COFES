#!
# Landing de la aplicación Streamlit para pruebas y generación de ejemplos

import streamlit as st


# ----------------------------------------------------------------------------------------------------------------------
# Título de la aplicación 
# ----------------------------------------------------------------------------------------------------------------------
st.title('Utilidades para pruebas y generación de ejemplos')
# ----------------------------------------------------------------------------------------------------------------------
# Definir la configuración de la página y estilos personalizados
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(
   page_title="Utilidades de simulación para pruebas y generación de ejemplos",
   page_icon= ":material/calculate:",
   layout="wide",
   initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 250px !important; # Set the width to your desired value
        }
        .table-right td, .table-right th {
            text-align: right !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# ----------------------------------------------------------------------------------------------------------------------
# Crear la barra lateral con los campos de entrada para la simulación
# ----------------------------------------------------------------------------------------------------------------------
