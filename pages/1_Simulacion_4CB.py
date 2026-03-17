#!
# Aplicación Streamlit para simular las facilidades de pago 4CB de COF_ES

import datetime  as dt
import streamlit as st
import pandas as pd
import bin.COFES__SIM_4CB as sim
import bin.COFES___tools as tools


st.title('Simulador para facilidades de pago 4CB')
st.info('Funcionalidad en pruebas', icon="⚠️")

st.set_page_config(
   page_title="Simulador para facilidades de pago 4CB",
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



on = st.toggle("Simulación masiva 4CB", value=False, key="toggle_4CB")

if on is False:
    col_varios_1, col_varios_2, col_varios_3 = st.columns([0.34, 0.33, 0.33], gap="small")
    
    capital_prestado_4CB = col_varios_1.number_input("Importe solicitado (EUR)",
                                           min_value=60.00, max_value=1500.00, step=10.00, value=300.00,
                                           help="Se debe indicar el importe del capital de la facilidad de pago. El importe mínimo es de 60 EUR y el máximo de 1500 EUR.")

    tasa_comision_apertura_4CB = col_varios_2.number_input("Porcentaje comisión de apertura",
                                                       min_value=0.00, max_value=2.80, step=0.05,
                                                       help="Se debe indicar el porcentaje de la comisión de apertura de la facilidad de pago. El porcentaje mínimo es de 0% y el máximo de 2.80%.")
        
    fecha_financiacion_4CB = col_varios_3.date_input("Fecha de financiación", dt.date.today())
    
    if st.session_state.get("simular", True):
        
        # Obtener los resultados de la simulación llamando a la función visualizar_simulacion_unitaria de la librería COFES_SIM_AMO_Consola
        
        resumen1, resumen2, ejemplo_representativo, cuadro_amortizacion, input_tae = sim.visualizar_simulacion_unitaria(capital_prestado_4CB,
                                                                                                                        tasa_comision_apertura_4CB,
                                                                                                                        fecha_financiacion_4CB)
        st.download_button(
            label="📥 Descargar en Excel",
            data=tools.generar_excel(resumen2,
                                     cuadro_amortizacion,
                                     pd.DataFrame({'TAE': [resumen1.at['%','TAE']], 'Ejemplo representativo': [ejemplo_representativo]}),
                                     input_tae  ),
            file_name="simulacion_4CB_unitaria.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        
        # Mostrar resumen de la simulación
    
        # Mostrar el resumen económico de la simulación

        with st.expander("Resumen", expanded=True):
            col1, col2 = st.columns([0.08, 0.92], gap="small")
            html_table1 = resumen1.to_html(classes='table table-right', index=True)
            html_table2 = resumen2.to_html(classes='table table-right', index=True)

            col1.markdown(html_table1, unsafe_allow_html=True)
            col2.markdown(html_table2, unsafe_allow_html=True)



        # Mostrar las pestañas con los detalles de la simulación

        tab1, tab2, tab3 = st.tabs(["Cuadro de amortización", "Ejemplo representativo", "Detalle TAE"])



        # Mostrar contenido de la pestaña Secuencias financieras

        with tab1:
            st.dataframe(cuadro_amortizacion,hide_index=True)



        # Mostrar contenido de la pestaña "Ejemplo representativo"

        with tab2:
            st.code(ejemplo_representativo, wrap_lines=True)



        # Mostrar contenido de la pestaña "Cuadro de amortización"

        with tab3:
            st.dataframe(input_tae,hide_index=True)

else:
    col_varios_4, col_varios_5, col_varios_6 = st.columns([0.34, 0.33, 0.33], gap="small")
    
    importes_prestado_4CB = col_varios_4.slider("Rango de importe solicitado (EUR)",
                                              min_value=60.00, max_value=1500.00, step=10.00, value=[300.00,360.00],
                                              help="Se debe indicar el rango del capital de la facilidad de pago. El importe mínimo es de 60 EUR y el máximo de 1500 EUR.")

    tasas_comision_apertura_4CB = col_varios_5.slider("Rango del porcentaje comisión de apertura",
                                                 min_value=0.00, max_value=2.80, step=0.05, value=[2.60,2.80],
                                                 help="Se debe indicar el porcentaje de la comisión de apertura a utlizar en la simulación")
        
    fechas_financiacion_4CB = col_varios_6.date_input("Fecha de financiación", dt.date.today())
    
    if st.button("Simular"):
        with st.spinner("Simulando..."):
            resultado_simulacion_masiva = sim.simular_masivamente(importes_prestado_4CB,
                                                                  tasas_comision_apertura_4CB,
                                                                  fechas_financiacion_4CB)

        st.success("Simulación masiva completada")

        st.download_button(
            label="📥 Descargar en Excel",
            data=tools.generar_excel(resultado_simulacion_masiva=resultado_simulacion_masiva),
            file_name="simulacion_4CB_masiva.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        # Mostrar resultados de la simulación masiva

        with st.expander("Resultados de la simulación masiva", expanded=True):
            st.dataframe(resultado_simulacion_masiva, hide_index=True)



# Final de la aplicación    