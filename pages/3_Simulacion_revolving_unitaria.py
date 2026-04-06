#!
# Aplicación Streamlit para simular operaciones de los productos revolving de COF_ES

import streamlit as st
import bin.COFES__SIM_RCC as sim
import bin.COFES___tools as tools

# ----------------------------------------------------------------------------------------------------------------------
# Título de la aplicación y aviso de funcionalidad en construcción
# ----------------------------------------------------------------------------------------------------------------------
st.title('Simulador Revolving con Seguro Opcional')
st.info('Funcionalidad en pruebas', icon="⚠️")

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
col_varios_1, col_varios_2, col_varios_3, col_varios_4 = st.columns([0.25, 0.25, 0.25, 0.25], gap="small")

seguro_tasa = tools.OPCIONES_SEGURO[col_varios_1.selectbox("Seguro mensual",
                                                     list(tools.OPCIONES_SEGURO.keys()))]
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
col_varios_5, col_varios_6, col_varios_7, col_varios_8 = st.columns([0.25, 0.25, 0.25, 0.25],gap="small")

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

if tipo_calculo == "Vitesse":
    valor = col_varios_8.selectbox("Vitesse (%)",tools.VITESSE_VALORES)
elif tipo_calculo == "Cuota":
    valor = col_varios_8.selectbox("Cuota mensual (€)",tools.rcc_opciones_cuota(capital))
elif tipo_calculo == "Duración":
    opciones_duracion = []
    mapa_vitesse = {}
    for v in tools.VITESSE_VALORES:
        cuota_test = round(capital*v/100,2)
        tabla_test = sim.simulador(capital,tin,"Cuota",cuota_test,fecha_financiacion,0)
        meses = len(tabla_test)
        etiqueta = f"{meses} meses"
        opciones_duracion.append(etiqueta)
        mapa_vitesse[etiqueta] = v
    seleccion = col_varios_8.selectbox("Duración del préstamo",opciones_duracion)
    valor = mapa_vitesse[seleccion]
    tipo_calculo = "Vitesse"
else:
    valor = None

# ----------------------------------------------------------------------------------------------------------------------
# Llamar backend para simular la operación y obtener resultados de la simulación
# ----------------------------------------------------------------------------------------------------------------------
if valor is not None:
    cuadro_amortización, rcc_resumen = sim.simulador(capital, tin, tipo_calculo, valor, fecha_financiacion, seguro_tasa)

# ----------------------------------------------------------------------------------------------------------------------
# Exportar resultados de la simulación a Excel
# ----------------------------------------------------------------------------------------------------------------------
    st.download_button(
        label = "📥 Descargar en Excel",
        data = tools.generar_excel(rcc_resumen, cuadro_amortización),
        file_name = "simulacion_revolving.xlsx",
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar resultados de la simulación en Streamlit
# ----------------------------------------------------------------------------------------------------------------------
    tab1, tab2, = st.tabs(["Resumen", "Cuadro de amortización"])
    
    with tab1:
        st.dataframe(rcc_resumen.astype(str))

    with tab2:
        st.dataframe(cuadro_amortización.astype(str),hide_index=True)

# ----------------------------------------------------------------------------------------------------------------------
# Final de la aplicación
# ----------------------------------------------------------------------------------------------------------------------