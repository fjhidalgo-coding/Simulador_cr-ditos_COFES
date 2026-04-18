#!

import calendar as cl
import datetime  as dt
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP, ROUND_DOWN, getcontext
from io import BytesIO
import pandas as pd
import numpy as np



''' Declarar las constantes globales para todos los simuladores '''
DICCIONARIO_PRODUCTOS = pd.read_csv('./data/COFES_00_PRODUCTOS_DICCIONARIO.csv',
                                    sep=',',
                                    dayfirst=True).sort_values(by="Código de producto POPS")
FECHAS_BLOQUEO = pd.read_csv('./data/COFES_01_Date_Blocage.csv',
                             sep=';',
                             parse_dates=['Fecha_BLOQUEO'],
                             dayfirst=True).sort_values(by='Fecha_BLOQUEO')
getcontext().prec = 50
LISTA_PRODUCTOS = list(DICCIONARIO_PRODUCTOS['Nombre del producto'].values)
LISTA_SEGURO = ["Seguro ADE",
                "Sin seguro",
                "Vida Plus",
                "Vida"]
OPCIONES_SEGURO_AMO = {
    "1 asegurado ADE":0.0444,
    "2 asegurados ADE":0.0768,
    "Sin seguro":0.0000,
    "1 asegurado Vida":1.0000,
    "1 asegurado Vida +":2.0000,
    "1 asegurado Vida + y 1 asegurado Vida":3.0000,
    "2 asegurado Vida":4.0000,
    "2 asegurado Vida +":5.0000
}
OPCIONES_SEGURO_NFOIS = {
    "No":0,
    "ADE NFOIS":0.006
}
OPCIONES_SEGURO_RCC = {
    "No":0,
    "Un titular Light":0.0035,
    "Un titular Full/Senior":0.0061,
    "Dos titulares Full/Full":0.0104,
    "Dos titulares Senior/Senior":0.0104,
    "Dos titulares Light/Light":0.0059,
    "Dos titulares Full/Light":0.0082
}
RCC_OPCIONES_VITESSE = [2.7,2.75,3,3.25,3.43,4.37,5.17,6.57,9.37,3.7,4,4.4,4.8,5.2,5.6,6,6.4,6.8]



''' Declarar las funciones comunes para todos los simuladores '''

def bascular_a_decimal(valor, tipo_redondeo):

    '''Forzar formato Decimal para los cálculos y evitar problemas de precisión con los floats'''
    if not isinstance(valor, Decimal):
        valor = Decimal(str(valor))
   
    return valor.quantize(Decimal('0.01'), rounding=tipo_redondeo)



def calcular_comision_apertura(capital_prestado,
                               tasa_comision_apertura,
                               imp_max_com_apertura,
                               comision_apertura_capitalizada):

    '''Calcular la comisión de apertura en base al capital prestado y el porcentaje definido'''
    comision_apertura = capital_prestado * tasa_comision_apertura / 100
    if comision_apertura > imp_max_com_apertura and imp_max_com_apertura > 0:
        '''Comprobar que la comisión calculada no supera el límite marcado; si fuese el caso, actualizamos el valor de la comisión con el límite'''
        comision_apertura = imp_max_com_apertura
    if comision_apertura_capitalizada:
        capitalizacion_comision_apertura = comision_apertura
    else:
        capitalizacion_comision_apertura = 0.00
   
    return (redondear_decimal(comision_apertura),
            redondear_decimal(capitalizacion_comision_apertura))



def calcular_descuento_partner(importe_crédito,
                               tasa,
                               carencia,
                               plazo,
                               plazo_2sec):

    '''Función para calcular el descuento partner de los productos amortizables de COF_ES'''
    if tasa != 0.00:
        # En este cálculo, asumimos que la capitalización de la comisión de apertura debe ser abonada por el partner
        # Existe un descuadre en las operaciones con carencia --> El excel de EI no contenía la manera de calcular con carencia
        duracion_total = plazo + plazo_2sec
        capital_mensual = truncar_decimal(importe_crédito / duracion_total, 7)
        tasa_mensual = 1 + truncar_decimal(tasa / 1200, 7)
        tasa_descuento = 1 - truncar_decimal(tasa_mensual ** -duracion_total, 7)
        ajuste_carencia = truncar_decimal(tasa_mensual ** -carencia, 7)
        capital_mensual_ajustado = truncar_decimal(capital_mensual * tasa_descuento, 7) * 1200
        descuento = truncar_decimal(capital_mensual_ajustado / tasa * ajuste_carencia, 7)
        descuento = truncar_decimal(importe_crédito - descuento, 2)
    else:
        descuento = 0.00

    return redondear_decimal(descuento)



