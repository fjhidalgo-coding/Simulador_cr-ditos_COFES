#!
# Aplicación Streamlit para simular operaciones de los productos amortizables de Cofidis España



# Importar los módulos a utilizar en la aplicación

import streamlit as st
import datetime  as dt
import pandas as pd
import COFES_SIM_AMO_Consola as sim




#  Declarar las listas de productos tanto de crédito como de seguro

LISTA_SEGURO = sim.LISTA_SEGURO
LISTA_PRODUCTOS = sim.LISTA_PRODUCTOS
PRODUCTOS_DICCIONARIO = sim.PRODUCTOS_DICCIONARIO



# Convertir el diccionario de productos en un dataframe para facilitar su manejo

productos_descripcion = pd.DataFrame(PRODUCTOS_DICCIONARIO)


#  Iniciar la aplicación

st.set_page_config(
   page_title="Simulador de préstamos amortizables",
   page_icon="💱",
   layout="wide",
   initial_sidebar_state="expanded",
)
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title('Simulador de préstamos amortizables')



# Crear barra lateral donde se introducen los datos de la simulación
with st.sidebar:
    
    # Crear selector del producto amortizable a simular
    with st.expander("Seleccionar producto", expanded=True):
        with st.form("Producto"):
            etiqueta_producto = st.selectbox('Elige el producto contratado:', LISTA_PRODUCTOS, index=1)
            seleccion = st.form_submit_button("Seleccionar producto")
            
            # Guardar el producto seleccionado en session_state
            if seleccion:
                st.session_state.etiqueta_producto = etiqueta_producto
                st.session_state.simular = False  # Reinicia simulación al cambiar producto

    # Seleccionar datos de la simulación
    if "etiqueta_producto" in st.session_state:        
        with st.form("Datos de entrada"):
                
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

            # Mmostrar botón para simular la operación
            submit = st.form_submit_button("Simular operación")

            # Guardar los datos en session_state
            if submit:
                st.session_state.simular = True
            
            with st.expander("Personalizar las fechas"):
                fecha_financiacion = st.date_input("Fecha de financiación", dt.date.today())
                dia_pago = st.number_input("Día de vencimiento", min_value=1, max_value=12, step=1, value=2, help="Se debe indicar el día de pago seleccionado por el cliente")

            tasa = st.number_input("Tipo de Interés Deudor", min_value=0.0, max_value=20.00, step=0.05, value=5.95, help="Se debe indicar el porcentaje del Tipo de Interés Nominal - TIN - a utlizar en la simulación")
            capital_prestado = st.number_input("Importe solicitado (EUR)", min_value=50.00, max_value=60000.00, step=50.00, value=1500.00, help="Se debe indicar el importe del capital solicitado en el préstamo")
            plazo = st.number_input("Nº de mensualidades", min_value=3, max_value=120, step=1, value=12, help="Se debe indicar la duración en meses del plazo de amortización")
            
            idx = LISTA_PRODUCTOS.index(st.session_state.etiqueta_producto)
            
            if idx != 1 and idx < 8:
                carencia = st.number_input("Meses de carencia", min_value=0, max_value=4, step=1, help="Se debe indicar la duración de la carencia total inicial")
            
            if 5 < idx < 8:
                with st.expander("Gestionar la segunda secuencia financiera"):
                    tasa_2SEC = st.number_input("Tipo de Interés Deudor", min_value=0.0, max_value=20.00, step=0.05, value=0.00, help="Se debe indicar el porcentaje del TIN a aplicar en la segunda secuencia")
                    capital_2SEC = st.number_input("Importe a amortizar en la segunda secuencia (EUR)", min_value=50.00, max_value=30000.00, step=50.00, help="Se debe indicar el importe del capital a amortizar en la segunda secuencia del OPTION+")
                    plazo_2SEC = st.number_input("Duración de la segunda secuencia", min_value=1, max_value=60, step=1, help="Se debe indicar la duración en meses del segundo tramo de amortización")   
                    
            if idx < 2 or idx > 7:
                with st.expander("Gestionar el seguro"):
                    if LISTA_PRODUCTOS.index(etiqueta_producto) < 2:
                        seguro_titular_1 = st.selectbox("Seguro titular 1", LISTA_SEGURO[:2], index=1)
                        seguro_titular_2 = st.selectbox("Seguro titular 2", LISTA_SEGURO[:2], index=1)
                    else:
                        seguro_titular_1 = st.selectbox("Seguro titular 1", LISTA_SEGURO[1:], index=0)
                        seguro_titular_2 = st.selectbox("Seguro titular 2", LISTA_SEGURO[1:], index=0)
            
            if  idx != 1:
                with st.expander("Gestionar la comisión de apertura"):
                    tasa_comision_apertura = st.number_input("Porcentaje comisión de apertura", min_value=0.00, max_value=5.00, step=0.05, help="Se debe indicar el porcentaje de la comisión de apertura a utlizar en la simulación")
                    
                    if idx > 7:
                        comision_apertura_capitalizada = st.checkbox("Comisión de apertura capitalizada",value=True, disabled=True)
                    elif idx > 1:
                        comision_apertura_capitalizada = st.checkbox("Comisión de apertura capitalizada")
                    
                    imp_max_com_apertura = st.number_input("Importe máximo de la comisión de apertura (EUR)", min_value=0.00, step=1.00, help="Se debe indicar el importe que no debería superar la comisión de apertura")
            
        

