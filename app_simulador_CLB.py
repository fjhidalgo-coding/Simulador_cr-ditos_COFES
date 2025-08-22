import streamlit as st
import COFES_SIM_AMORTIZABLE_V1.COFES_SIM_AMO_Consola as sim

st.title('Simulador de Cofidis España')
st.header('Préstamos amortizables')
st.write('¡Streamlit está funcionando correctamente!')

with st.form("Datos de entrada"):
    
    with st.expander("Ver detalle del producto seleccionado"):
    st.write('''
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    ''')
    
    
    tasa = st.slider("Tipo de Interés Deudor", min_value=0.0, max_value=20.00, step=0.05, help="Se debe indicar el porcentaje del Tipo de Interés Nominal - TIN - a utlizar en la simulación")
    
    tasa_comision_apertura = st.slider("Porcentaje comisión de apertura", min_value=0.0, max_value=5.00, step=0.05, help="Se debe indicar el porcentaje de la comisión de apertura a utlizar en la simulación")
    comision_apertura_capitalizada = st.checkbox("Comisión de apertura capitalizada")
    imp_max_com_apertura = st.number_input("Importe máximo de la comisión de apertura (EUR)", min_value=0.00, step=1.00, help="Se debe indicar el importe que no debería superar la comisión de apertura")

    seguro_titular_1 = st.checkbox("Titular 1 asegurado")
    seguro_titular_2 = st.checkbox("Titular 2 asegurado")
    
    
    st.form_submit_button("Pendiente")