def calcular_fechas(etiqueta_producto,
                    fecha_financiacion,
                    dia_pago,
                    carencia):

    '''Función para calcular las principales fechas de préstamo'''
    fecha_financiacion = pd.to_datetime(fecha_financiacion)
    fecha_fin_carencia = pd.to_datetime("")
    fecha_fin_carencia_diferida = pd.to_datetime("")
    fecha_fin_carencia_gratuita_forzada = pd.to_datetime("")
    
    '''Calcular la fecha del primer vencimiento en base a la fecha de bloqueo posterior a la fecha de financiación'''
    proximas_db = FECHAS_BLOQUEO[FECHAS_BLOQUEO['Fecha_BLOQUEO'] >= fecha_financiacion]
    fecha_primer_vencimiento = proximas_db['Fecha_BLOQUEO'].iloc[0].replace(day=dia_pago) + pd.DateOffset(months=1)
    
    '''Calculamos el periodo de "carencia diferida" gratuita de los productos Vorwerk que evita tener una primera mensualidad superior al resto'''
    if LISTA_PRODUCTOS.index(etiqueta_producto) in (3, 5) and fecha_financiacion < (fecha_primer_vencimiento + pd.DateOffset(months=-1)):
        fecha_fin_carencia_gratuita_forzada = fecha_primer_vencimiento + pd.DateOffset(months=-1)
    
    '''Recalculamos la fecha del primer vencimiento de los amortizables de directos para evitar que haya menos de 14 días entre la fecha de financiación y el primer recibo'''
    if LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 1) and carencia == 0 and (fecha_primer_vencimiento - fecha_financiacion).days  < 14:
        fecha_primer_vencimiento += pd.DateOffset(months=1)
    
    if carencia != 0:
        if fecha_financiacion.day != dia_pago:
            '''Calculamos la fecha fin carencia diferida, de la carencia normal y la fecha del primer vencimiento'''
            if fecha_fin_carencia_gratuita_forzada is not None and pd.notnull(fecha_fin_carencia_gratuita_forzada):
                '''Si existe carencia gratuita forzada, la fecha fin de carencia se calcula a partir de esta'''
                fecha_fin_carencia = fecha_fin_carencia_gratuita_forzada + pd.DateOffset(months=carencia)
            else:
                if fecha_financiacion < (fecha_primer_vencimiento + pd.DateOffset(months=-1)):
                    '''Calculamos la fecha de fin de la carencia diferida cuando la fecha de financiación entre fecha de bloqueo y fecha de vencimiento'''
                    fecha_fin_carencia_diferida = fecha_primer_vencimiento + pd.DateOffset(months=-1)
                else:
                    fecha_fin_carencia_diferida = fecha_primer_vencimiento
                fecha_fin_carencia = fecha_fin_carencia_diferida + pd.DateOffset(months=carencia)
        else:
            fecha_fin_carencia = fecha_primer_vencimiento + pd.DateOffset(months=carencia-1)
        fecha_primer_vencimiento = fecha_fin_carencia + pd.DateOffset(months=1)

    return (fecha_fin_carencia_gratuita_forzada, 
            fecha_fin_carencia_diferida,
            fecha_fin_carencia,
            fecha_primer_vencimiento)



