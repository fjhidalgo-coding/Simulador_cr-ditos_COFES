#!
'''Programa para la simulación de los productos amortizables de COF_ES'''

import calendar
import pandas as pd
import bin.COFES___tools as tools

''' Definir funciones asociadas al cálculo de la TAE '''

def calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion,
                                                       w_fecha_ultimo_vencimiento_tratado,
                                                       w_dia_año):

    '''Conversión de las fecha de entrada al formato timestamp de Pandas'''
    fecha_financiacion = pd.to_datetime(fecha_financiacion)
    w_fecha_ultimo_vencimiento_tratado = pd.to_datetime(w_fecha_ultimo_vencimiento_tratado)
    
    '''Función para calcular la fracción del año entre la fecha de financiación y el vencimiento tratado'''
    w_dia_año_anterior = 366 if calendar.isleap(w_fecha_ultimo_vencimiento_tratado.year - 1) else 365
    w_dia_año_anterior = w_dia_año if pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).year ==  pd.to_datetime(fecha_financiacion).year else w_dia_año_anterior 
    delta_años = 0 if (w_fecha_ultimo_vencimiento_tratado.year - fecha_financiacion.year + 1) < 1 else w_fecha_ultimo_vencimiento_tratado.year - fecha_financiacion.year + 1
    w_aniversario_fecha_financiación = fecha_financiacion + pd.DateOffset(years=delta_años)
    
    if w_dia_año != w_dia_año_anterior and w_fecha_ultimo_vencimiento_tratado < w_aniversario_fecha_financiación:
        delta_años = delta_años - 2 if delta_años > 1 else 0
        w_aniversario_fecha_financiación += pd.DateOffset(years=-1)
        fraccion_año = (delta_años + ((w_dia_año_anterior - pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año_anterior)  
                       + ((pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).dayofyear) / w_dia_año))
    elif w_fecha_ultimo_vencimiento_tratado > w_aniversario_fecha_financiación:
        fraccion_año = (0 if delta_años < 1 else delta_años) + ((pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).dayofyear - pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año)
    else:
        delta_años = delta_años - 1 if delta_años > 1 else 0
        w_aniversario_fecha_financiación += pd.DateOffset(years=-1)
        fraccion_año = delta_años + ((pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).dayofyear - pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año)

    return tools.truncar_decimal(fraccion_año, 7)



def calcular_tae(cuota_tae,
                 tiempo,
                 tasa,
                 van_cuota_tae=[],
                 tolerancia=0.000001,
                 max_iteraciones=10000):

    '''Función para calcular la TAE de la operación'''
    tae = (1 + tasa / 1200) ** 12 - 1 # TAE inicial aproximada
    for _ in range(max_iteraciones):
        van_cuota_tae.clear()
        for i in range(len(cuota_tae)):
            van_cuota_tae.append(cuota_tae[i] / ((1 + tae) ** tiempo[i]))
            
        if abs(sum(van_cuota_tae)) < tolerancia:  # Comprueba si el VAN está dentro de la tolerancia
            return tae
        
        if sum(van_cuota_tae) < 0:
            tae -= 0.0001
        else:
            tae += 0.0001
        
    return tools.redondear_decimal(tae * 100)
