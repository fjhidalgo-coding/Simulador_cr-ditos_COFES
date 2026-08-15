#!
# Aplicación Streamlit para simular operaciones de los productos amortizables

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
            width: 250px !important; # Set the width to your desired value
        }
        .table-right td, .table-right th {
            text-align: right !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
# ----------------------------------------------------------------------------------------------------------------------
# ********BLOQUE COMÚN******** DE INPUTS PARA LA SIMULACIÓN UNITARIA Y MASIVA
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Primera sección de inputs: tipo de simulación, selección del producto, día de pago, fecha de financiación y seguro
# ----------------------------------------------------------------------------------------------------------------------
col_sim_1, col_sim_2, col_sim_3, col_sim_4, col_sim_5 = st.columns([0.25,
                                                                    0.25,
                                                                    0.15,
                                                                    0.15,
                                                                    0.20],
                                                                    gap="small")
# ----------------------------------------------------------------------------------------------------------------------    
# Toggle para seleccionar entre simulación unitaria o masiva
# ----------------------------------------------------------------------------------------------------------------------    
on_masiva = col_sim_1.toggle("Simulación masiva",
                             value=False,
                             key="toggle_amortizable",
                             help="Se debe activar el toggle para realizar una simulación masiva de los productos amortizables")
# ----------------------------------------------------------------------------------------------------------------------    
# Menú desplegable para seleccionar el producto a simular
# ----------------------------------------------------------------------------------------------------------------------    
etiqueta_producto = col_sim_2.selectbox('Elige el producto contratado:',
                                        tools.LISTA_PRODUCTOS[:14],
                                        index=1)
if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (6, 7, 12, 13):
    on_residual_porcentual = col_sim_1.toggle("Cuota residual porcentual",
                                              value=False,
                                              key="toggle_residual_porcentual",
                                              help="Se debe activar el toggle para calcular la segunda secuencia financiera en base a un porcentaje del capital a amortizar en lugar de un importe fijo")
    if on_residual_porcentual and tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (6, 7):
        on_porcentual_compra = col_sim_1.toggle("% sobre el bien adquirido",
                                                value=False,
                                                key="toggle_porcentual_compra",
                                                help="Se debe activar el toggle para calcular la segunda secuencia financiera en base a un porcentaje del importe del bien adquirido en lugar de un porcentaje del capital a amortizar")
    else:
        on_porcentual_compra = False
else:
    on_residual_porcentual = False
    on_porcentual_compra = False
# ----------------------------------------------------------------------------------------------------------------------    
# Input para seleccionar el día de pago y la fecha de financiación
# ----------------------------------------------------------------------------------------------------------------------    
dia_pago = col_sim_3.number_input("Día de vencimiento",
                                  min_value=1,
                                  max_value=12,
                                  step=1,
                                  value=2,
                                  help="Se debe indicar el día de pago seleccionado por el cliente")
# ----------------------------------------------------------------------------------------------------------------------    
# Input para seleccionar la fecha de financiación
# ----------------------------------------------------------------------------------------------------------------------    
fecha_financiacion = col_sim_4.date_input("Fecha de financiación",
                                          tools.dt.date.today())
# ----------------------------------------------------------------------------------------------------------------------    
# Menú desplegable para seleccionar el seguro mensual en los productos que lo permiten
# ----------------------------------------------------------------------------------------------------------------------    
if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 1):
    seguro_tasa = tools.OPCIONES_SEGURO_AMO[col_sim_5.selectbox("Seguro mensual",
                                                                list(tools.OPCIONES_SEGURO_AMO.keys())[:3], index=2)]
elif tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (8, 9, 10, 11, 12, 13):
    seguro_tasa = tools.OPCIONES_SEGURO_AMO[col_sim_5.selectbox("Seguro mensual",
                                                                list(tools.OPCIONES_SEGURO_AMO.keys())[2:], index=0)]
else:
    seguro_tasa = 0.00
# ----------------------------------------------------------------------------------------------------------------------
# Segunda sección de inputs: tasa, opciones de la comisión de apertura y entrega a cuenta de los productos "Ballon"
# ----------------------------------------------------------------------------------------------------------------------
col_sim_6, col_sim_7, col_sim_8, col_sim_9, col_sim_10 = st.columns([0.20,
                                                                    0.20,
                                                                    0.20,
                                                                    0.20,
                                                                    0.20],
                                                                    gap="small")
