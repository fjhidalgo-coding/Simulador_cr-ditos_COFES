#!
# Aplicación Streamlit para simular masivamente operaciones de los productos amortizables de COF_ES

import streamlit as st
import bin.COFES__SIM_AMO as sim
import bin.COFES___tools as tools

# ----------------------------------------------------------------------------------------------------------------------
# Título de la aplicación 
# ----------------------------------------------------------------------------------------------------------------------
st.title('Simulador masivo de préstamos amortizables')
# ----------------------------------------------------------------------------------------------------------------------
# Definir la configuración de la página y estilos personalizados
# ----------------------------------------------------------------------------------------------------------------------
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
# ----------------------------------------------------------------------------------------------------------------------
# Primera sección de inputs: producto, día de pago, fecha de financiación y seguro
# ----------------------------------------------------------------------------------------------------------------------
col_sim_1, col_sim_2, col_sim_3, col_sim_4 = st.columns([0.25,
                                                         0.25,
                                                         0.25,
                                                         0.25],
                                                        gap="small")
etiqueta_producto = col_sim_1.selectbox('Elige el producto contratado:',
                                        tools.LISTA_PRODUCTOS[:14],
                                        index=1)
dia_pago = col_sim_2.number_input("Día de vencimiento",
                                  min_value=1,
                                  max_value=12,
                                  step=1,
                                  value=2,
                                  help="Se debe indicar el día de pago seleccionado por el cliente")
fecha_financiacion = col_sim_3.date_input("Fecha de financiación",
                                          tools.dt.date.today())
if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 1):
    seguro_tasa = tools.OPCIONES_SEGURO_AMO[col_sim_4.selectbox("Seguro mensual",
                                                                list(tools.OPCIONES_SEGURO_AMO.keys())[:3], index=2)]
elif tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (8, 9, 10, 11, 12, 13):
    seguro_tasa = tools.OPCIONES_SEGURO_AMO[col_sim_4.selectbox("Seguro mensual",
                                                                list(tools.OPCIONES_SEGURO_AMO.keys())[2:], index=0)]
else:
    seguro_tasa = 0.00
# ----------------------------------------------------------------------------------------------------------------------
# Detalle del producto de préstamo seleccionado
# ----------------------------------------------------------------------------------------------------------------------
with st.expander(f"Características del producto {etiqueta_producto}",
                 expanded=False):
    # Filtrar el dataframe "tools.DICCIONARIO_PRODUCTOS" con el producto seleccionado en la simulación
    producto_info = tools.DICCIONARIO_PRODUCTOS[tools.DICCIONARIO_PRODUCTOS["Nombre del producto"] == etiqueta_producto]
    st.dataframe(producto_info.T,
                 width='stretch')
    # Recordatorio de que la primera mensualidad de los productos Vorwerk financiado no puede superar la mensualidad contractual
    if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (3, 5):
        st.markdown(":orange-badge[⚠️ Si el contrato es financiado entre fecha de bloqueo y fecha de vencimiento, se crea una carencia diferida con tipo de interés 0% para evitar que la primera mensualidad supere la cuota contractual]")
# ----------------------------------------------------------------------------------------------------------------------
# Segunda sección de inputs: tipo de interés, comisión de apertura y campos asociados a la comisión de apertura
# ----------------------------------------------------------------------------------------------------------------------
col_varios_1, col_varios_2, col_varios_3, col_varios_4 = st.columns([0.25,
                                                                     0.25,
                                                                     0.25,
                                                                     0.25],
                                                                    gap="small")
tasa = col_varios_1.number_input("Tipo de Interés Deudor",
                                 min_value=0.0,
                                 max_value=20.00,
                                 step=0.05,
                                 value=5.95,
                                 help="Se debe indicar el porcentaje del Tipo de Interés Nominal - TIN - a utlizar en la simulación")
