#!
# Aplicación Streamlit para simular operaciones de los productos amortizables de COF_ES



# Importar los módulos a utilizar en la aplicación

import streamlit as st
import datetime  as dt
import pandas as pd
import COFES__SIM_AMO_Consola as sim



#  Declarar las listas de productos tanto de crédito como de seguro

LISTA_SEGURO = sim.LISTA_SEGURO
LISTA_PRODUCTOS = sim.LISTA_PRODUCTOS
PRODUCTOS_DICCIONARIO = sim.PRODUCTOS_DICCIONARIO



# Convertir el diccionario de productos en un dataframe para facilitar su manejo

productos_descripcion = pd.DataFrame(PRODUCTOS_DICCIONARIO)



# Inicializar variables

carencia = 0
tasa_2SEC = 0.00
capital_2SEC = 0
plazo_2SEC = 0
seguro_titular_1 = "SIN SEGURO"
seguro_titular_2 = "SIN SEGURO"
tasa_comision_apertura = 0.0
comision_apertura_capitalizada = False
imp_max_com_apertura = 0.0
fecha_financiacion = dt.date.today()
dia_pago = 2
etiqueta_producto = LISTA_PRODUCTOS[1]
on = False



#  Iniciar la aplicación / Configuración del título y de la barra lateral / CSS

st.title('Simulador de préstamos amortizables')
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



# Crear barra lateral donde se introducen los datos de la simulación

with st.sidebar:



    # Crear selector del producto amortizable a simular

    etiqueta_producto = st.selectbox('Elige el producto contratado:', LISTA_PRODUCTOS, index=1)



    # Mostrar las opciones de fecha de simulación y día de pago

    with st.expander("Personalizar las fechas"):
        fecha_financiacion = st.date_input("Fecha de financiación", dt.date.today())
        dia_pago = st.number_input("Día de vencimiento", 
                                   min_value=1, max_value=12, step=1, value=2, 
                                   help="Se debe indicar el día de pago seleccionado por el cliente")



    # Mostrar los campos para gestionar el seguro en los productos que lo permiten

    if LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 1, 8, 9, 10, 11):
        with st.expander("Gestionar el seguro"):
            if LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 1):
                seguro_titular_1 = st.selectbox("Seguro titular 1", LISTA_SEGURO[:2], index=1)
                seguro_titular_2 = st.selectbox("Seguro titular 2", LISTA_SEGURO[:2], index=1)
            else:
                seguro_titular_1 = st.selectbox("Seguro titular 1", LISTA_SEGURO[1:], index=0)
                seguro_titular_2 = st.selectbox("Seguro titular 2", LISTA_SEGURO[1:], index=0)



    # Mostrar los campos para gestionar la comisión de apertura en los productos que lo permiten

    if  LISTA_PRODUCTOS.index(etiqueta_producto) != 1:
        with st.expander("Gestionar la comisión de apertura"):
            tasa_comision_apertura = st.number_input("Porcentaje comisión de apertura", 
                                                     min_value=0.00, max_value=5.00, step=0.05, 
                                                     help="Se debe indicar el porcentaje de la comisión de apertura a utlizar en la simulación")
            
            if LISTA_PRODUCTOS.index(etiqueta_producto) in (8, 9, 10, 11):
                comision_apertura_capitalizada = st.checkbox("Comisión de apertura capitalizada",
                                                             value=True, disabled=True)
            elif LISTA_PRODUCTOS.index(etiqueta_producto) in (2, 3, 4, 5, 6, 7):
                comision_apertura_capitalizada = st.checkbox("Comisión de apertura capitalizada")
            
            imp_max_com_apertura = st.number_input("Importe máximo de la comisión de apertura (EUR)", 
                                                   min_value=0.00, step=1.00, 
                                                   help="Se debe indicar el importe que no debería superar la comisión de apertura")



    # Mostrar los campos de tipo de interés, importe a financiar y duración del préstamo
    tasa = st.number_input("Tipo de Interés Deudor", 
                           min_value=0.0, max_value=20.00, step=0.05, value=5.95, 
                           help="Se debe indicar el porcentaje del Tipo de Interés Nominal - TIN - a utlizar en la simulación")
    capital_prestado = st.number_input("Importe solicitado (EUR)", 
                                       min_value=50.00, max_value=60000.00, step=50.00, value=1500.00, 
                                       help="Se debe indicar el importe del capital solicitado en el préstamo")
    plazo = st.number_input("Nº de mensualidades", 
                            min_value=3, max_value=120, step=1, value=12, 
                            help="Se debe indicar la duración en meses del plazo de amortización")



    # Mostrar el campo para indicar la carencia en los productos que lo permiten
    if LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 2, 3, 4, 5, 6, 7):
        carencia = st.number_input("Meses de carencia", 
                                   min_value=0, max_value=4, step=1, 
                                   help="Se debe indicar la duración de la carencia total inicial")



    # Mostrar los campos para gestionar la segunda secuencia financiera en los productos que lo permiten
    if LISTA_PRODUCTOS.index(etiqueta_producto) in (6, 7):
        with st.expander("Gestionar la segunda secuencia financiera", expanded=True):
            on = st.toggle("Cuota residual porcentual")
            tasa_2SEC = st.number_input("Tipo de Interés Deudor", 
                                        min_value=0.0, max_value=20.00, step=0.05, value=0.00, 
                                        help="Se debe indicar el porcentaje del TIN a aplicar en la segunda secuencia")
            if on:
                capital_2SEC = round(capital_prestado * st.number_input("Porcentaje a amortizar en la segunda secuencia (%)", 
                                                                        min_value=5.00, max_value=70.00, step=5.00, value=30.00, 
                                                                        help="Se debe indicar el porcentaje del capital a amortizar en la segunda secuencia del OPTION+")/100, 2)
            else:
                capital_2SEC = st.number_input("Importe a amortizar en la segunda secuencia (EUR)", 
                                               min_value=50.00, max_value=30000.00, step=50.00, 
                                               help="Se debe indicar el importe del capital a amortizar en la segunda secuencia del OPTION+")
            plazo_2SEC = st.number_input("Duración de la segunda secuencia", 
                                         min_value=1, max_value=60, step=1, 
                                         help="Se debe indicar la duración en meses del segundo tramo de amortización")   



