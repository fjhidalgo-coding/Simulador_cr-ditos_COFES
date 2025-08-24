#!
# Aplicación Streamlit para simular operaciones de los productos amortizables de Cofidis España



# Importar los módulos a utilizar en la aplicación

import streamlit as st
import datetime  as dt
import COFES_SIM_AMORTIZABLE_V1.COFES_SIM_AMO_Consola as sim



#  Declarar las listas de productos tanto de crédito como de seguro

LISTA_PRODUCTOS = ["CREDITO FUSION","Crédito Proyecto","Compra a plazos","Compra a plazos Vorwerk","Compra financiada","COMPRA FINANCIADA VORWERK","AMORTIZABLE OPTION PH IP","AMORTIZABLE OPTION PH IC","CREDITO FINANCIACION AUTO OCASION","CREDITO FINANCIACION MOTO OCASION","CREDITO FINANCIACION AUTO NUEVO","CREDITO FINANCIACION MOTO NUEVO","CREDITO FINANCIACION AUTO OCASION","CREDITO FINANCIACION MOTO OCASION"]
LISTA_SEGURO = ["Seguro ADE", "SIN SEGURO", "VIDA PLUS", "VIDA"]



#  Iniciar la aplicación

st.set_page_config(
   page_title="Simulador de préstamos amortizables",
   page_icon="💱",
   layout="wide",
   initial_sidebar_state="expanded",
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
    
    # Detallar las características del producto amortizable de la simulación
    with st.expander(f"Detalle del producto: {etiqueta_producto}", expanded=False):
        if idx == 0:
            st.write("Familia de productos: Amortizable Rachat Directo")
            st.write("Interés: A cargo del cliente")
            st.write("Carencia: Hasta 2 meses en función del PROCOM")
            st.write("Comisión de apertura: En función del PROCOM y parametrización TACT. Presentada en el primer vencimiento")
            st.write("Secuencia financiera: Única")
            st.write("Producto asegurable (ADE)")
            st.write("Mínimo entre fecha de financiación y el primer vencimiento: Debe transcurrir un mínimo de 14 días")
        elif idx == 1:
            st.write("Familia de productos: Amortizable Directo")
            st.write("Interés: A cargo del cliente")
            st.write("Carencia: No aplicable")
            st.write("Comisión de apertura: No aplicable")
            st.write("Secuencia financiera: Única")
            st.write("Producto asegurable (ADE)")
            st.write("Mínimo entre fecha de financiación y el primer vencimiento: Debe transcurrir un mínimo de 14 días")
        elif idx < 6:
            st.write("Familia de productos: Amortizable Punto de Venta")
            if idx < 4:
                st.write("Interés: A cargo del cliente")
            else:
                st.write("Interés: A cargo del partner")
            st.write("Carencia:  Hasta 4 meses en función del baremo y el PROCOM")
            st.write("Comisión de apertura: En función del baremo y el PROCOM. Capitalizada o presentada en el primer vencimiento en función del PROCOM")
            st.write("Secuencia financiera: Única")
            st.write("Producto NO asegurable")
            st.write("Mínimo entre fecha de financiación y el primer vencimiento: Debe haber una fecha de bloqueo")
        elif idx < 8:
            st.write("Familia de productos: Amortizable OPTION+")
            if idx == 7:
                st.write("Interés: A cargo del cliente  aunque la segunda secuencia financiera puede tener interés 0% en función del PROCOM")
            else:
                st.write("Interés: A cargo del partner aunque la segunda secuencia financiera puede tener interés cliente en función del PROCOM")
            st.write("Carencia:  Hasta 4 meses en función del baremo y el PROCOM")
            st.write("Comisión de apertura: En función del baremo y el PROCOM. Capitalizada o presentada en el primer vencimiento en función del PROCOM")
            st.write("Secuencia financiera: Doble")
            st.write("Producto NO asegurable")
            st.write("Mínimo entre fecha de financiación y el primer vencimiento: Debe haber una fecha de bloqueo")
        else:
            st.write("Familia de productos: Amortizable AUTO")
            st.write("Interés: A cargo del cliente")
            st.write("Carencia: No aplicable")
            st.write("Comisión de apertura: En función del baremo y el PROCOM. Capitalizada")
            st.write("Secuencia financiera: Única")
            st.write("Producto asegurable (Vida y Vida+)")
            st.write("Mínimo entre fecha de financiación y el primer vencimiento: Debe haber una fecha de bloqueo")    
        if idx == 3 or idx == 5:
            st.markdown(":orange-badge[⚠️ Si el contrato es financiado entre fecha de bloqueo y fecha de vencimiento, se crea una carencia diferida con tipo de interés 0% para evitar que la primera mensualidad supere la cuota contractual]")
        
    
    comision = sim.calcular_comision_apertura(capital_prestado, tasa_comision_apertura, imp_max_com_apertura)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Capital", capital_prestado, "EUR")
    col2.metric("Intereses", "PENDIENTE", "EUR")
    col3.metric("Comisión de apertura", comision, "EUR")
    col4.metric("Prima de seguro", "PENDIENTE", "EUR")
    col5.metric("Coste total", "PENDIENTE", "EUR")
    col6.metric("Importe total a pagar", "PENDIENTE", "EUR")
    
    
    
# Mostrar pie
st.write('¡Streamlit está funcionando correctamente!')