if  tools.LISTA_PRODUCTOS.index(etiqueta_producto) != 1:
    tasa_comision_apertura = col_varios_2.number_input("Porcentaje comisión de apertura",
                                                       min_value=0.00,
                                                       max_value=5.00,
                                                       step=0.05,
                                                       help="Se debe indicar el porcentaje de la comisión de apertura a utlizar en la simulación")
    imp_max_com_apertura = col_varios_3.number_input("Importe máximo de la comisión de apertura (EUR)",
                                                     min_value=0.00,
                                                     step=1.00,
                                                     help="Se debe indicar el importe que no debería superar la comisión de apertura")
    if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (8, 9, 10, 11):
        comision_apertura_capitalizada = col_varios_4.checkbox("Comisión de apertura capitalizada",
                                                               value=True,
                                                               disabled=True)      
    elif tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (12, 13):
        comision_apertura_capitalizada = col_varios_4.checkbox("Comisión de apertura capitalizada",
                                                               value=True)
    elif tools.LISTA_PRODUCTOS.index(etiqueta_producto) == 0:
        comision_apertura_capitalizada = False
    else:
        comision_apertura_capitalizada = col_varios_4.checkbox("Comisión de apertura capitalizada")
else:
    tasa_comision_apertura = tools.redondear_decimal(0.00)
    comision_apertura_capitalizada = False
    imp_max_com_apertura = tools.redondear_decimal(0.00)
# ----------------------------------------------------------------------------------------------------------------------
# Tercera sección de inputs: Importes prestados, plazos, carencias y campos asociados a la segunda secuencia financiera
# ----------------------------------------------------------------------------------------------------------------------
if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (12, 13):
    col_val_1, col_val_2, col_val_3, col_val_4 = st.columns([0.40,
                                                             0.20,
                                                             0.20,
                                                             0.20],
                                                            gap="small")
    importes_prestado = col_val_1.slider("Rango del bien adquirido (EUR)",
                                         min_value=3000.00,
                                         max_value=60000.00,
                                         step=500.00,
                                         value=[4500.00,9500.00],
                                         help="Se debe indicar el importe del capital solicitado en el préstamo")
    entrega_a_cuenta = col_val_2.number_input("Importe entregado a cuenta (EUR)",
                                              min_value=0.00,
                                              max_value=60000.00,
                                              step=50.00,
                                              value=2000.00,
                                              help="Se debe indicar el importe entregado a cuenta por el cliente")
    plazos = col_val_3.slider("Rango de mensualidades a simular",
                              min_value=12,
                              max_value=360,
                              step=12,
                              value=[24, 60],
                              help="Se debe indicar la duración en meses del plazo de amortización")
else:
    col_val_1, col_val_2, col_val_3 = st.columns([0.34,
                                                  0.33,
                                                  0.33],
                                                 gap="small")
    if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 1, 8, 9, 10, 11):
        importes_prestado = col_val_1.slider("Rango de importe solicitado (EUR)",
                                             min_value=3000.00,
                                             max_value=60000.00,
                                             step=500.00,
                                             value=[4500.00,9500.00],
                                             help="Se debe indicar el importe del capital solicitado en el préstamo")
        plazos = col_val_2.slider("Rango de mensualidades a simular",
                                  min_value=12,
                                  max_value=360,
                                  step=12,
                                  value=[24, 60],
                                  help="Se debe indicar la duración en meses del plazo de amortización")
        entrega_a_cuenta = 0.00
    else:
        importes_prestado = col_val_1.slider("Rango de importe solicitado (EUR)",
                                             min_value=50.00,
                                             max_value=12000.00,
                                             step=50.00,
                                             value=[500.00,1500.00],
                                             help="Se debe indicar el importe del capital solicitado en el préstamo")
        plazos = col_val_2.slider("Rango de mensualidades a simular",
                                  min_value=1,
                                  max_value=120,
                                  step=1,
                                  value=[12, 60],
                                  help="Se debe indicar la duración en meses del plazo de amortización")
        entrega_a_cuenta = 0.00
# Mostrar el campo para indicar la carencia en los productos que lo permiten
if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 2, 3, 4, 5, 6, 7):
    carencias = col_val_3.slider("Rango de meses de carencia",
                                 min_value=0,
                                 max_value=4,
                                 step=1,
                                 value=[0, 0],
                                 help="Se debe indicar la duración de la carencia total inicial")