# ----------------------------------------------------------------------------------------------------------------------    
# Input para seleccionar el tipo de interés deudor, opciones de la comisión de apertura y 
# ----------------------------------------------------------------------------------------------------------------------    
tasa = col_sim_6.number_input("Tipo de Interés Deudor",
                              min_value=0.0,
                              max_value=20.00,
                              step=0.05,
                              value=5.95, 
                              help="Se debe indicar el porcentaje del Tipo de Interés Nominal - TIN - a utlizar en la simulación")
# ----------------------------------------------------------------------------------------------------------------------    
# Mostrar los campos para gestionar la comisión de apertura en los productos que lo permiten
# ----------------------------------------------------------------------------------------------------------------------    
if  tools.LISTA_PRODUCTOS.index(etiqueta_producto) == 1:
    tasa_comision_apertura = 0.00
    comision_apertura_capitalizada = False
    imp_max_com_apertura = 0.00
else:
    tasa_comision_apertura = col_sim_7.number_input("Porcentaje comisión de apertura",
                                                    min_value=0.00,
                                                    max_value=10.00,
                                                    step=0.05,
                                                    value=0.00,
                                                    help="Se debe indicar el porcentaje de la comisión de apertura a utlizar en la simulación")
    imp_max_com_apertura = col_sim_8.number_input("Imp. máx. de la com. de apertura",
                                                  min_value=0.00,
                                                  step=1.00, 
                                                  help="Se debe indicar el importe que no debería superar la comisión de apertura")
    if tools.LISTA_PRODUCTOS.index(etiqueta_producto) == 0:
        comision_apertura_capitalizada = False 
    elif tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (8, 9, 10, 11):
        comision_apertura_capitalizada = col_sim_9.checkbox("Com. Apert. capitalizada",
                                                            value=True,
                                                            disabled=True)
    elif tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (12, 13):
        comision_apertura_capitalizada = col_sim_9.checkbox("Com. Apert. capitalizada",
                                                            value=True)
    else:
        comision_apertura_capitalizada = col_sim_9.checkbox("Com. Apert. capitalizada")

if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (12, 13) or on_porcentual_compra == True:
    entrega_a_cuenta = col_sim_10.number_input("Imp. entregado a cuenta (EUR)",
                                               min_value=0.00,
                                               max_value=60000.00,
                                               step=50.00,
                                               value=2000.00, 
                                               help="Se debe indicar el importe entregado a cuenta por el cliente")
else:
    entrega_a_cuenta = 0.00

# ----------------------------------------------------------------------------------------------------------------------
# ********BLOQUE SIMULACION UNITARIA********
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Bloque de inputs para la simulación unitaria
# ----------------------------------------------------------------------------------------------------------------------
if on_masiva is False:
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar los campos de tipo de interés, importe a financiar y duración del préstamo
# ----------------------------------------------------------------------------------------------------------------------
    col_sim_11, col_sim_12, col_sim_13, col_sim_14 = st.columns([0.25,
                                                                 0.25,
                                                                 0.25,
                                                                 0.25],
                                                                 gap="small")
    if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (12, 13) or on_porcentual_compra == True:
        importe_bien = col_sim_11.number_input("Importe del bien adquirido (EUR)",
                                               min_value=50.00,
                                               max_value=60000.00,
                                               step=50.00,
                                               value=15000.00, 
                                               help="Se debe indicar el importe del bien adquirido con el préstamo")
        capital_prestado = col_sim_14.number_input("Importe solicitado (EUR)",
                                                   value=(importe_bien - entrega_a_cuenta if importe_bien > entrega_a_cuenta else 0),
                                                   disabled=True,
                                                   help="Se debe indicar el importe del capital solicitado en el préstamo")
    else:
        capital_prestado = col_sim_11.number_input("Importe solicitado (EUR)",
                                                   min_value=50.00,
                                                   max_value=60000.00,
                                                   step=50.00,
                                                   value=1500.00, 
                                                   help="Se debe indicar el importe del capital solicitado en el préstamo")
    plazo = col_sim_12.number_input("Nº de mensualidades",
                                    min_value=1,
                                    max_value=360,
                                    step=1,
                                    value=12,
                                    help="Se debe indicar la duración en meses del plazo de amortización")
