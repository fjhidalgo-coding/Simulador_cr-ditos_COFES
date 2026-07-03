#!
# Aplicación Streamlit para simular operaciones en curso de vida sobre productos AMO y RCC de COF_ES

import streamlit as st
import bin.COFES__SIM_LIFE as sim
import bin.COFES___tools as tools

# ----------------------------------------------------------------------------------------------------------------------
# Título de la aplicación 
# ----------------------------------------------------------------------------------------------------------------------
st.title('Simulador para operaciones en curso de vida')
# ----------------------------------------------------------------------------------------------------------------------
# Definir la configuración de la página y estilos personalizados
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(
   page_title="Simulador para operaciones en curso de vida",
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
# ----------------------------------------------------------------------------------------------------------------------
# Toggle para seleccionar entre simulación unitaria o masiva
# ----------------------------------------------------------------------------------------------------------------------
on = st.toggle("Simulación amortizable",
               value=False,
               key="toggle_AMO")
# ----------------------------------------------------------------------------------------------------------------------
# Sección de inputs: capital financiado, tasa de interés y la fecha del último recibo o fecha de financiación
# ----------------------------------------------------------------------------------------------------------------------
col_varios_1, col_varios_2, col_varios_3 = st.columns([0.34,
                                                       0.33,
                                                       0.33],
                                                       gap="small")
capital_pendiente = col_varios_1.number_input("Capital pendiente (EUR)",
                                              min_value=60.00,
                                              max_value=60_000.00,
                                              step=250.00,
                                              value=3_000.00,
                                              help="Se debe indicar el importe del capital pendiente. El importe mínimo es de 60 EUR y el máximo de 60.000 EUR.")
tasa_interes = col_varios_2.number_input("TIN anual (%)",
                                         min_value=0.0,
                                         max_value=30.0,
                                         step=0.10,
                                         value=21.79,
                                         help="Se debe indicar el porcentaje de la tasa de interés anual. El porcentaje mínimo es de 0% y el máximo de 30,00%.")
fecha_inicial = col_varios_3.date_input("Fecha de ultimo recibo / Fecha de financiacion",
                                        tools.dt.date.today())
# ----------------------------------------------------------------------------------------------------------------------
# Sección de inputs: capital financiado, tasa de la comisión de apertura y la fecha de financiación
# ----------------------------------------------------------------------------------------------------------------------
col_varios_4, col_varios_5, col_varios_6 = st.columns([0.34,
                                                       0.33,
                                                       0.33],
                                                       gap="small")
mensualidad_actual = col_varios_4.number_input("Mensualidad actual (EUR)",
                                               min_value=3.00,
                                               max_value=2_000.00,
                                               step=15.00,
                                               value=90.00,
                                               help="Se debe indicar el importe de la mensualidad actual. El importe mínimo es de 3 EUR y el máximo de 2.000 EUR.")
if on is True:
    seguro_tasa = tools.OPCIONES_SEGURO_AMO[col_varios_5.selectbox("Seguro mensual",
                                                                   list(tools.OPCIONES_SEGURO_AMO.keys())[:3], index=2)]
else:
    seguro_tasa = tools.OPCIONES_SEGURO_RCC[col_varios_5.selectbox("Seguro mensual",
                                                                   list(tools.OPCIONES_SEGURO_RCC.keys()))]
dia_pago = col_varios_6.number_input("Día de vencimiento",
                                     min_value=1,
                                     max_value=29,
                                     step=1,
                                     value=2, 
                                     help="Se debe indicar el día de vencimiento de los recibos")
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar opciones de simulación
# ----------------------------------------------------------------------------------------------------------------------
if on is True:
    tab1, tab2, tab3, tab4 = st.tabs(["Amortizaciones anticipadas",
                                      "Cambio de día de pago",
                                      "Cambio de mensualidad",
                                      "Aplazamiento"])
else:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Amortizaciones anticipadas",
                                            "Cambio de día de pago",
                                            "Cambio de mensualidad",
                                            "Aplazamiento",
                                            "Joker / Comodín",
                                            "Disposiciones (aumentos de capital)"])
with tab1:
    df_amort_raw = st.data_editor(tools.pd.DataFrame({"Fecha": [None],
                                                      "Importe": [0.0]}),
                                  column_config={"Fecha": st.column_config.DateColumn("Fecha amortizacion",
                                                                                      format="DD/MM/YYYY"),
                                                 "Importe": st.column_config.NumberColumn("Importe (EUR)",
                                                                                          min_value=0,
                                                                                          step=100)},
                                  num_rows="dynamic",
                                  width="stretch",
                                  key="editor_amort")
with tab2:
    df_cambio_dia_raw = st.data_editor(tools.pd.DataFrame({"Fecha del cambio": [None],
                                                           "Nuevo dia": [None]}),
                                       column_config={"Fecha del cambio": st.column_config.DateColumn("Fecha exacta del cambio",
                                                                                                      format="DD/MM/YYYY"),
                                                      "Nuevo dia": st.column_config.NumberColumn("Nuevo dia de pago",
                                                                                                 min_value=1,
                                                                                                 max_value=29,
                                                                                                 step=1)},
                                       num_rows="dynamic",
                                       width="stretch",
                                       key="editor_cambio_dia")