def calcular_mensualidad_estandar(importe_crédito,
                                  tasa_global, 
                                  plazo, 
                                  carencia, 
                                  tasa_2sec, 
                                  capital_2sec, 
                                  plazo_2sec, 
                                  tasa, 
                                  tasa_ade, 
                                  fecha_financiacion, 
                                  fecha_fin_carencia_gratuita_forzada, 
                                  fecha_fin_carencia_diferida, 
                                  fecha_fin_carencia,
                                  w_DIAS_BASE):
    '''Función para calcular la mensualidad estándar de los productos amortizables de COF_ES'''
    
    '''Incremantar el capital de la operación con el interés y seguro capitalizado al finalizar carencia'''
    
    if carencia == 1:
        w_interes_periodo_carencia = calcular_periodo(importe_crédito, fecha_fin_carencia - pd.DateOffset(months=1), fecha_fin_carencia, tasa_global) * carencia
        importe_crédito +=  w_interes_periodo_carencia

    if carencia > 1:
        w_interes_periodo_carencia = calcular_periodo(importe_crédito, fecha_fin_carencia - pd.DateOffset(months=1), fecha_fin_carencia, tasa) * carencia
        w_fecha_ultimo_vencimiento_tratado = (fecha_fin_carencia_gratuita_forzada if fecha_fin_carencia_gratuita_forzada is not None and pd.notnull(fecha_fin_carencia_gratuita_forzada)
                                                                                  else fecha_fin_carencia_diferida
                                                                                  if fecha_fin_carencia_diferida is not None and pd.notnull(fecha_fin_carencia_diferida)
                                                                                  else fecha_financiacion)
        importe_crédito += ( w_interes_periodo_carencia + 
                            calcular_periodo_roto(importe_crédito, w_fecha_ultimo_vencimiento_tratado, fecha_fin_carencia, tasa_ade, w_DIAS_BASE))
        
    '''Calcular la mensualidad contractual del préstamo rendondeando al céntimo superior para asegurar la ventilación de todo el capital'''
    if tasa_global == 0.00:
        cuota_1sec = (importe_crédito - capital_2sec) / plazo
    else:
        cuota_1sec = ((capital_2sec * tasa_global / 1200)
                      + ((importe_crédito - capital_2sec) * tasa_global / 1200 * ((1 + (tasa_global / 1200)) ** plazo) / (((1 + (tasa_global / 1200)) ** plazo) - 1)))
    

    '''Calcular la mensualidad de la segunda secuencia en caso de que exista'''
    if capital_2sec == 0.00:
        cuota_2sec = 0.00
    else:
        if tasa_2sec == 0.00:
            cuota_2sec = capital_2sec / plazo_2sec
        else:
            cuota_2sec = capital_2sec * tasa_2sec / 1200 * ((1 + (tasa_2sec / 1200)) ** plazo_2sec) / (((1 + (tasa_2sec / 1200)) ** plazo_2sec) - 1)
    
    if w_DIAS_BASE == 365:
        return (redondear_decimal(cuota_1sec),
                redondear_decimal(cuota_2sec))
    else:
        return (redondear_decimal_superior(cuota_1sec),
                redondear_decimal_superior(cuota_2sec))



def calcular_periodo(base_calculo,
                     fecha_inicio,
                     fecha_fin,
                     tasa_a_aplicar):

    '''Forzar formato Decimal para los cálculos y evitar problemas de precisión con los floats'''
    base_calculo = redondear_decimal(base_calculo)
    tasa_a_aplicar = redondear_decimal(tasa_a_aplicar)

    '''Calcular el interés o el seguro cuando el periodo está completo'''
    importe_calculo_periodo = redondear_decimal(base_calculo * tasa_a_aplicar / 1200 * ((fecha_fin.year - fecha_inicio.year) * 12 + (fecha_fin.month - fecha_inicio.month)))
   
    return redondear_decimal(importe_calculo_periodo)



def calcular_periodo_roto(base_calculo,
                          fecha_inicio,
                          fecha_fin,
                          tasa_a_aplicar,
                          w_DIAS_BASE):

    '''Forzar formato Decimal para los cálculos y evitar problemas de precisión con los floats'''
    base_calculo = redondear_decimal(base_calculo)
    tasa_a_aplicar = redondear_decimal(tasa_a_aplicar)

    ''' AMO: Calcular el interés o el seguro cuando el día de inicio de periodo no coincide con el día de fin de periodo
        RCC: Calcular el interés del periodo'''
    if w_DIAS_BASE == 365:
        if dias_año(fecha_inicio) != dias_año(fecha_fin) and fecha_fin.month == 1:
            importe_calculo_periodo_roto = (truncar_decimal(base_calculo * tasa_a_aplicar / 100 * (dt.datetime(fecha_inicio.year, 12, 31) - fecha_inicio).days / dias_año(fecha_inicio), 5) +
                                            truncar_decimal(base_calculo * tasa_a_aplicar / 100 * ((fecha_fin - dt.datetime(fecha_fin.year, 1, 1)).days + 1) / dias_año(fecha_fin), 5))
        else:
            importe_calculo_periodo_roto = base_calculo * tasa_a_aplicar / 100 * (pd.to_datetime(fecha_fin) - pd.to_datetime(fecha_inicio)).days / dias_año(fecha_fin)
    else:
        importe_calculo_periodo_roto = base_calculo * tasa_a_aplicar / 100 * (pd.to_datetime(fecha_fin) - pd.to_datetime(fecha_inicio)).days / w_DIAS_BASE
    
    return redondear_decimal(importe_calculo_periodo_roto)



