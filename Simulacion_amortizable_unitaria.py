#!
# Aplicación Streamlit para simular operaciones de los productos amortizables de COF_ES

import streamlit as st
import bin.COFES__SIM_AMO as sim
import bin.COFES___tools as tools

# ----------------------------------------------------------------------------------------------------------------------
# Título de la aplicación 
# ----------------------------------------------------------------------------------------------------------------------
st.title('Simulador de préstamos amortizables')

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
# Crear la barra lateral con los campos de entrada para la simulación
# ----------------------------------------------------------------------------------------------------------------------
with st.sidebar:
# ----------------------------------------------------------------------------------------------------------------------
# Crear selector del producto amortizable a simular
# ----------------------------------------------------------------------------------------------------------------------
    etiqueta_producto = st.selectbox('Elige el producto contratado:',
                                     tools.LISTA_PRODUCTOS[:14], index=1)
# ----------------------------------------------------------------------------------------------------------------------
    # Crar expander donde mostrar las opciones de fecha de simulación y día de pago
# ----------------------------------------------------------------------------------------------------------------------
    with st.expander("Personalizar las fechas"):
        fecha_financiacion = st.date_input("Fecha de financiación",
                                           tools.dt.date.today())
        dia_pago = st.number_input("Día de vencimiento",
                                   min_value=1,
                                   max_value=12,
                                   step=1,
                                   value=2, 
                                   help="Se debe indicar el día de pago seleccionado por el cliente")
# ----------------------------------------------------------------------------------------------------------------------
    # Mostrar los campos para gestionar la comisión de apertura en los productos que lo permiten
# ----------------------------------------------------------------------------------------------------------------------
    if  tools.LISTA_PRODUCTOS.index(etiqueta_producto) != 1:
        with st.expander("Gestionar la comisión de apertura"):
            tasa_comision_apertura = st.number_input("Porcentaje comisión de apertura",
                                                     min_value=0.00,
                                                     max_value=10.00,
                                                     step=0.05,
                                                     value=0.00,
                                                     help="Se debe indicar el porcentaje de la comisión de apertura a utlizar en la simulación")
            if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (8, 9, 10, 11):
                comision_apertura_capitalizada = st.checkbox("Comisión de apertura capitalizada",
                                                             value=True,
                                                             disabled=True)
            elif tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (12, 13):
                comision_apertura_capitalizada = st.checkbox("Comisión de apertura capitalizada",
                                                             value=True)
            elif tools.LISTA_PRODUCTOS.index(etiqueta_producto) != 0:
                comision_apertura_capitalizada = st.checkbox("Comisión de apertura capitalizada")
            else:
                comision_apertura_capitalizada = False 
            
            imp_max_com_apertura = st.number_input("Importe máximo de la comisión de apertura (EUR)",
                                                   min_value=0.00,
                                                   step=1.00, 
                                                   help="Se debe indicar el importe que no debería superar la comisión de apertura")
    else:
        tasa_comision_apertura = 0.00
        comision_apertura_capitalizada = False
        imp_max_com_apertura = 0.00
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar los campos de tipo de interés, importe a financiar y duración del préstamo
# ----------------------------------------------------------------------------------------------------------------------
    if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (12, 13):
        importe_bien = st.number_input("Importe del bien adquirido (EUR)",
                                       min_value=50.00,
                                       max_value=60000.00,
                                       step=50.00,
                                       value=15000.00, 
                                       help="Se debe indicar el importe del bien adquirido con el préstamo")
        entrega_a_cuenta = st.number_input("Importe entregado a cuenta (EUR)",
                                           min_value=0.00,
                                           max_value=60000.00,
                                           step=50.00,
                                           value=2000.00, 
                                           help="Se debe indicar el importe entregado a cuenta por el cliente")
        capital_prestado = st.number_input("Importe solicitado (EUR)",
                                           value=(importe_bien - entrega_a_cuenta if importe_bien > entrega_a_cuenta else 0),
                                           disabled=True,
                                           help="Se debe indicar el importe del capital solicitado en el préstamo")
    else:
        capital_prestado = st.number_input("Importe solicitado (EUR)",
                                           min_value=50.00,
                                           max_value=60000.00,
                                           step=50.00,
                                           value=1500.00, 
                                           help="Se debe indicar el importe del capital solicitado en el préstamo")
    tasa = st.number_input("Tipo de Interés Deudor",
                           min_value=0.0,
                           max_value=20.00,
                           step=0.05,
                           value=5.95, 
                           help="Se debe indicar el porcentaje del Tipo de Interés Nominal - TIN - a utlizar en la simulación")
    plazo = st.number_input("Nº de mensualidades",
                            min_value=1,
                            max_value=360,
                            step=1,
                            value=12,
                            help="Se debe indicar la duración en meses del plazo de amortización")
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar los campos para gestionar el seguro en los productos que lo permiten
# ----------------------------------------------------------------------------------------------------------------------
    if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 1):
        seguro_tasa = tools.OPCIONES_SEGURO_AMO[st.selectbox("Seguro mensual",
                                                              list(tools.OPCIONES_SEGURO_AMO.keys())[:3], index=2)]
    elif tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (8, 9, 10, 11, 12, 13):
        seguro_tasa = tools.OPCIONES_SEGURO_AMO[st.selectbox("Seguro mensual",
                                                              list(tools.OPCIONES_SEGURO_AMO.keys())[2:], index=0)]
    else:
        seguro_tasa = 0.00
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar el campo para indicar la carencia en los productos que lo permiten
# ----------------------------------------------------------------------------------------------------------------------
    if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 2, 3, 4, 5, 6, 7, 12, 13):
        carencia = st.number_input("Meses de carencia", 
                                   min_value=0,
                                   max_value=4,
                                   step=1, 
                                   help="Se debe indicar la duración de la carencia total inicial")
    else:
        carencia = 0
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar los campos para gestionar la segunda secuencia financiera en los productos que lo permiten
# ----------------------------------------------------------------------------------------------------------------------
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
                capital_2sec = round((importe_bien if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (12, 13) else capital_prestado) * st.number_input("Porcentaje a amortizar en la segunda secuencia (%)", 
                                                                        min_value=5.00, max_value=70.00, step=5.00, value=30.00, 
                                                                        help="Se debe indicar el porcentaje del capital a amortizar en la segunda secuencia del OPTION+")/100, 2)
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
        tasa_2sec = 0.00
        capital_2sec = 0
        plazo_2sec = 0