with tab3:
    df_cambio_cuota_raw = st.data_editor(tools.pd.DataFrame({"Fecha del cambio": [None],
                                                             "Nueva cuota (EUR)": [None]}),
                                         column_config={"Fecha del cambio": st.column_config.DateColumn("Fecha exacta del cambio",
                                                                                                        format="DD/MM/YYYY"),
                                                        "Nueva cuota (EUR)": st.column_config.NumberColumn("Nueva cuota (EUR)",
                                                                                                           min_value=0,
                                                                                                           step=1.0)},
                                         num_rows="dynamic",
                                         width="stretch",
                                         key="editor_cambio_cuota")
with tab4:
    col_varios_7, col_varios_8, col_varios_9, col_varios_10 = st.columns([0.15,
                                                                          0.20,
                                                                          0.25,
                                                                          0.40],
                                                                          gap="small")
    usar_aplazamiento = col_varios_7.checkbox("Activar aplazamiento")
    if usar_aplazamiento:
        fecha_aplazamiento_input = col_varios_8.date_input("Fecha de inicio del aplazamiento",
                                                           tools.dt.date.today(),
                                                           key="aplazamiento_fecha")
        importe_aplazado = col_varios_9.number_input("Importe del capital impagado a aplazar (EUR)",
                                                     min_value=0.00,
                                                     max_value=60_000.00,
                                                     step=25.00,
                                                     value=0.00,
                                                     help="Se debe indicar el importe del capital impagado a aplazar. El importe mínimo es de 0 EUR y el máximo de 60.000 EUR.")
    fecha_aplazamiento = fecha_aplazamiento_input if usar_aplazamiento else None
    importe_aplazado = importe_aplazado if usar_aplazamiento else 0.00
if on is True:
    fecha_joker = None
    df_dispos_raw = tools.pd.DataFrame({"Fecha": [None],
                                        "Importe": [0.0]})
else:
    with tab5: # type: ignore
        col_varios_11, col_varios_12, col_varios_13 = st.columns([0.15,
                                                                  0.20,
                                                                  0.65],
                                                                  gap="small")
        usar_joker = col_varios_11.checkbox("Activar joker")
        if usar_joker:
            fecha_joker_input = col_varios_12.date_input("Fecha de la orden del joker",
                                                         tools.dt.date.today(),
                                                         key="joker_fecha")
        fecha_joker = fecha_joker_input if usar_joker else None
    with tab6: # type: ignore
        df_dispos_raw = st.data_editor(tools.pd.DataFrame({"Fecha": [None],
                                                           "Importe": [0.0]}),
                                       column_config={"Fecha": st.column_config.DateColumn("Fecha disposicion",
                                                                                           format="DD/MM/YYYY"),
                                                      "Importe": st.column_config.NumberColumn("Importe (EUR)",
                                                                                               min_value=0,
                                                                                               step=100)},
                                       num_rows="dynamic",
                                       width="stretch",
                                       key="editor_dispos")
# ----------------------------------------------------------------------------------------------------------------------
# Llamar backend para simular la operación y obtener resultados de la simulación en curso de vida
# ----------------------------------------------------------------------------------------------------------------------
if st.button("Simular"):
    with st.spinner("Simulando..."):
            resultado_simulacion_masiva = "Hi"
    st.success("Simulación masiva completada")
# ----------------------------------------------------------------------------------------------------------------------
# Exportar resultados de la simulación a Excel
# ----------------------------------------------------------------------------------------------------------------------
    st.download_button(
        label="📥 Descargar en Excel",
        data=tools.generar_excel(resumen2,
                             cuadro_amortizacion,
                             tools.pd.DataFrame({'TAE': [resumen1.at['%','TAE']],
                                                 'Ejemplo representativo': [ejemplo_representativo]}),
                             input_tae  ),
        file_name="simulacion_en_curso_de_vida.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar resultados de la simulación en Streamlit
# ----------------------------------------------------------------------------------------------------------------------
    with st.expander("Resumen", expanded=True):
        col1, col2 = st.columns([0.08,
                                     0.92],
                                    gap="small")
        html_table1 = resumen1.to_html(classes='table table-right',
                                           index=True)
        html_table2 = resumen2.to_html(classes='table table-right',
                                           index=True)
        col1.markdown(html_table1,
                          unsafe_allow_html=True)
        col2.markdown(html_table2,
                          unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Cuadro de amortización",
                                    "Ejemplo representativo",
                                    "Detalle TAE"])
        with tab1:
                st.dataframe("cuadro_amortizacion",
                         hide_index=True)
        with tab2:
                st.code("ejemplo_representativo"    ,
                    wrap_lines=True)
        with tab3:
                st.dataframe("input_tae",
                         hide_index=True)
# ----------------------------------------------------------------------------------------------------------------------
# Final de la aplicación
# ---------------------------------------------------------------------------------------------------------------------- 