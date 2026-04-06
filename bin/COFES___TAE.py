#!
'''Programa para la simulación de los productos amortizables de COF_ES'''

import bin.COFES___tools as tools

''' Definir funciones asociadas al cálculo de la TAE '''

def calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion,
                                                       w_fecha_ultimo_vencimiento_tratado,
                                                       w_dia_año):

    '''Conversión de las fecha de entrada al formato timestamp de Pandas'''
    fecha_financiacion = tools.pd.to_datetime(fecha_financiacion)
    w_fecha_ultimo_vencimiento_tratado = tools.pd.to_datetime(w_fecha_ultimo_vencimiento_tratado)
    
    '''Función para calcular la fracción del año entre la fecha de financiación y el vencimiento tratado'''
    if tools.pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).year ==  tools.pd.to_datetime(fecha_financiacion).year:
        w_dia_año_anterior = w_dia_año
    else:
        w_dia_año_anterior = tools.dias_año(w_fecha_ultimo_vencimiento_tratado - tools.pd.DateOffset(days=1))
    
       
    delta_años = 0 if (w_fecha_ultimo_vencimiento_tratado.year - fecha_financiacion.year + 1) < 1 else w_fecha_ultimo_vencimiento_tratado.year - fecha_financiacion.year + 1
    w_aniversario_fecha_financiación = fecha_financiacion + tools.pd.DateOffset(years=delta_años)
    
    if w_dia_año != w_dia_año_anterior and w_fecha_ultimo_vencimiento_tratado < w_aniversario_fecha_financiación:
        delta_años = delta_años - 2 if delta_años > 1 else 0
        w_aniversario_fecha_financiación += tools.pd.DateOffset(years=-1)
        fraccion_año = (delta_años + ((w_dia_año_anterior - tools.pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año_anterior)  
                       + ((tools.pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).dayofyear) / w_dia_año))
    elif w_fecha_ultimo_vencimiento_tratado > w_aniversario_fecha_financiación:
        fraccion_año = (0 if delta_años < 1 else delta_años) + ((tools.pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).dayofyear - tools.pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año)
    else:
        delta_años = delta_años - 1 if delta_años > 1 else 0
        w_aniversario_fecha_financiación += tools.pd.DateOffset(years=-1)
        fraccion_año = delta_años + ((tools.pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).dayofyear - tools.pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año)

    return tools.truncar_decimal(fraccion_año, 7)



def calcular_tae(cuota_tae,
                 tiempo,
                 tasa,
                 van_cuota_tae=None,
                 tolerancia=0.000001,
                 max_iteraciones=1000):

    '''Función para calcular la TAE de la operación'''
    if van_cuota_tae is None:
        van_cuota_tae = []

    tasa_float = float(tasa)
    tae = (1 + tasa_float / 1200) ** 12 - 1 # TAE inicial aproximada
    for _ in range(max_iteraciones):
        van_cuota_tae.clear()
        for i in range(len(cuota_tae)):
            cuota = float(cuota_tae[i]) if cuota_tae[i] is not None else 0.0
            periodo = float(tiempo[i]) if tiempo[i] is not None else 0.0
            van_cuota_tae.append(cuota / ((1 + tae) ** periodo))
            
        if abs(sum(van_cuota_tae)) < tolerancia:  # Comprueba si el VAN está dentro de la tolerancia
            return tools.redondear_decimal(tools.Decimal(str(tae * 100)))
        
        if sum(van_cuota_tae) < 0:
            tae -= 0.0001
        else:
            tae += 0.0001
        
    return tools.redondear_decimal(tools.Decimal(str(tae * 100)))