# ----------------------------------------------------------------------------------------------------------------------
# Mostra el resultado de la simulación
# ----------------------------------------------------------------------------------------------------------------------
if st.session_state.get("simular", True):
# ----------------------------------------------------------------------------------------------------------------------
# Llamar backend para simular la operación y obtener resultados de la simulación
# ----------------------------------------------------------------------------------------------------------------------
    (resumen1,
     resumen2,
     resumen3,
     ejemplo_representativo,
     cuadro_amortizacion,
     input_tae) = sim.visualizar_simulacion_unitaria(etiqueta_producto,
                                                     fecha_financiacion,
                                                     dia_pago,
                                                     tasa,
                                                     capital_prestado,
                                                     plazo,
                                                     carencia,
                                                     tasa_2sec,
                                                     capital_2sec,
                                                     plazo_2sec,
                                                     seguro_tasa,
                                                     tasa_comision_apertura,
                                                     comision_apertura_capitalizada,
                                                     imp_max_com_apertura)
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar resumen de la simulación
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Detallar las características del producto amortizable de la simulación
# ----------------------------------------------------------------------------------------------------------------------
    with st.expander(f"Características del producto {etiqueta_producto}",
                     expanded=False):
        # Filtrar el dataframe "tools.DICCIONARIO_PRODUCTOS" con el producto seleccionado en la simulación
        producto_info = tools.DICCIONARIO_PRODUCTOS[tools.DICCIONARIO_PRODUCTOS["Nombre del producto"] == etiqueta_producto]
        
        st.dataframe(producto_info.T,
                     width='stretch')
           
        # Recordatorio de que la primera mensualidad de los productos Vorwerk financiado no puede superar la mensualidad contractual
        if tools.LISTA_PRODUCTOS.index(etiqueta_producto) == 3:
            st.warning('Para evitar que la primera mensualidad supere la cuota contractual, la carencia diferida tiene un tipo de interés del 0,00 % y, si el contrato es financiado entre fecha de bloqueo y fecha de vencimiento, se crea una carencia diferida forzada entre la fecha de financiación y la primera fecha de vencimiento teórica posible.', icon="⚠️")
            st.toast('Para evitar que la primera mensualidad supere la cuota contractual, la carencia diferida tiene un tipo de interés del 0,00 % y, si el contrato es financiado entre fecha de bloqueo y fecha de vencimiento, se crea una carencia diferida forzada entre la fecha de financiación y la primera fecha de vencimiento teórica posible.', icon="⚠️")
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar el resumen económico de la simulación
# ----------------------------------------------------------------------------------------------------------------------
    if resumen1 is None:
         st.error(ejemplo_representativo,
                  icon="❌")
    else:
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
# ----------------------------------------------------------------------------------------------------------------------
# Exportar resultados de la simulación a Excel
# ----------------------------------------------------------------------------------------------------------------------    
        st.download_button(
            label="📥 Descargar en Excel",
            data=tools.generar_excel(resumen2,
                                     cuadro_amortizacion,
                                     tools.pd.DataFrame({'TAE': [resumen1.at['%','TAE']],
                                                         'Ejemplo representativo': [ejemplo_representativo]}),
                                     input_tae,
                                     resumen3),
            file_name="simulacion_amortizable.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar resultados de la simulación en Streamlit
# ----------------------------------------------------------------------------------------------------------------------
        tab1, tab2, tab3, tab4 = st.tabs(["Secuencias financieras",
                                          "Ejemplo representativo",
                                          "Cuadro de amortización",
                                          "Detalle TAE"])
        with tab1:
            html_table = resumen3.to_html(classes='table table-right',
                                          index=True)
            st.markdown(html_table,
                        unsafe_allow_html=True)
        with tab2:
            st.code(ejemplo_representativo,
                    wrap_lines=True)
        with tab3:
            st.dataframe(cuadro_amortizacion,
                         hide_index=True)
        with tab4:
            st.dataframe(input_tae,
                         hide_index=True)
# ----------------------------------------------------------------------------------------------------------------------
# Final de la aplicación
# ---------------------------------------------------------------------------------------------------------------------- 