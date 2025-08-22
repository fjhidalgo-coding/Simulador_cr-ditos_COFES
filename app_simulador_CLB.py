import streamlit as st
import datetime  as dt
import COFES_SIM_AMORTIZABLE_V1.COFES_SIM_AMO_Consola as sim

LISTA_PRODUCTOS = ["CREDITO FUSION","Crédito Proyecto","Compra a plazos","Compra a plazos Vorwerk","Compra financiada","COMPRA FINANCIADA VORWERK","AMORTIZABLE OPTION PH IP","AMORTIZABLE OPTION PH IC","CREDITO FINANCIACION AUTO OCASION","CREDITO FINANCIACION MOTO OCASION","CREDITO FINANCIACION AUTO NUEVO","CREDITO FINANCIACION MOTO NUEVO","CREDITO FINANCIACION AUTO OCASION","CREDITO FINANCIACION MOTO OCASION"]
LISTA_SEGURO = ["SIN SEGURO", "Seguro ADE","VIDA PLUS", "VIDA"]
    
st.title('Simulador de Cofidis España')


with st.sidebar:
    
    with st.form("Datos de entrada"):
        
        etiqueta_producto = st.selectbox('Elige el producto contratado:', LISTA_PRODUCTOS, index=1)
        tasa = st.number_input("Tipo de Interés Deudor", min_value=0.0, max_value=20.00, step=0.05, value=5.95, help="Se debe indicar el porcentaje del Tipo de Interés Nominal - TIN - a utlizar en la simulación")
        capital_prestado = st.number_input("Importe solicitado (EUR)", min_value=50.00, max_value=60000.00, step=50.00, value=1500.00, help="Se debe indicar el importe del capital solicitado en el préstamo")
        plazo = st.number_input("Nº de mensualidades", min_value=3, max_value=120, step=1, value=12, help="Se debe indicar la duración en meses del plazo de amortización")
        carencia = st.number_input("Meses de carencia", min_value=0, max_value=4, step=1, help="Se debe indicar la duración de la carencia total inicial")
        
        with st.expander("Gestionar la segunda secuencia financiera"):
            capital_2SEC = st.number_input("Importe a amortizar en la segunda secuencia (EUR)", min_value=50.00, max_value=30000.00, step=50.00, help="Se debe indicar el importe del capital a amortizar en la segunda secuencia del OPTION+")
            plazo_2SEC = st.number_input("Duración de la segunda secuencia", min_value=1, max_value=60, step=1, help="Se debe indicar la duración en meses del segundo tramo de amortización")   
                
        with st.expander("Gestionar el seguro"):
            seguro_titular_1 = st.selectbox("Seguro titular 1", LISTA_SEGURO, index=0)
            seguro_titular_2 = st.selectbox("Seguro titular 2", LISTA_SEGURO, index=0)
        
        with st.expander("Gestionar la comisión de apertura"):
            tasa_comision_apertura = st.number_input("Porcentaje comisión de apertura", min_value=0.00, max_value=5.00, step=0.05, help="Se debe indicar el porcentaje de la comisión de apertura a utlizar en la simulación")
            comision_apertura_capitalizada = st.checkbox("Comisión de apertura capitalizada")
            imp_max_com_apertura = st.number_input("Importe máximo de la comisión de apertura (EUR)", min_value=0.00, step=1.00, help="Se debe indicar el importe que no debería superar la comisión de apertura")
        
        with st.expander("Personalizar las fechas"):
            fecha_financiacion = st.date_input("Fecha de financiación", dt.date.today())
            dia_pago = st.number_input("Día de vencimiento", min_value=1, max_value=12, step=1, value=2, help="Se debe indicar el día de pago seleccionado por el cliente")
            
        st.form_submit_button("Pendiente",on_click=sim.calcular_comision_apertura(capital_prestado, tasa_comision_apertura, imp_max_com_apertura))
        
st.header('Préstamos amortizables')

with st.expander("Ver detalle del producto seleccionado"):
    st.write("Pendiente alimentar con detalle del producto seleccionado")

st.write('¡Streamlit está funcionando correctamente!')

        