#!
# Aplicación Streamlit para simular operaciones de los productos amortizables de COF_ES

import streamlit as st


st.set_page_config(
   page_title="Simulador de préstamos amortizables",
   page_icon= ":material/calculate:",
   layout="wide",
   initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 425px !important; # Set the width to your desired value
        }
        .table-right td, .table-right th {
            text-align: right !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)



st.title('Simulador de préstamos amortizables en curso de vida')
st.warning('Funcionalidad en construcción', icon="⚠️")
