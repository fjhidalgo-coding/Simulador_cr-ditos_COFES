#!
# Aplicación Streamlit para simular operaciones de los productos NFOIS de COF_ES
'''
Origen:
https://j5vbtgssdbnjlekfpym2p6.streamlit.app/
https://github.com/mildredbr-design/Rev4/blob/main/app.py
'''

import streamlit as st
import bin.COFES__SIM_NFOIS as sim
import bin.COFES___tools as tools

# ----------------------------------------------------------------------------------------------------------------------
# Título de la aplicación y aviso de funcionalidad en construcción
# ----------------------------------------------------------------------------------------------------------------------
st.title('💳 Simulador CofidisPay')
st.info('Funcionalidad en pruebas', icon="⚠️")

# ----------------------------------------------------------------------------------------------------------------------
# Definir la configuración de la página y estilos personalizados
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(
   page_title = "Simulador de CofidisPay",
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
# Primera sección de inputs: capital financiado, tasa de interés, duración y opciones de seguro
# ----------------------------------------------------------------------------------------------------------------------
col_varios_1, col_varios_2, col_varios_3, col_varios_4 = st.columns([0.25,
                                                                     0.25,
                                                                     0.25,
                                                                     0.25],
                                                                    gap="small")

capital_prestado = col_varios_1.number_input("Importe de financiación (€)",
                                             min_value=0.0,
                                             max_value=1000000.0,
                                             step=250.00,
                                             value=3000.0)
tasa = col_varios_2.number_input("TIN anual (%)",
                                 min_value=0.0,
                                 max_value=30.0,
                                 step=0.10,
                                 value=18.00)
plazo = col_varios_3.number_input("Nº de mensualidades",
                                  min_value=1,
                                  max_value=360,
                                  step=1,
                                  value=12,
                                  help="Se debe indicar la duración en meses del plazo de amortización")
seguro_tasa = tools.OPCIONES_SEGURO_NFOIS[col_varios_4.selectbox("Seguro mensual",
                                                                 list(tools.OPCIONES_SEGURO_NFOIS.keys()))]

# ----------------------------------------------------------------------------------------------------------------------
# Segunda sección de inputs: porcentaje de comisión de apertura, importe máximo de comisión de apertura, fecha de financiación y día de vencimiento
# ----------------------------------------------------------------------------------------------------------------------
col_varios_5, col_varios_6, col_varios_7, col_varios_8 = st.columns([0.25,
                                                                     0.25,
                                                                     0.25,
                                                                     0.25],
                                                                    gap="small")

tasa_comision_apertura = col_varios_5.number_input("Comisión de apertura (%)",
                                                   min_value=0.00,
                                                   max_value=10.00,
                                                   step=0.05,
                                                   value=0.00,
                                                   help="Se debe indicar el porcentaje de la comisión de apertura a utlizar en la simulación")
imp_max_com_apertura = col_varios_6.number_input("Importe máximo de la comisión de apertura (EUR)", 
                                                   min_value=0.00, step=1.00, 
                                                   help="Se debe indicar el importe que no debería superar la comisión de apertura")
fecha_financiacion = col_varios_7.date_input("Fecha de financiación",
                                             tools.dt.date.today())
dia_pago = col_varios_8.number_input("Día de vencimiento",
                                     min_value=1,
                                     max_value=12,
                                     step=1,
                                     value=2,
                                     help="Se debe indicar el día de pago seleccionado por el cliente")

# ----------------------------------------------------------------------------------------------------------------------
# Llamar backend para simular la operación y obtener resultados de la simulación
# ----------------------------------------------------------------------------------------------------------------------
if plazo is not None:
    cuadro_amortización, nfois_resumen, datos_tae = sim.nfois_simulacion_completa(capital_prestado,
                                                                                  tasa,
                                                                                  plazo,
                                                                                  fecha_financiacion,
                                                                                  seguro_tasa,
                                                                                  dia_pago,
                                                                                  tasa_comision_apertura,
                                                                                  imp_max_com_apertura)

# ----------------------------------------------------------------------------------------------------------------------
# Exportar resultados de la simulación a Excel
# ----------------------------------------------------------------------------------------------------------------------
    st.download_button(
        label = "📥 Descargar en Excel",
        data = tools.generar_excel(nfois_resumen,
                                   cuadro_amortización,
                                   None,
                                   datos_tae),
        file_name = "simulacion_NFOIS.xlsx",
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar resultados de la simulación en Streamlit
# ----------------------------------------------------------------------------------------------------------------------
    tab1, tab2, tab3 = st.tabs(["Resumen",
                                "Cuadro de amortización",
                                "Datos TAE"])

    with tab1:
        st.dataframe(nfois_resumen.astype(str))

    with tab2:
        st.dataframe(cuadro_amortización.astype(str),
                     hide_index=True)

    with tab3:
        st.dataframe(datos_tae.astype(str),
                     hide_index=True)

# ----------------------------------------------------------------------------------------------------------------------
# Final de la aplicación
# ----------------------------------------------------------------------------------------------------------------------