# Mostra el resultado de la simulación
if st.session_state.get("simular", False):
    
    # Realizar los cálculos de la simulación
    tae, comision_apertura, importe_total_a_pagar, coste_total, intereses, coste_seguro, importe_crédito, descuento, tasa, cuota_1SEC, cuota_2SEC, fecha_fin_carencia_gratuita_forzada, fecha_fin_carencia_diferida, fecha_fin_carencia, fecha_primer_vencimiento, cuadro_amortizacion, input_TAE = sim.simular_prestamo_CLB(etiqueta_producto, fecha_financiacion, dia_pago, tasa, capital_prestado, plazo, carencia, tasa_2SEC, capital_2SEC, plazo_2SEC, seguro_titular_1, seguro_titular_2, tasa_comision_apertura, comision_apertura_capitalizada, imp_max_com_apertura)
    
    # Mostrar resumen de la simulación
    with st.expander("", expanded=True):
        resumen1 = pd.DataFrame(
        {
            "TAE": [f"{tae:.2f}"],
        },
        index=["%"],
    )
        resumen2 = pd.DataFrame(
        {
            "Importe total a pagar": [f"{importe_total_a_pagar:.2f}"],
            "Coste total": [f"{coste_total:.2f}"],
            "Intereses": [f"{intereses:.2f}"],
            "Prima de seguro": [f"{coste_seguro:.2f}"],
            "Comisión de apertura": [f"{comision_apertura:.2f}"],
            "Capital": [f"{capital_prestado:.2f}"],
            "Importe del crédito": [f"{importe_crédito:.2f}"],
            "Descuento Partner": [f"{descuento:.2f}"],
        },
        index=["EUR"],
    )
    
        col1, col2 = st.columns([0.08, 0.92], gap="small")
        col1.table(resumen1)
        col2.table(resumen2)

    
    
    # Detallar las características del producto amortizable de la simulación
    with st.expander(f"Características del producto {etiqueta_producto}", expanded=False):
        # Filtrar el dataframe "productos_descripcion" con el producto seleccionado en la simulación
        producto_info = productos_descripcion[productos_descripcion["Nombre del producto"] == etiqueta_producto]
        
        col3, col4 = st.columns([0.33, 0.67], gap="medium")
        
        if not producto_info.empty:
            for columna in producto_info.columns:
                valor = producto_info.iloc[0][columna]
                col3.markdown(f'<div style="text-align: right;">{columna}</div>', unsafe_allow_html=True)
                col4.markdown(f'<div style="text-align: left;">{valor}</div>', unsafe_allow_html=True)
        else:
            st.write("Producto no encontrado.")
            
        # Recordatorio de que la primera mensualidad de los productos Vorwerk financiado no puede superar la mensualidad contractual
        if idx == 3 or idx == 5:
            st.markdown(":orange-badge[⚠️ Si el contrato es financiado entre fecha de bloqueo y fecha de vencimiento, se crea una carencia diferida con tipo de interés 0% para evitar que la primera mensualidad supere la cuota contractual]")
    
    
    tab1, tab2, tab3, tab4 = st.tabs(["Secuencias financieras", "Ejemplo representativo", "Cuadro de amortización", "Detalle TAE"])
    with tab1:
        
        mostrar_fecha = lambda fecha: fecha.strftime('%d/%m/%Y') if fecha is not None and pd.notnull(fecha) else "No disponible"
        
        cuenta_vencimientos = cuadro_amortizacion['Tipo vcto'].value_counts()
        primeros = cuadro_amortizacion.groupby('Tipo vcto').head(1)
        ultimos = cuadro_amortizacion.groupby('Tipo vcto').tail(1)
        modales = cuadro_amortizacion.groupby('Tipo vcto')['Mens. vcto'].agg(lambda x: x.mode().iat[0] if not x.mode().empty else None)


        resumen3 = pd.DataFrame(
        {
            "F_1er_VCTO":  [mostrar_fecha(fecha) for fecha in primeros['F_Vcto'].values],
            "F_INI": [f"{coste_total:.2f}"],
            "F_FIN":  [mostrar_fecha(fecha) for fecha in ultimos['F_Vcto'].values],
            "Nº Vencimientos": cuenta_vencimientos.loc[ultimos['Tipo vcto']].values,
            "IMP_1era_Cuota": primeros['Mens. vcto'].values,
            "IMP_Cuota": modales.loc[ultimos['Tipo vcto']].values, # Usar la moda no funciona para duraciones de 3 meses
            "IMP_ULT_Cuota": ultimos['Mens. vcto'].values,
            "Tipo": "PDTE añadir TIN",
        },
        index=ultimos['Tipo vcto'].values,
    )
    
        st.table(resumen3)

        
        
        st.write(f"TMP - Mensualidad primera secuencia: {cuota_1SEC}")
        st.write(f"TMP - Mensualidad segunda secuencia: {cuota_2SEC}")
    
        
    with tab2:
        st.code("Pendiente desarrollo")

    with tab3:
        st.dataframe(cuadro_amortizacion,hide_index=True)
    
    with tab4:
        st.dataframe(input_TAE,hide_index=True)
    



# Final de la aplicación