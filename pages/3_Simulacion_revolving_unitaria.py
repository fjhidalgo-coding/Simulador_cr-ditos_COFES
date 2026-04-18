#!
# Aplicación Streamlit para simular operaciones de los productos revolving de COF_ES

import streamlit as st
import bin.COFES__SIM_RCC as sim
import bin.COFES___tools as tools

# ----------------------------------------------------------------------------------------------------------------------
# Título de la aplicación y aviso de funcionalidad en construcción
# ----------------------------------------------------------------------------------------------------------------------
st.title('Simulador Revolving con Seguro Opcional')
# ----------------------------------------------------------------------------------------------------------------------
# Definir la configuración de la página y estilos personalizados
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(
   page_title = "Simulador de préstamos revolving",
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
# Primera sección de inputs: coste del seguro, fecha de financiación y día de pago
# ----------------------------------------------------------------------------------------------------------------------
col_varios_1, col_varios_2, col_varios_3, col_varios_4 = st.columns([0.25,
                                                                     0.25,
                                                                     0.25,
                                                                     0.25],
                                                                    gap="small")

seguro_tasa = tools.OPCIONES_SEGURO_RCC[col_varios_1.selectbox("Seguro mensual",
                                                              list(tools.OPCIONES_SEGURO_RCC.keys()))]
fecha_financiacion = col_varios_2.date_input("Fecha de financiación",
                                             tools.dt.date.today())
dia_pago = col_varios_3.number_input("Día de vencimiento",
                                     min_value=1,
                                     max_value=12,
                                     step=1,
                                     value=2,
                                     help="Se debe indicar el día de pago seleccionado por el cliente")
# ----------------------------------------------------------------------------------------------------------------------
# Segunda sección de inputs: capital financiado, tasa de interés, tipo de cálculo y cuota/vitesse/duración
# ----------------------------------------------------------------------------------------------------------------------
col_varios_5, col_varios_6, col_varios_7, col_varios_8 = st.columns([0.25,
                                                                     0.25,
                                                                     0.25,
                                                                     0.25],
                                                                    gap="small")

capital = col_varios_5.number_input("Importe de financiación (€)",
                                    min_value=0.0,
                                    max_value=1000000.0,
                                    step=250.00,
                                    value=3000.0)
tin = col_varios_6.number_input("TIN anual (%)",
                                min_value=0.0,
                                max_value=30.0,
                                step=0.10,
                                value=21.79)
tipo_calculo = col_varios_7.selectbox("Tipo de cálculo",
                                      ["Seleccionar","Vitesse","Cuota","Duración"])
# Calcular el importe de la cuota mensual en función del tipo de cálculo seleccionado por el usuario.
if tipo_calculo == "Vitesse":
    cuota = tools.rcc_obtener_cuota(capital,col_varios_8.selectbox("Vitesse (%)",
                                                                   tools.RCC_OPCIONES_VITESSE))
elif tipo_calculo == "Cuota":
    cuota = col_varios_8.selectbox("Cuota mensual (€)",
                                   tools.rcc_opciones_cuota(capital))
elif tipo_calculo == "Duración":
    rcc_duraciones, rcc_cuotas = sim.rcc_obtener_duraciones(capital,
                                                            tin,
                                                            fecha_financiacion)    
    cuota = rcc_cuotas[col_varios_8.selectbox("Duración del crédito",
                                              rcc_duraciones)]
else:
    cuota = None
# ----------------------------------------------------------------------------------------------------------------------
# Llamar backend para simular la operación y obtener resultados de la simulación
# ----------------------------------------------------------------------------------------------------------------------
if cuota is not None:
    cuadro_amortización, rcc_resumen, datos_tae = sim.rcc_simulacion_completa(capital,
                                                                              tin,
                                                                              cuota,
                                                                              fecha_financiacion,
                                                                              seguro_tasa,
                                                                              dia_pago)
# ----------------------------------------------------------------------------------------------------------------------
# Exportar resultados de la simulación a Excel
# ----------------------------------------------------------------------------------------------------------------------
    st.download_button(
        label = "📥 Descargar en Excel",
        data = tools.generar_excel(rcc_resumen,
                                   cuadro_amortización,
                                   None,
                                   datos_tae),
        file_name = "simulacion_revolving.xlsx",
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar resultados de la simulación en Streamlit
# ----------------------------------------------------------------------------------------------------------------------
    tab1, tab2, tab3 = st.tabs(["Resumen",
                                "Cuadro de amortización",
                                "Datos TAE"])
    with tab1:
        st.dataframe(rcc_resumen.astype(str))
    with tab2:
        st.dataframe(cuadro_amortización.astype(str),
                     hide_index=True)
    with tab3:
        st.dataframe(datos_tae.astype(str),
                     hide_index=True)
# ----------------------------------------------------------------------------------------------------------------------
# Final de la aplicación
# ----------------------------------------------------------------------------------------------------------------------