def calcular_seguro_capitalizado(capital_com_apertura,
                                 plazo,
                                 seguro_titular_1,
                                 seguro_titular_2):

    '''Calcular el seguro de vida en base al capital prestado, el tipo de seguro, el número de personas aseguradas y la duración del préstamo'''
    tasa_titular_1 = obtener_tasa_seguro_auto(plazo,
                                              seguro_titular_1)
    tasa_titular_2 = obtener_tasa_seguro_auto(plazo,
                                              seguro_titular_2)
    seguro_capitalizado = redondear_decimal(capital_com_apertura * tasa_titular_1) + redondear_decimal(capital_com_apertura * tasa_titular_2)
    
    return redondear_decimal(seguro_capitalizado)



def dias_año(fecha):

    '''Función para recuperar el número de días del año de una fecha dada'''
    return 366 if cl.isleap(fecha.year) else 365



def formatear_decimales(value) -> str:
    """Formatea un valor numérico como moneda con coma decimal."""
    if isinstance(value, Decimal):
        value = float(value)
    if value is None:
        return "0,00"

    return f"{value:.2f}".replace('.', ',')



def generar_excel(df_resumen=None, df_tamo=None, df_ejemplo=None, df_tae=None, df_secuencias=None, resultado_simulacion_masiva=None, df_errores=None):
    
    '''Función para generar un archivo Excel con varias hojas a partir de los DataFrames proporcionados'''
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
        if df_errores is not None:
            df_errores.to_excel(writer, sheet_name="Errores", index=False)
    output.seek(0)

    return output



def mostrar_fecha(fecha):

    ''' Función para devolver la fecha formateada a dd/mm/yyyy '''
    if fecha is not None and pd.notnull(fecha):
        fecha = pd.to_datetime(fecha, format='%d/%m/%Y').strftime('%d/%m/%Y') 
    else:
        return None    

    return fecha



def obtener_tasa_seguro_auto(plazo,
                             tipo_seguro):

    # Cada tupla: (plazo_máximo, tasa_vida_plus, tasa_vida, tasa_otro)
    rangos = [
        (24, 0.0476, 0.0141, 0.0),
        (36, 0.0555, 0.0220, 0.0),
        (48, 0.0635, 0.0300, 0.0),
        (60, 0.0691, 0.0356, 0.0),
        (72, 0.0782, 0.0447, 0.0),
        (84, 0.0882, 0.0547, 0.0),
        (96, 0.0992, 0.0657, 0.0),
        (108, 0.1110, 0.0775, 0.0),
        (float('inf'), 0.1241, 0.0906, 0.0)
    ]
    for max_plazo, tasa_vida_plus, tasa_plus, tasa_otro in rangos:
        if plazo < max_plazo + 1:
            return (
                truncar_decimal(tasa_vida_plus, 4) if tipo_seguro == 2 # 2 = Vida +
                else truncar_decimal(tasa_plus, 4) if tipo_seguro == 1 # 1 = Vida
                else truncar_decimal(tasa_otro, 4) # None = Sin seguro 
                )
    
    return truncar_decimal(0.0, 4)



def rcc_obtener_cuota(capital,vitesse):

    '''Función para calcular la cuota mensual en base al capital y el porcentaje de vitesse seleccionado'''
    return redondear_decimal(capital * vitesse / 100)



def rcc_opciones_cuota(capital):

    '''Función para listar las cuotas posibles en base a las vitesse disponibles para un capital dado'''
    listado_mensualidades = []
    for i in RCC_OPCIONES_VITESSE:
        listado_mensualidades.append(rcc_obtener_cuota(capital, i))
        
    return listado_mensualidades



def redondear_decimal(valor):

    '''Función para redondear un número decimal a 2 decimales'''
    return bascular_a_decimal(valor, ROUND_HALF_UP)



def redondear_decimal_superior(valor):

    '''Función para redondear un número decimal a 2 decimales'''
    return bascular_a_decimal(valor, ROUND_CEILING)



def truncar_decimal(valor,
                    decimales):

    '''Función para truncar un número decimal a un número específico de decimales sin redondear'''
    if not isinstance(valor, Decimal):
        valor = Decimal(str(valor))
    formato = '0.' + '0' * decimales

    return valor.quantize(Decimal(formato), rounding=ROUND_DOWN)
