#!
'''Funciones comunes a todos los simuladores'''

import calendar as cl
from decimal import Decimal, ROUND_HALF_UP
from io import BytesIO
import pandas as pd


def dias_año(fecha):

    '''Función para recuperar el número de días del año de una fecha dada'''
    return 366 if cl.isleap(fecha.year) else 365



def truncar_decimal(valor,
                    decimales):

    '''Función para truncar un número decimal a un número específico de decimales sin redondear'''
    factor = 10 ** decimales
   
    return int(valor * factor) / factor



def redondear_decimal(valor):

    '''Función para redondear un número decimal a 2 decimales'''
    return float(Decimal(valor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))



def mostrar_fecha(fecha):

    ''' Función para devolver la fecha formateada a dd/mm/yyyy '''
    if fecha is not None and pd.notnull(fecha):
        fecha = pd.to_datetime(fecha).strftime('%d/%m/%Y') 
    else:
        return None
    
    return fecha



def formatear_decimales(value: float) -> str:
    """Formatea un valor numérico como moneda con coma decimal."""
    return f"{value:.2f}".replace('.', ',')



def generar_excel(df_resumen=None, df_tamo=None, df_ejemplo=None, df_tae=None, df_secuencias=None,resultado_simulacion_masiva=None):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        if df_resumen is not None:
            df_resumen.to_excel(writer, sheet_name="Resumen", index=False)
        if df_secuencias is not None:
            df_secuencias.to_excel(writer, sheet_name="Secuencias", index=False)
        if df_ejemplo is not None:
            df_ejemplo.to_excel(writer, sheet_name="Ejemplo", index=False)
        if df_tamo is not None:
            df_tamo.to_excel(writer, sheet_name="Tamo", index=False)
        if df_tae is not None:
            df_tae.to_excel(writer, sheet_name="TAE", index=False)
        if resultado_simulacion_masiva is not None:
            resultado_simulacion_masiva.to_excel(writer, sheet_name="Simulación Masiva", index=False)

    output.seek(0)
    return output