elif tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (12, 13):
    carencias = col_val_4.slider("Rango de meses de carencia",
                                 min_value=0,
                                 max_value=4,
                                 step=1,
                                 value=[0, 0],
                                 help="Se debe indicar la duración de la carencia total inicial")
else:
    carencias = [0,]
# Mostrar los campos para gestionar la segunda secuencia financiera en los productos que lo permiten
if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (6, 7, 12, 13):
    with st.expander("Gestionar la segunda secuencia financiera",
                     expanded=True):
        on = st.toggle("Cuota residual porcentual")
        tasa_2sec = st.number_input("Tipo de Interés Deudor",
                                    min_value=0.0,
                                    max_value=20.00,
                                    step=0.05,
                                    value=0.00,
                                    help="Se debe indicar el porcentaje del TIN a aplicar en la segunda secuencia")
        if on:
            capital_2sec = st.number_input("Porcentaje a amortizar en la segunda secuencia (%)",
                                           min_value=5.00,
                                           max_value=70.00,
                                           step=5.00,
                                           value=30.00,
                                           help="Se debe indicar el porcentaje del capital a amortizar en la segunda secuencia del OPTION+")
        else:
            capital_2sec = st.number_input("Importe a amortizar en la segunda secuencia (EUR)",
                                           min_value=50.00,
                                           max_value=30000.00,
                                           step=50.00, 
                                           help="Se debe indicar el importe del capital a amortizar en la segunda secuencia del OPTION+")
        plazo_2sec = st.number_input("Duración de la segunda secuencia",
                                     min_value=1,
                                     max_value=60,
                                     step=1, 
                                     help="Se debe indicar la duración en meses del segundo tramo de amortización")   
else:
    tasa_2sec = tools.redondear_decimal(0.00)
    capital_2sec = tools.redondear_decimal(0.00)
    plazo_2sec = 0
    on = False
# ----------------------------------------------------------------------------------------------------------------------
# Llamar backend para simular la operación y obtener resultados de la simulación
# ----------------------------------------------------------------------------------------------------------------------
st.subheader("Resumen de los datos a simular")
if st.button("Simular"):
    with st.spinner("Simulando..."):
        resultado_simulacion_masiva, errores_simulacion_masiva = sim.simular_masivamente(capital_2sec,
                                                                                         carencias,
                                                                                         comision_apertura_capitalizada,
                                                                                         dia_pago,
                                                                                         entrega_a_cuenta,
                                                                                         etiqueta_producto,
                                                                                         fecha_financiacion,
                                                                                         imp_max_com_apertura,
                                                                                         importes_prestado,
                                                                                         on,
                                                                                         plazo_2sec,
                                                                                         plazos,
                                                                                         seguro_tasa,
                                                                                         tasa,
                                                                                         tasa_2sec,
                                                                                         tasa_comision_apertura)
    st.success("Simulación masiva completada")
# ----------------------------------------------------------------------------------------------------------------------
# Exportar resultados de la simulación a Excel
# ----------------------------------------------------------------------------------------------------------------------
    st.download_button(
                label="📥 Descargar en Excel",
                data=tools.generar_excel(resultado_simulacion_masiva=resultado_simulacion_masiva,
                                         df_errores=errores_simulacion_masiva),
                file_name="simulacion_AMO_masiva.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar resultados de la simulación en Streamlit
# ----------------------------------------------------------------------------------------------------------------------
    st.dataframe(resultado_simulacion_masiva,
                 hide_index=True)
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar los errores de la simulación en Streamlit en caso de que existan errores en algunos registros
# ----------------------------------------------------------------------------------------------------------------------
    if not errores_simulacion_masiva.empty:
        st.error(f"Se han descartado {len(errores_simulacion_masiva)} registros con error en la simulación.")
        st.dataframe(errores_simulacion_masiva,
                     hide_index=True)
# ----------------------------------------------------------------------------------------------------------------------
# Final de la aplicación
# ----------------------------------------------------------------------------------------------------------------------