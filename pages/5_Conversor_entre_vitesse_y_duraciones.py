#!
'''
Aplicación Streamlit para realizar conversiones entre velocidades y duraciones de productos revolving
'''

import streamlit as st
import bin.COFES__SIM_RCC as sim
import bin.COFES___tools as tools

# ----------------------------------------------------------------------------------------------------------------------
# Título de la aplicación y aviso de funcionalidad en construcción
# ----------------------------------------------------------------------------------------------------------------------
st.title('Conversor de velocidad a duración')
# ----------------------------------------------------------------------------------------------------------------------
# Definir la configuración de la página y estilos personalizados
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(
   page_title = "Conversor de velocidades a duración",
   page_icon = ":material/calculate:",
   layout = "wide",
   initial_sidebar_state = "expanded",
)
st.markdown(
    """
    <style>
        section[data-testid = "stSidebar"] {
            width: 425px !important; # Set the width to your desired value
        }
        .table-right td, .table-right th {
            text-align: right !important;
        }
    </style>
    """,
    unsafe_allow_html = True,
)
# ----------------------------------------------------------------------------------------------------------------------
# Inputs: TIN, capital financiado, fecha de financiación y día de pago  (columna 1)
# ----------------------------------------------------------------------------------------------------------------------
col_varios_1, col_varios_2, col_varios_3 = st.columns([0.40,
                                                       0.30,
                                                       0.30],
                                                       gap="small")
tin = col_varios_1.number_input("TIN anual (%)",
                                min_value=0.0,
                                max_value=30.0,
                                step=0.10,
                                value=21.79)
capital = col_varios_1.number_input("Importe de financiación (€)",
                                    min_value=0.0,
                                    max_value=1000000.0,
                                    step=250.00,
                                    value=3000.0)
fecha_financiacion = col_varios_1.date_input("Fecha de financiación",
                                             tools.dt.date.today())
dia_pago = col_varios_1.number_input("Día de vencimiento",
                                     min_value=1,
                                     max_value=12,
                                     step=1,
                                     value=2,
                                     help="Se debe indicar el día de pago seleccionado por el cliente")
# ----------------------------------------------------------------------------------------------------------------------
# Input de velocidades para crear el listado a convertir a duraciones (columna 2)
# ----------------------------------------------------------------------------------------------------------------------
df_vitesse_raw = col_varios_2.data_editor(tools.pd.DataFrame({"Velocidades": [0.0]}),
                                          column_config={"Velocidades": st.column_config.NumberColumn("Velocidades",
                                                                                                      min_value=2.0,
                                                                                                      step=0.01)},
                                          num_rows="dynamic",
                                          width="stretch",
                                          key="editor_amort")
# ----------------------------------------------------------------------------------------------------------------------
# Llamar backend para simular la operación y obtener resultados de la simulación
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Llamar backend para simular la operación y obtener resultados de la simulación
# ----------------------------------------------------------------------------------------------------------------------
if col_varios_2.button("Convertir"):
    with st.spinner("Convertiendo..."):
        rcc_duraciones, rcc_cuotas = sim.rcc_obtener_duraciones(capital,
                                                                tin,
                                                                fecha_financiacion,
                                                                df_vitesse_raw)
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar duraciones calculadas para cada velocidad en la tercera columna
# ----------------------------------------------------------------------------------------------------------------------
        col_varios_3.dataframe(rcc_duraciones, width='stretch')
# ----------------------------------------------------------------------------------------------------------------------
# Final de la aplicación
# ----------------------------------------------------------------------------------------------------------------------