# ----------------------------------------------------------------------------------------------------------------------
# Mostrar el campo para indicar la carencia en los productos que lo permiten
# ----------------------------------------------------------------------------------------------------------------------
    if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 2, 3, 4, 5, 6, 7, 12, 13):
        carencia = col_sim_13.number_input("Meses de carencia",
                                           min_value=0,
                                           max_value=4,
                                           step=1, 
                                           help="Se debe indicar la duración de la carencia total inicial")
    else:
        carencia = 0

# ----------------------------------------------------------------------------------------------------------------------
# ********BLOQUE SIMULACION MASIVA********
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    # Tercera sección de inputs: Importes prestados, plazos y carencias
# ----------------------------------------------------------------------------------------------------------------------
else:
    col_val_1, col_val_2, col_val_3 = st.columns([0.34,
                                                  0.33,
                                                  0.33],
                                                  gap="small")
# ----------------------------------------------------------------------------------------------------------------------
        # Importe del capital en base al bien adquirido en los productos que lo permiten y rango de mensualidades a simular
# ----------------------------------------------------------------------------------------------------------------------
    if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (12, 13) or on_porcentual_compra == True:
        importes_prestado = col_val_1.slider("Rango del bien adquirido (EUR)",
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
# ----------------------------------------------------------------------------------------------------------------------
    # Importe del capital en base al importe financiado en los productos que lo permiten y rango de mensualidades a simular
# ----------------------------------------------------------------------------------------------------------------------
    else:
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
        ventrega_a_cuenta = 0.00
# ----------------------------------------------------------------------------------------------------------------------
    # Mostrar el campo para indicar la carencia en los productos que lo permiten
# ----------------------------------------------------------------------------------------------------------------------
    if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 2, 3, 4, 5, 6, 7, 12, 13):
        carencias = col_val_3.slider("Rango de meses de carencia",
                                     min_value=0,
                                     max_value=4,
                                     step=1,
                                     value=[0, 0],
                                     help="Se debe indicar la duración de la carencia total inicial")
    else:
        carencias = [0,]

# ----------------------------------------------------------------------------------------------------------------------
# ********BLOQUE COMÚN******** DE INPUTS PARA LA SEGUNDA SECUENCIA FINANCIERA
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
# Mostrar los campos para gestionar la segunda secuencia financiera en los productos que lo permiten
# ----------------------------------------------------------------------------------------------------------------------
if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (6, 7, 12, 13):
    col_sim_15, col_sim_16, col_sim_17, col_sim_18 = st.columns([0.25,
                                                                 0.25,
                                                                 0.25,
                                                                 0.25],
                                                                 gap="small")
    if on_residual_porcentual == True:
        capital_2sec = round(col_sim_15.number_input("% a amortizar en la segunda secuencia",
                                                     min_value=5.00,
                                                     max_value=70.00,
                                                     step=5.00,
                                                     value=30.00, 
                                                     help="Se debe indicar el porcentaje del capital a amortizar en la segunda secuencia del OPTION+")
                             * (importe_bien if tools.LISTA_PRODUCTOS.index(etiqueta_producto) in (12, 13) else capital_prestado)
                             /100,
                             2)
    else:
        capital_2sec = col_sim_15.number_input("Importe a amortizar en la 2ª secuencia",
                                               min_value=50.00,
                                               max_value=30000.00,
                                               step=50.00, 
                                               help="Se debe indicar el importe del capital a amortizar en la segunda secuencia del OPTION+")
    plazo_2sec = col_sim_16.number_input("Duración de la segunda secuencia",
                                         min_value=1,
                                         max_value=60,
                                         step=1, 
                                         help="Se debe indicar la duración en meses del segundo tramo de amortización")   
    tasa_2sec = col_sim_17.number_input("Tipo de Interés Deudor de la 2º secuencia",
                                        min_value=0.0,
                                        max_value=20.00,
                                        step=0.05,
                                        value=0.00, 
                                        help="Se debe indicar el porcentaje del TIN a aplicar en la segunda secuencia")
else:
    tasa_2sec = 0.00
    capital_2sec = 0
    plazo_2sec = 0