# Mostra el resultado de la simulación

if st.session_state.get("simular", True):



    # Obtener los resultados de la simulación llamando a la función visualizar_simulacion_unitaria de la librería COFES_SIM_AMO_Consola

    resumen1, resumen2, resumen3, ejemplo_representativo, cuadro_amortizacion, input_TAE = sim.visualizar_simulacion_unitaria(etiqueta_producto,
                                                                                                                              fecha_financiacion,
                                                                                                                              dia_pago,
                                                                                                                              tasa,
                                                                                                                              capital_prestado,
                                                                                                                              plazo,
                                                                                                                              carencia,
                                                                                                                              tasa_2SEC,
                                                                                                                              capital_2SEC,
                                                                                                                              plazo_2SEC,
                                                                                                                              seguro_titular_1,
                                                                                                                              seguro_titular_2,
                                                                                                                              tasa_comision_apertura,
                                                                                                                              comision_apertura_capitalizada,
                                                                                                                              imp_max_com_apertura)



    # Mostrar resumen de la simulación
    
    # Detallar las características del producto amortizable de la simulación

    with st.expander(f"Características del producto {etiqueta_producto}", expanded=False):
        # Filtrar el dataframe "productos_descripcion" con el producto seleccionado en la simulación
        producto_info = productos_descripcion[productos_descripcion["Nombre del producto"] == etiqueta_producto]
        
        st.dataframe(producto_info.T, width='stretch')
           
        # Recordatorio de que la primera mensualidad de los productos Vorwerk financiado no puede superar la mensualidad contractual

        if LISTA_PRODUCTOS.index(etiqueta_producto) in (3, 5):
            st.markdown(":orange-badge[⚠️ Si el contrato es financiado entre fecha de bloqueo y fecha de vencimiento, se crea una carencia diferida con tipo de interés 0% para evitar que la primera mensualidad supere la cuota contractual]")



    # Mostrar el resumen económico de la simulación

    with st.expander("", expanded=True):
        col1, col2 = st.columns([0.08, 0.92], gap="small")
        html_table1 = resumen1.to_html(classes='table table-right', index=True)
        html_table2 = resumen2.to_html(classes='table table-right', index=True)

        col1.markdown(html_table1, unsafe_allow_html=True)
        col2.markdown(html_table2, unsafe_allow_html=True)



    # Mostrar las pestañas con los detalles de la simulación

    tab1, tab2, tab3, tab4 = st.tabs(["Secuencias financieras", "Ejemplo representativo", "Cuadro de amortización", "Detalle TAE"])



    # Mostrar contenido de la pestaña Secuencias financieras

    with tab1:
        html_table = resumen3.to_html(classes='table table-right', index=True)
        st.markdown(html_table, unsafe_allow_html=True)



    # Mostrar contenido de la pestaña "Ejemplo representativo"

    with tab2:
        st.code(ejemplo_representativo, wrap_lines=True)



    # Mostrar contenido de la pestaña "Cuadro de amortización"

    with tab3:
        st.dataframe(cuadro_amortizacion,hide_index=True)



    # Mostrar contenido de la pestaña "Detalle TAE"

    with tab4:
        st.dataframe(input_TAE,hide_index=True)



# Final de la aplicación