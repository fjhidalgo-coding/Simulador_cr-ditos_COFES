#!
'''Aplicación Streamlit para simular operaciones en curso de vida de COF_ES
Origen: 
https://https://disposici-n-rev-kgnmih4g6h2pfkmcxef5ob.streamlit.app/
https://github.com/mildredbr-design/disposici-n-rev/blob/main/simulador_revolving-2.py
'''

import bin.COFES___TAE as tools_tae
import bin.COFES___tools as tools
import bin.COFES__SIM_AMO as sim_amo
import bin.COFES__SIM_RCC as sim_rcc



''' Crear las funciones necesarias para la simulación en curso de vida'''

def rcc_cuadro_amortización(capital_pendiente,
                            df_amort_raw,
                            df_cambio_cuota_raw,
                            df_cambio_dia_raw,
                            df_dispos_raw,
                            dia_pago,
                            fecha_inicial,
                            fecha_joker,
                            mensualidad_actual,
                            on,
                            seguro_tasa,
                            usar_joker,
                            tasa_interes):
    if on:
        DIAS_BASE = 360
    else:
        DIAS_BASE = 365


    return (tools.pd.DataFrame(cuadro_amortización),
            tools.pd.DataFrame(rcc_resumen),
            tools.pd.DataFrame(datos_tae))