# ----------------------------------------------------------------------------------------------------------------------
# ********BLOQUE SIMULACION UNITARIA********
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
    # Mostra el resultado de la simulación
# ----------------------------------------------------------------------------------------------------------------------
if on_masiva is False:
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
# Mostrar resultados de la simulación en Streamlit
# ----------------------------------------------------------------------------------------------------------------------
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Resumen",
                                                      "Secuencias financieras",
                                                      "Ejemplo representativo",
                                                      "Cuadro de amortización",
                                                      "Detalle TAE",
                                                      f"Características del producto {etiqueta_producto}"])
# ----------------------------------------------------------------------------------------------------------------------    
    # Mostrar el resumen económico de la simulación
# ----------------------------------------------------------------------------------------------------------------------    
        if resumen1 is None:
            with tab1:
                st.error(ejemplo_representativo,icon="❌")
        else:
            with tab1:
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
    # Mostrar el resumen de las secuencias financieras de la simulación
# ----------------------------------------------------------------------------------------------------------------------    
        with tab2:
            html_table = resumen3.to_html(classes='table table-right',
                                          index=True)
            st.markdown(html_table,
                        unsafe_allow_html=True)
# ----------------------------------------------------------------------------------------------------------------------    
    # Mostrar el ejemplo representativo de la simulación
# ----------------------------------------------------------------------------------------------------------------------    
        with tab3:
            st.code(ejemplo_representativo,
                    wrap_lines=True)
# ----------------------------------------------------------------------------------------------------------------------    
    # Mostrar el cuadro de amortización de la simulación
# ----------------------------------------------------------------------------------------------------------------------    
        with tab4:
            st.dataframe(cuadro_amortizacion,
                         hide_index=True)
# ----------------------------------------------------------------------------------------------------------------------    
    # Mostrar el detalle del TAE de la simulación
# ----------------------------------------------------------------------------------------------------------------------    
        with tab5:
            st.dataframe(input_tae,
                         hide_index=True)
# ----------------------------------------------------------------------------------------------------------------------    
    # Mostrar el detalle del producto de la simulación
# ----------------------------------------------------------------------------------------------------------------------    
        with tab6:
        # Filtrar el dataframe "tools.DICCIONARIO_PRODUCTOS" con el producto seleccionado en la simulación
            producto_info = tools.DICCIONARIO_PRODUCTOS[tools.DICCIONARIO_PRODUCTOS["Nombre del producto"] == etiqueta_producto]
        # Recordatorio de que la primera mensualidad de los productos Vorwerk financiado no puede superar la mensualidad contractual
            if tools.LISTA_PRODUCTOS.index(etiqueta_producto) == 3:
                st.warning('Para evitar que la primera mensualidad supere la cuota contractual, la carencia diferida tiene un tipo de interés del 0,00 % y, si el contrato es financiado entre fecha de bloqueo y fecha de vencimiento, se crea una carencia diferida forzada entre la fecha de financiación y la primera fecha de vencimiento teórica posible.', icon="⚠️")
                st.toast('Para evitar que la primera mensualidad supere la cuota contractual, la carencia diferida tiene un tipo de interés del 0,00 % y, si el contrato es financiado entre fecha de bloqueo y fecha de vencimiento, se crea una carencia diferida forzada entre la fecha de financiación y la primera fecha de vencimiento teórica posible.', icon="⚠️")
            st.dataframe(producto_info.T,
                         width='stretch')
# ----------------------------------------------------------------------------------------------------------------------
    # Exportar resultados de la simulación a Excel
# ----------------------------------------------------------------------------------------------------------------------    
        st.download_button(
            label="📥 Descargar en Excel",
            data=tools.generar_excel(resumen2,
                                    cuadro_amortizacion,
                                    tools.pd.DataFrame({'TAE': [resumen1.at['%','TAE']],# type: ignore
                                                        'Ejemplo representativo': [ejemplo_representativo]}),
                                    input_tae,
                                    resumen3),
            file_name="simulacion_amortizable.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# ----------------------------------------------------------------------------------------------------------------------
# ********BLOQUE SIMULACION MASIVA********
# ----------------------------------------------------------------------------------------------------------------------

else:
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
# Final de la aplicación
# ---------------------------------------------------------------------------------------------------------------------- 