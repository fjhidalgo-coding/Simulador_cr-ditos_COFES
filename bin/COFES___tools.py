#!
'''Funciones comunes a todos los simuladores'''

from decimal import Decimal, ROUND_HALF_UP
import pandas as pd


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
