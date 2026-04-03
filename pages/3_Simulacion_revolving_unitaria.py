#!
# Aplicación Streamlit para simular operaciones de los productos revolving de COF_ES

from datetime import datetime
import streamlit as st
import pandas as pd
import bin.COFES__SIM_RCC as sim
import bin.COFES___tools as tools



# Definir variables
valor=None
vitesse_valores=[2.7,2.75,3,3.25,3.43,4.37,5.17,6.57,9.37]
opciones_seguro={
    "No":0,
    "Un titular Light":0.0035,
    "Un titular Full/Senior":0.0061,
    "Dos titulares Full/Full":0.0104,
    "Dos titulares Senior/Senior":0.0104,
    "Dos titulares Light/Light":0.0059,
    "Dos titulares Full/Light":0.0082
}



# Título y aviso de funcionalidad en construcción
st.title('Simulador Revolving con Seguro Opcional')
st.info('Funcionalidad en pruebas', icon="⚠️")



# Definir la configuración de la página y estilos personalizados
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



# Primera sección de inputs: capital, TIN, fecha de inicio y tipo de cálculo
col_varios_1, col_varios_2, col_varios_3, col_varios_4 = st.columns([0.25, 0.25, 0.25, 0.25], gap="small")

capital = col_varios_1.number_input("Importe de financiación (€)",min_value=0.0, max_value=1000000.0, step=250.00, value=3000.0)
tin = col_varios_2.number_input("TIN anual (%)",min_value=0.0, max_value=30.0, step=0.10, value=21.79)
fecha_inicio = col_varios_3.date_input("Fecha de financiación", datetime.today())
dia_recibo = col_varios_4.selectbox("Seleccione el día del recibo (1-12)",options=list(range(1, 13)), index=1)



# Segunda sección de inputs: tipo de cálculo, valor asociado al tipo de cálculo y seguro mensual
col_varios_5, col_varios_6, col_varios_7 = st.columns([0.25, 0.25, 0.25], gap="small")

tipo_calculo = col_varios_5.selectbox("Tipo de cálculo",["Seleccionar","Vitesse","Cuota","Duración"])
if tipo_calculo=="Vitesse":
    valor=col_varios_6.selectbox("Vitesse (%)",vitesse_valores)
elif tipo_calculo=="Cuota":
    opciones_cuota=[round(capital*v/100,2) for v in vitesse_valores]
    valor=col_varios_6.selectbox("Cuota mensual (€)",opciones_cuota)
elif tipo_calculo=="Duración":
    opciones_duracion=[]
    mapa_vitesse={}
    for v in vitesse_valores:
        cuota_test=round(capital*v/100,2)
        tabla_test=sim.simulador(capital,tin,"Cuota",cuota_test,fecha_inicio,0)
        meses=len(tabla_test)
        etiqueta=f"{meses} meses"
        opciones_duracion.append(etiqueta)
        mapa_vitesse[etiqueta]=v
    seleccion=col_varios_5.selectbox("Duración del préstamo",opciones_duracion)
    valor=mapa_vitesse[seleccion]
    tipo_calculo="Vitesse"
seguro_str=col_varios_7.selectbox("Seguro mensual",list(opciones_seguro.keys()))
seguro_tasa=opciones_seguro[seguro_str]

if valor is not None and tipo_calculo!="Seleccionar":
    
    tabla=sim.simulador(capital, tin, tipo_calculo, valor, fecha_inicio, seguro_tasa)

    # Quitar columna seguro si no hay seguro
    if seguro_tasa==0 and "Seguro (€)" in tabla.columns:
        tabla=tabla.drop(columns=["Seguro (€)"])

    total_intereses=round(tabla["Intereses total (€)"].sum(),2)
    total_capital_intereses=round(tabla["Cuota (€)"].sum(),2)

    if seguro_tasa>0:
        total_seguro=round(tabla["Seguro (€)"].sum(),2)

    cuotas_tae=[-capital]+list(tabla["Cuota (€)"])
    fechas_tae=[fecha_inicio]+list(tabla["Fecha recibo"])

    tae= sim.calcular_tae(cuotas_tae,fechas_tae)
    
    if seguro_tasa>0:
        resumen_dict={
        "Concepto":[
        "Duración (meses)",
        "Intereses (€)",
        "Seguro (€) total",
        "Coste total (capital+intereses)",
        "Coste total (capital+intereses+seguro)",
        "TAE (%)"
        ],
        "Valor":[
        len(tabla),
        total_intereses,
        total_seguro,
        total_capital_intereses,
        round(total_capital_intereses+total_seguro,2),
        tae
        ]
        }
    else:
        resumen_dict={
        "Concepto":[
        "Duración (meses)",
        "Intereses (€)",
        "Importe total a pagar (capital+intereses)",
        "TAE (%)"
        ],
        "Valor":[
        len(tabla),
        tools.formatear_decimales(total_intereses),
        tools.formatear_decimales(total_capital_intereses),
        tools.formatear_decimales(tae)
        ]
        }
    df_resumen=pd.DataFrame(resumen_dict).transpose()

    # ---------------------------------------------------------
    # EXPORTAR A EXCEL
    # ---------------------------------------------------------
    st.download_button(
        label="📥 Descargar en Excel",
        data=tools.generar_excel(df_resumen, tabla),
        file_name="simulacion_revolving.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    tab1, tab2, = st.tabs(["Resumen", "Cuadro de amortización"])
    
    with tab1:
        st.dataframe(df_resumen)

    with tab2:
        st.dataframe(tabla,hide_index=True)
    