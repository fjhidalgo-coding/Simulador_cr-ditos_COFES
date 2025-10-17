#!
'''Programa para la simulación de los productos amortizables de COF_ES'''

import math
import pandas as pd 
import calendar



''' Declarar constantes'''

DIAS_BASE = 360
LISTA_SEGURO = ["Seguro ADE", "Sin seguro", "Vida Plus", "Vida"]
PRODUCTOS_DICCIONARIO = pd.read_csv('COFES_00_PRODUCTOS_DICCIONARIO.csv', sep=',', dayfirst=True).sort_values(by="Código de producto POPS")
LISTA_PRODUCTOS = list(PRODUCTOS_DICCIONARIO['Nombre del producto'].values)


''' Declarar variables globales '''

capital_prestado = 0.00
comision_apertura = 0.00
tasa_comision_apertura = 0.00
imp_max_com_apertura = 0.00
comision_apertura_capitalizada = False
etiqueta_producto = ""
fechas_bloqueo = pd.read_csv('COFES_01_Date_Blocage.csv', sep=';', parse_dates=['Fecha_BLOQUEO'], dayfirst=True).sort_values(by='Fecha_BLOQUEO')
tipo_vencimiento = []
numero_vencimiento = []
fecha_vencimiento = []
capital_inicial = []
mensualidad_vencimiento = []
intereses_vencimiento = []
intereses_diferidos_vencimiento = []
intereses_capitalizados_vencimiento = []
seguro_vencimiento = []
seguro_diferidos_vencimiento = []
seguro_capitalizados_vencimiento = []
comisiones_vencimiento = []
capital_financiado_periodo = []
capital_vencimiento = []
capital_pendiente = []
cuota_tae = []
año_base = []
tiempo = []
van_cuota_tae = []
f_inicio_periodo = []
mensualidad_contractual = []
tasa_periodo = []



''' Crear las funciones necesarias para la simulación '''

def truncar_decimal(valor, decimales):
    '''Función para truncar un número decimal a un número específico de decimales sin redondear'''
    factor = 10 ** decimales
   
    return int(valor * factor) / factor



def calcular_periodo_roto(base_calculo, fecha_inicio, fecha_fin, tasa_a_aplicar):
    '''Calcular el interés o el seguro cuando el día de inicio de periodo no coincide con el día de fin de periodo'''
    importe_calculo_periodo_roto = round(base_calculo * tasa_a_aplicar / 100 * (pd.to_datetime(fecha_fin) - pd.to_datetime(fecha_inicio)).days / DIAS_BASE, 2)
    
    return importe_calculo_periodo_roto



def calcular_periodo(base_calculo, fecha_inicio, fecha_fin, tasa_a_aplicar):
    '''Calcular el interés o el seguro cuando el periodo está completo'''
    importe_calculo_periodo = round(base_calculo * tasa_a_aplicar / 1200, 2) * ((fecha_fin.year - fecha_inicio.year) * 12 + (fecha_fin.month - fecha_inicio.month))
   
    return importe_calculo_periodo



def calcular_comision_apertura(capital_prestado, tasa_comision_apertura, imp_max_com_apertura, comision_apertura_capitalizada):
    '''Calcular la comisión de apertura en base al capital prestado y el porcentaje definido'''
    comision_apertura = round(capital_prestado * tasa_comision_apertura / 100, 2)
    if comision_apertura > imp_max_com_apertura and imp_max_com_apertura > 0:
        '''Comprobar que la comisión calculada no supera el límite marcado; si fuese el caso, actualizamos el valor de la comisión con el límite'''
        comision_apertura = imp_max_com_apertura
    if comision_apertura_capitalizada:
        capitalizacion_comision_apertura = comision_apertura
    else:
        capitalizacion_comision_apertura = 0.00
   
    return comision_apertura, capitalizacion_comision_apertura



def obtener_tasa_seguro_ade(seguro_titular_1, seguro_titular_2):
    if seguro_titular_1 == "Seguro ADE" and seguro_titular_2 == "Seguro ADE":
        tasa_ade = 7.68
    elif seguro_titular_1 == "Seguro ADE" or seguro_titular_2 == "Seguro ADE":
        tasa_ade = 4.44
    else:
        tasa_ade = 0.00
    
    return tasa_ade



def obtener_tasa_seguro_auto(plazo, tipo_seguro):
    # Cada tupla: (plazo_máximo, tasa_vida_plus, tasa_vida, tasa_otro)
    rangos = [
        (24, 0.04760, 0.01410, 0.0),
        (36, 0.05550, 0.02200, 0.0),
        (48, 0.06350, 0.03000, 0.0),
        (60, 0.06910, 0.03560, 0.0),
        (72, 0.07820, 0.04470, 0.0),
        (84, 0.08820, 0.05470, 0.0),
        (96, 0.09920, 0.06570, 0.0),
        (108, 0.11100, 0.07750, 0.0),
        (float('inf'), 0.12410, 0.09060, 0.0)
    ]
    for max_plazo, tasa_vida_plus, tasa_plus, tasa_otro in rangos:
        if plazo < max_plazo + 1:
            return (
                tasa_vida_plus if tipo_seguro == "Vida Plus"
                else tasa_plus if tipo_seguro == "Vida"
                else tasa_otro
                )
    
    return 0.0



def calcular_seguro_capitalizado(capital_com_apertura, plazo, seguro_titular_1, seguro_titular_2):
    '''Calcular el seguro de vida en base al capital prestado, el tipo de seguro, el número de personas aseguradas y la duración del préstamo'''
    tasa_titular_1 = obtener_tasa_seguro_auto(plazo, seguro_titular_1)
    tasa_titular_2 = obtener_tasa_seguro_auto(plazo, seguro_titular_2)
    seguro_capitalizado = round(capital_com_apertura * tasa_titular_1, 2) + round(capital_com_apertura * tasa_titular_2, 2)
    
    return seguro_capitalizado



def calculo_fechas(etiqueta_producto, fecha_financiacion, dia_pago, carencia):
    '''Función para calcular las principales fechas de préstamo'''
    fecha_financiacion = pd.to_datetime(fecha_financiacion)
    fecha_fin_carencia = pd.to_datetime("")
    fecha_fin_carencia_diferida = pd.to_datetime("")
    fecha_fin_carencia_gratuita_forzada = pd.to_datetime("")
    
    '''Calcular la fecha del primer vencimiento en base a la fecha de bloqueo posterior a la fecha de financiación'''
    proximas_db = fechas_bloqueo[fechas_bloqueo['Fecha_BLOQUEO'] >= fecha_financiacion]
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

    return fecha_fin_carencia_gratuita_forzada, fecha_fin_carencia_diferida, fecha_fin_carencia, fecha_primer_vencimiento



def descuento_partner(importe_crédito, tasa, carencia, plazo, plazo_2sec):
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

    return descuento



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
                                  fecha_fin_carencia):
    '''Función para calcular la mensualidad estándar de los productos amortizables de COF_ES'''
    
    '''Incremantar el capital de la operación con el interés y seguro capitalizado al finalizar carencia'''
    if carencia == 1:
        importe_crédito += round((importe_crédito * tasa_global / 1200),2) * carencia
    if carencia > 1:
        w_fecha_ultimo_vencimiento_tratado = (fecha_fin_carencia_gratuita_forzada if fecha_fin_carencia_gratuita_forzada is not None and pd.notnull(fecha_fin_carencia_gratuita_forzada)
                                                                                  else fecha_fin_carencia_diferida
                                                                                  if fecha_fin_carencia_diferida is not None and pd.notnull(fecha_fin_carencia_diferida)
                                                                                  else fecha_financiacion)
        importe_crédito += calcular_periodo_roto(importe_crédito, w_fecha_ultimo_vencimiento_tratado, fecha_fin_carencia, tasa_ade)
        importe_crédito += round((importe_crédito * tasa / 1200),2) * carencia
        
    '''Calcular la mensualidad contractual del préstamo rendondeando al céntimo superior para asegurar la ventilación de todo el capital'''
    if tasa_global == 0.00:
        cuota_1sec = math.ceil((importe_crédito - capital_2sec) / plazo * 100) / 100
    else:
        cuota_1sec = (round(capital_2sec * tasa_global / 1200, 2) 
                      + math.ceil((importe_crédito - capital_2sec) * tasa_global / 1200 * ((1 + (tasa_global / 1200)) ** plazo) / (((1 + (tasa_global / 1200)) ** plazo) - 1) * 100 ) / 100)
    

    '''Calcular la mensualidad de la segunda secuencia en caso de que exista'''
    if capital_2sec != 0.00:
        if tasa_2sec == 0.00:
            cuota_2sec = math.ceil(capital_2sec / plazo_2sec * 100) / 100
        else:
            cuota_2sec = math.ceil(capital_2sec * tasa_2sec / 1200 * ((1 + (tasa_2sec / 1200)) ** plazo_2sec) / (((1 + (tasa_2sec / 1200)) ** plazo_2sec) - 1) * 100 ) / 100
    else:
        cuota_2sec = 0.00
    
    return cuota_1sec, cuota_2sec



def calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion,w_fecha_ultimo_vencimiento_tratado, w_dia_año):
    '''Función para calcular la fracción del año entre la fecha de financiación y el vencimiento tratado'''
    w_dia_año_anterior = 366 if calendar.isleap(w_fecha_ultimo_vencimiento_tratado.year - 1) else 365
    w_dia_año_anterior = w_dia_año if pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).year ==  pd.to_datetime(fecha_financiacion).year else w_dia_año_anterior 
    delta_años = 0 if (w_fecha_ultimo_vencimiento_tratado.year - fecha_financiacion.year + 1) < 1 else w_fecha_ultimo_vencimiento_tratado.year - fecha_financiacion.year + 1
    w_aniversario_fecha_financiación = fecha_financiacion + pd.DateOffset(years=delta_años)
    
    if w_dia_año != w_dia_año_anterior and w_fecha_ultimo_vencimiento_tratado < w_aniversario_fecha_financiación:
        delta_años = delta_años - 1 if delta_años > 1 else 0
        w_aniversario_fecha_financiación += pd.DateOffset(years=-1)
        fraccion_año = (delta_años + ((w_dia_año_anterior - pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año_anterior)  
                       + ((pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).dayofyear) / w_dia_año))
    elif w_fecha_ultimo_vencimiento_tratado > w_aniversario_fecha_financiación:
        fraccion_año = (0 if delta_años < 1 else delta_años) + ((pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).dayofyear - pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año)
    else:
        delta_años = delta_años - 1 if delta_años > 1 else 0
        w_aniversario_fecha_financiación += pd.DateOffset(years=-1)
        fraccion_año = delta_años + ((pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).dayofyear - pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año)

    return round(fraccion_año, 7)



def calcular_tae(cuota_tae, tiempo, tasa, tolerancia=0.000001, max_iteraciones=1000):
    '''Función para calcular la TAE de la operación'''
    tae = (1 + tasa / 1200) ** 12 - 1  # TAE inicial aproximada
    for _ in range(max_iteraciones):
        van_cuota_tae.clear()
        for i in range(len(cuota_tae)):
            van_cuota_tae.append(round(cuota_tae[i] / ((1 + tae) ** tiempo[i]),7))
            
        if abs(sum(van_cuota_tae)) < tolerancia:  # Comprueba si el VAN está dentro de la tolerancia
            return tae
        
        if sum(van_cuota_tae) < 0:
            tae -= 0.0001
        else:
            tae += 0.0001
        
    return round(tae * 100,2)



def alimentar_cuadro_amortizacion(w_tipo_vencimiento, 
                                  w_numero_vencimiento, 
                                  w_fecha_vencimiento, 
                                  w_capital_inicial, 
                                  w_mensualidad_vencimiento, 
                                  w_intereses_vencimiento, 
                                  w_intereses_diferidos_vencimiento, 
                                  w_intereses_capitalizados_vencimiento, 
                                  w_seguro_vencimiento, 
                                  w_seguro_diferidos_vencimiento, 
                                  w_seguro_capitalizados_vencimiento, 
                                  w_comisiones_vencimiento, 
                                  w_capital_financiado_periodo, 
                                  w_capital_vencimiento, 
                                  w_capital_pendiente, 
                                  w_cuota_tae, 
                                  w_año_base, 
                                  w_tiempo, 
                                  w_f_inicio_periodo, 
                                  w_mensualidad_contractual, 
                                  w_tasa_periodo):
    '''Función para almacenar la construcción del cuadro de amortización asociado a la instrucción'''
    tipo_vencimiento.append(w_tipo_vencimiento)
    numero_vencimiento.append(w_numero_vencimiento)
    fecha_vencimiento.append(w_fecha_vencimiento)
    capital_inicial.append(w_capital_inicial)
    mensualidad_vencimiento.append(w_mensualidad_vencimiento)
    intereses_vencimiento.append(w_intereses_vencimiento)
    intereses_diferidos_vencimiento.append(w_intereses_diferidos_vencimiento)
    intereses_capitalizados_vencimiento.append(w_intereses_capitalizados_vencimiento)
    seguro_vencimiento.append(w_seguro_vencimiento)
    seguro_diferidos_vencimiento.append(w_seguro_diferidos_vencimiento)
    seguro_capitalizados_vencimiento.append(w_seguro_capitalizados_vencimiento)
    comisiones_vencimiento.append(w_comisiones_vencimiento)
    capital_financiado_periodo.append(w_capital_financiado_periodo)
    capital_vencimiento.append(w_capital_vencimiento)
    capital_pendiente.append(w_capital_pendiente)
    cuota_tae.append(w_cuota_tae)
    año_base.append(w_año_base)
    tiempo.append(w_tiempo)
    f_inicio_periodo.append(w_f_inicio_periodo)
    mensualidad_contractual.append(w_mensualidad_contractual)
    tasa_periodo.append(w_tasa_periodo)



def simular_prestamo_CLB(etiqueta_producto, 
                         fecha_financiacion, 
                         dia_pago, 
                         tasa, 
                         capital_prestado, 
                         plazo, 
                         carencia, 
                         tasa_2sec, 
                         capital_2sec, 
                         plazo_2sec, 
                         seguro_titular_1, 
                         seguro_titular_2, 
                         tasa_comision_apertura, 
                         comision_apertura_capitalizada, 
                         imp_max_com_apertura):
    '''Función principal para la simulación de los productos amortizables de COF_ES'''
    
    '''Calcular la comisión de apertura'''
    comision_apertura, capitalizacion_comision_apertura = calcular_comision_apertura(capital_prestado, tasa_comision_apertura, imp_max_com_apertura, comision_apertura_capitalizada)
    
    '''Calcular variable con la capitalización de la comisión de apertura'''
    capital_com_apertura = capital_prestado + capitalizacion_comision_apertura
    
    '''Calcular el seguro de vida capitalizado'''
    seguro_capitalizado = calcular_seguro_capitalizado(capital_com_apertura, plazo, seguro_titular_1, seguro_titular_2)
    
    '''Calcular el importe del crédito incluyendo capital, comisión de apertura capitalizada y seguro capitalizado'''
    importe_crédito = capital_com_apertura + seguro_capitalizado
    
    '''Calcular el descuento y modificar la tasa de interés de los productos con interés partner'''
    if LISTA_PRODUCTOS.index(etiqueta_producto) in (4, 5, 6):
        descuento = descuento_partner(importe_crédito, tasa, carencia, plazo, plazo_2sec)
        tasa = 0.00
    else:
        descuento = 0.00
    
    '''Calcular la tasa del seguro ADE'''
    tasa_ade = obtener_tasa_seguro_ade(seguro_titular_1, seguro_titular_2)
    
    '''Calcular la tasa a utilizar para el cálculo de la mensualidad (incluye el seguro ADE; de la primera secuencia para los productos con 2 secuencias)'''
    tasa_global = tasa + tasa_ade
    
    '''Calcular las fechas que nos permiten generar el cuadro de amortización'''
    fecha_fin_carencia_gratuita_forzada, fecha_fin_carencia_diferida, fecha_fin_carencia, fecha_primer_vencimiento = calculo_fechas(etiqueta_producto, fecha_financiacion, dia_pago, carencia)
    
    '''Calcular las mensualidades contractuales de todas las secuencias del contrato'''
    cuota_1sec, cuota_2sec = calcular_mensualidad_estandar(importe_crédito, 
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
                                                           fecha_fin_carencia)
    
    '''Generar el cuadro de amortización de la operación simulada'''
    tipo_vencimiento.clear()
    numero_vencimiento.clear()
    fecha_vencimiento.clear()
    capital_inicial.clear()
    mensualidad_vencimiento.clear()
    intereses_vencimiento.clear()
    intereses_diferidos_vencimiento.clear()
    intereses_capitalizados_vencimiento.clear()
    seguro_vencimiento.clear()
    seguro_diferidos_vencimiento.clear()
    seguro_capitalizados_vencimiento.clear()
    comisiones_vencimiento.clear()
    capital_financiado_periodo.clear()
    capital_vencimiento.clear()
    capital_pendiente.clear()
    cuota_tae.clear()
    año_base.clear()
    tiempo.clear()
    van_cuota_tae.clear()
    f_inicio_periodo.clear()
    mensualidad_contractual.clear()
    tasa_periodo.clear()

    '''Generar el vencimiento de financiación'''
    cuadro_amortizacion = pd.DataFrame()
    if plazo_2sec > 0:
        w_tipo_vencimiento="Amort. 1ª sec."
    else:
        w_tipo_vencimiento="Amortización"
    w_fecha_ultimo_vencimiento_tratado = fecha_financiacion
    w_capital_pendiente = importe_crédito
    w_intereses_diferidos_vencimiento = 0.00
    w_seguro_diferidos_vencimiento = 0.00
    alimentar_cuadro_amortizacion("Financiación",
                                  0,
                                  fecha_financiacion,
                                  0.00,
                                  0.00,
                                  0.00,
                                  0.00,
                                  0.00,
                                  0.00,
                                  0.00,
                                  seguro_capitalizado,
                                  capitalizacion_comision_apertura,
                                  capital_prestado,
                                  -importe_crédito,
                                  importe_crédito,
                                  -capital_prestado,
                                  366 if calendar.isleap(fecha_financiacion.year) else 365,
                                  0,
                                  fecha_financiacion,
                                  0.00,
                                  0.00)

    '''Generar el vencimiento de carencia gratuita forzada'''
    if fecha_fin_carencia_gratuita_forzada is not None and pd.notnull(fecha_fin_carencia_gratuita_forzada):        
        alimentar_cuadro_amortizacion("Carencia gratuita forzada",
                                      0,
                                      fecha_fin_carencia_gratuita_forzada,
                                      w_capital_pendiente,
                                      0.00,
                                      0.00,
                                      0.00,
                                      0.00,
                                      0.00,
                                      0.00,
                                      0.00,
                                      0.00,
                                      0.00,
                                      0.00,
                                      w_capital_pendiente,
                                      0.00,
                                      366 if calendar.isleap(fecha_fin_carencia_gratuita_forzada.year) else 365,
                                      0,
                                      w_fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                      0.00,
                                      0.00)
        w_fecha_ultimo_vencimiento_tratado = fecha_fin_carencia_gratuita_forzada

    '''Generar el vencimiento de carencia diferida'''
    if fecha_fin_carencia_diferida is not None and pd.notnull(fecha_fin_carencia_diferida):        
        w_intereses_diferidos_vencimiento = calcular_periodo_roto(w_capital_pendiente, w_fecha_ultimo_vencimiento_tratado, fecha_fin_carencia_diferida, tasa)
        w_seguro_diferidos_vencimiento = calcular_periodo_roto(w_capital_pendiente, w_fecha_ultimo_vencimiento_tratado, fecha_fin_carencia_diferida, tasa_ade)
        alimentar_cuadro_amortizacion("Carencia diferida",
                                      0,
                                      fecha_fin_carencia_diferida,
                                      w_capital_pendiente,
                                      0.00,
                                      0.00,
                                      w_intereses_diferidos_vencimiento,
                                      0.00,
                                      0.00,
                                      w_seguro_diferidos_vencimiento,
                                      0.00,
                                      0.00,
                                      0.00,
                                      0.00,
                                      w_capital_pendiente,
                                      0.00,
                                      366 if calendar.isleap(fecha_fin_carencia_diferida.year) else 365,
                                      0,
                                      w_fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                      0.00,
                                      tasa)
        w_fecha_ultimo_vencimiento_tratado = fecha_fin_carencia_diferida

    '''Generar el vencimiento de carencia normal'''
    if fecha_fin_carencia is not None and pd.notnull(fecha_fin_carencia):        
        w_capital_inicial = w_capital_pendiente
        w_intereses_capitalizados_vencimiento = calcular_periodo(w_capital_pendiente, w_fecha_ultimo_vencimiento_tratado, fecha_fin_carencia, tasa)
        if carencia == 1:
            w_seguro_capitalizados_vencimiento = calcular_periodo(w_capital_pendiente, w_fecha_ultimo_vencimiento_tratado, fecha_fin_carencia, tasa_ade)
        else:
            w_seguro_capitalizados_vencimiento = calcular_periodo_roto(w_capital_pendiente, w_fecha_ultimo_vencimiento_tratado, fecha_fin_carencia, tasa_ade)
        w_capital_pendiente = round(w_capital_inicial + w_intereses_capitalizados_vencimiento + w_seguro_capitalizados_vencimiento, 2)
        alimentar_cuadro_amortizacion("Carencia normal",
                                      0,
                                      fecha_fin_carencia,
                                      w_capital_inicial,
                                      0.00,
                                      0.00,
                                      0.00,
                                      w_intereses_capitalizados_vencimiento,
                                      0.00,
                                      0.00,
                                      w_seguro_capitalizados_vencimiento,
                                      0.00,
                                      0.00,
                                      -w_intereses_capitalizados_vencimiento - w_seguro_capitalizados_vencimiento,
                                      w_capital_pendiente,
                                      0.00,
                                      366 if calendar.isleap(fecha_fin_carencia.year) else 365,
                                      0,
                                      w_fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                      0.00,
                                      tasa)
        w_fecha_ultimo_vencimiento_tratado = fecha_fin_carencia

    '''Primer vencimiento de amortización'''
    w_numero_vencimiento = 1
    w_capital_inicial = w_capital_pendiente
    if pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).day == pd.to_datetime(fecha_primer_vencimiento).day:
        w_intereses_vencimiento = calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa) + w_intereses_diferidos_vencimiento
        w_seguro_vencimiento = calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa_ade) + w_seguro_diferidos_vencimiento
        w_ajustes = w_intereses_diferidos_vencimiento + w_seguro_diferidos_vencimiento
    else:
        w_intereses_vencimiento = calcular_periodo_roto(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa) + w_intereses_diferidos_vencimiento
        w_seguro_vencimiento = calcular_periodo_roto(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa_ade) + w_seguro_diferidos_vencimiento
        w_ajustes = (w_intereses_vencimiento + w_seguro_vencimiento 
                     - calcular_periodo(w_capital_inicial, fecha_primer_vencimiento + pd.DateOffset(months=-1), fecha_primer_vencimiento, tasa) 
                     - calcular_periodo(w_capital_inicial, fecha_primer_vencimiento + pd.DateOffset(months=-1), fecha_primer_vencimiento, tasa_ade))
    w_comision_apertura = comision_apertura - capitalizacion_comision_apertura
    w_mensualidad_vencimiento = cuota_1sec + w_comision_apertura + w_ajustes
    w_capital_vencimiento = round(w_mensualidad_vencimiento - w_intereses_vencimiento - w_seguro_vencimiento - w_comision_apertura, 2)
    w_capital_pendiente = round(w_capital_inicial - w_capital_vencimiento, 2)
    w_dia_año = 366 if calendar.isleap(fecha_primer_vencimiento.year) else 365
    alimentar_cuadro_amortizacion(w_tipo_vencimiento,
                                  w_numero_vencimiento,
                                  fecha_primer_vencimiento,
                                  w_capital_inicial,
                                  w_mensualidad_vencimiento,
                                  w_intereses_vencimiento,
                                  0.00,
                                  0.00,
                                  w_seguro_vencimiento,
                                  0.00,
                                  0.00,
                                  w_comision_apertura,
                                  0.00,
                                  w_capital_vencimiento,
                                  w_capital_pendiente,
                                  w_intereses_vencimiento + w_capital_vencimiento + comision_apertura,  # Forzamos la cuota TAE para que incluya la comisión de apertura (ver SARA)
                                  w_dia_año,
                                  calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion, fecha_primer_vencimiento,w_dia_año),
                                  w_fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                  cuota_1sec,
                                  tasa)
    w_fecha_ultimo_vencimiento_tratado = fecha_primer_vencimiento

    '''Resto de vencimientos de la primera secuencia'''
    for i in range(2, plazo + 1):
        w_numero_vencimiento += 1
        w_capital_inicial = w_capital_pendiente
        w_fecha_vencimiento_calculado = w_fecha_ultimo_vencimiento_tratado + pd.DateOffset(months=1)
        w_seguro_vencimiento = calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, w_fecha_vencimiento_calculado, tasa_ade)
        if (w_numero_vencimiento == plazo 
            and cuota_1sec < calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, w_fecha_vencimiento_calculado, tasa) + w_capital_inicial + w_seguro_vencimiento - capital_2sec):
            w_intereses_vencimiento = (calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, w_fecha_vencimiento_calculado, tasa) 
                                       - (calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, w_fecha_vencimiento_calculado, tasa) 
                                          + w_capital_inicial + w_seguro_vencimiento - capital_2sec - cuota_1sec))
        else:
            w_intereses_vencimiento = calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, w_fecha_vencimiento_calculado, tasa)
        if cuota_1sec < w_capital_inicial + w_intereses_vencimiento + w_seguro_vencimiento - capital_2sec:
            w_mensualidad_vencimiento = cuota_1sec
        else:
            w_mensualidad_vencimiento = w_capital_inicial + w_intereses_vencimiento + w_seguro_vencimiento - capital_2sec
        w_capital_vencimiento = round(w_mensualidad_vencimiento - w_intereses_vencimiento - w_seguro_vencimiento, 2)
        w_capital_pendiente = round(w_capital_inicial - w_capital_vencimiento, 2)
        w_dia_año = 366 if calendar.isleap(fecha_primer_vencimiento.year) else 365
        alimentar_cuadro_amortizacion(w_tipo_vencimiento,
                                      w_numero_vencimiento,
                                      w_fecha_ultimo_vencimiento_tratado,
                                      w_capital_inicial,
                                      w_mensualidad_vencimiento,
                                      w_intereses_vencimiento,
                                      0.00,
                                      0.00,
                                      w_seguro_vencimiento,
                                      0.00,
                                      0.00,
                                      0.00,
                                      0.00,
                                      w_capital_vencimiento,
                                      w_capital_pendiente,
                                      w_intereses_vencimiento + w_capital_vencimiento,
                                      w_dia_año,
                                      calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion, w_fecha_ultimo_vencimiento_tratado,w_dia_año),
                                      w_fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                      cuota_1sec,
                                      tasa)
        w_fecha_ultimo_vencimiento_tratado = w_fecha_vencimiento_calculado

    '''Generar los vencimientos de la segunda secuencia en caso de que exista'''
    if plazo_2sec > 0:
        for i in range(1, plazo_2sec + 1):
            w_numero_vencimiento += 1
            w_capital_inicial = w_capital_pendiente
            w_fecha_vencimiento_calculado = w_fecha_ultimo_vencimiento_tratado + pd.DateOffset(months=1)
            w_seguro_vencimiento = calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, w_fecha_vencimiento_calculado, tasa_ade)
            if (w_numero_vencimiento == plazo_2sec + plazo
                and cuota_2sec < calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, w_fecha_vencimiento_calculado, tasa_2sec) + w_capital_inicial + w_seguro_vencimiento):
                w_intereses_vencimiento = (calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, w_fecha_vencimiento_calculado, tasa_2sec)
                                           - (calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, w_fecha_vencimiento_calculado, tasa_2sec) 
                                              + w_capital_inicial + w_seguro_vencimiento - cuota_2sec))
            else:
                w_intereses_vencimiento = calcular_periodo(w_capital_inicial, w_fecha_ultimo_vencimiento_tratado, w_fecha_vencimiento_calculado, tasa_2sec)
            if cuota_2sec < w_capital_inicial + w_intereses_vencimiento + w_seguro_vencimiento:
                w_mensualidad_vencimiento = cuota_2sec
            else:
                w_mensualidad_vencimiento = w_capital_inicial + w_intereses_vencimiento + w_seguro_vencimiento
            w_capital_vencimiento = round(w_mensualidad_vencimiento - w_intereses_vencimiento - w_seguro_vencimiento, 2)
            w_capital_pendiente = round(w_capital_inicial - w_capital_vencimiento, 2)
            w_dia_año = 366 if calendar.isleap(fecha_primer_vencimiento.year) else 365
            alimentar_cuadro_amortizacion("Amort. 2ª sec.",
                                          w_numero_vencimiento,
                                          w_fecha_ultimo_vencimiento_tratado,
                                          w_capital_inicial,
                                          w_mensualidad_vencimiento,
                                          w_intereses_vencimiento,
                                          0.00,
                                          0.00,
                                          w_seguro_vencimiento,
                                          0.00,
                                          0.00,
                                          0.00,
                                          0.00,
                                          w_capital_vencimiento,
                                          w_capital_pendiente,
                                          w_intereses_vencimiento + w_capital_vencimiento,
                                          w_dia_año,
                                          calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion, w_fecha_ultimo_vencimiento_tratado,w_dia_año),
                                          w_fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                          cuota_2sec,
                                          tasa_2sec)
            w_fecha_ultimo_vencimiento_tratado = w_fecha_vencimiento_calculado
    
    ''' Calcular la TAE de la operación con el listado de "cuota_tae", la fracción temporal entre la financiación y el vencimiento y el TIN'''
    tae = calcular_tae(cuota_tae, tiempo, tasa)
    
    ''' Crear el diccionario con los datos del cuadro de amortización y de la TAE'''
    datos_amortizacion = {
    'Tipo vcto' : tipo_vencimiento,
    'Nº Vcto' : numero_vencimiento,
    'F_Inicio' : f_inicio_periodo,
    'F_Vcto' : fecha_vencimiento,
    'TIN' : tasa_periodo,
    'Int. CAP. vcto' : intereses_capitalizados_vencimiento,
    'ASS CAP. vcto' : seguro_capitalizados_vencimiento,
    'Com. vcto' : comisiones_vencimiento,
    'Cap. finan.' : capital_financiado_periodo,
    'Cap. inicial' : capital_inicial,
    'Mens. vcto' : mensualidad_vencimiento,
    'Int. vcto' : intereses_vencimiento,
    'ASS vcto' : seguro_vencimiento,
    'Cap. vcto' : capital_vencimiento,
    'Cap. PDTE' : capital_pendiente,
    'Cuota teórica' : mensualidad_contractual,
    'Int. DIFF vcto' : intereses_diferidos_vencimiento,
    'ASS DIFF vcto' : seguro_diferidos_vencimiento,
}
    datos_tae = {
    'Fecha_Vencimiento' : fecha_vencimiento,
    'cuota_tae' : cuota_tae,
    'Año_Base' : año_base,
    'Tiempo': tiempo,
    'van_cuota_tae' : van_cuota_tae
}
    '''Crear el dataframe con el cuadro de amortización a mostrar'''
    cuadro_amortizacion = pd.DataFrame(datos_amortizacion)
    
    '''Crear el dataframe con el cuadro de cálculo TAE a mostrar'''
    input_tae = pd.DataFrame(datos_tae)
    
    ''' Crear las variables con los sumatorios del cuadro de amortización'''
    intereses = sum(intereses_vencimiento) + sum(intereses_capitalizados_vencimiento) 
    coste_seguro = sum(seguro_vencimiento) + sum(seguro_capitalizados_vencimiento)
    coste_total = intereses + comision_apertura # + coste_seguro
    importe_total_a_pagar = sum(mensualidad_vencimiento)
    
    mostrar_fecha = lambda fecha: fecha.strftime('%d/%m/%Y') if fecha is not None and pd.notnull(fecha) else "No disponible"
        
    cuadro_secuencias = cuadro_amortizacion[cuadro_amortizacion['Tipo vcto'] != "Financiación"]
    
    cuenta_vencimientos = cuadro_secuencias['Tipo vcto'].value_counts()
    primeros = cuadro_secuencias.groupby('Tipo vcto').head(1)
    ultimos = cuadro_secuencias.groupby('Tipo vcto').tail(1)

    resumen1 = pd.DataFrame(
        {
            "TAE": [f"{tae:.2f}".replace('.', ',')],
        },
    index=["%"],
    )

    resumen2 = pd.DataFrame(
        {
            "Importe total a pagar": [f"{importe_total_a_pagar:.2f}".replace('.', ',')],
            "Capital": [f"{capital_prestado:.2f}".replace('.', ',')],
            "Prima de seguro": [f"{coste_seguro:.2f}".replace('.', ',')],
            "Coste total": [f"{coste_total:.2f}".replace('.', ',')],
            "Intereses": [f"{intereses:.2f}".replace('.', ',')],
            "Comisión de apertura": [f"{comision_apertura:.2f}".replace('.', ',')],
            "Importe del crédito": [f"{importe_crédito:.2f}".replace('.', ',')],
            "Descuento Partner": [f"{descuento:.2f}".replace('.', ',')],
        },
    index=["EUR"],
    )

    resumen3 = pd.DataFrame(
    {
        "Nº Vencimientos": cuenta_vencimientos.loc[ultimos['Tipo vcto']].values,
        "TIN": [f"{tin:.2f}".replace('.', ',') for tin in primeros['TIN'].values],
        "F_INI": [mostrar_fecha(fecha) for fecha in primeros['F_Inicio'].values],
        "IMP_Cuota": [f"{cuota:.2f}".replace('.', ',') for cuota in primeros['Cuota teórica'].values],
        "F_1er_VCTO":  [mostrar_fecha(fecha) for fecha in primeros['F_Vcto'].values],
        "IMP_1era_Cuota": [f"{prim_vcto :.2f}".replace('.', ',') for prim_vcto in primeros['Mens. vcto'].values],
        "F_FIN":  [mostrar_fecha(fecha) for fecha in ultimos['F_Vcto'].values],
        "IMP_ULT_Cuota": [f"{ult_vcto :.2f}".replace('.', ',') for ult_vcto in ultimos['Mens. vcto'].values],
    },
    index=ultimos['Tipo vcto'].values,
    )
    
    ej_repr_seccion_1 = f"Ejemplo representativo:\n\nPara un préstamo de importe/PVP {f'{capital_prestado:.2f}'.replace('.', ',')} €, con un tipo de interés fijo del {f'{tasa:.2f}'.replace('.', ',')} % anual y TAE de {f'{tae:.2f}'.replace('.', ',')} %, "

    if LISTA_PRODUCTOS.index(etiqueta_producto) in (6, 7):
        if cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2] == 1:
            ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2]} mensualidades, de {f'{primeros['Mens. vcto'].values[-2]:.2f}'.replace('.', ',')} € al mes. "
        else:
            if primeros['Cuota teórica'].values[-2] == ultimos['Mens. vcto'].values[-2] and primeros['Cuota teórica'].values[-2] == primeros['Mens. vcto'].values[-2]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2]} mensualidades, de {f'{primeros['Cuota teórica'].values[-2]:.2f}'.replace('.', ',')} € al mes. "
            elif primeros['Cuota teórica'].values[-2] != ultimos['Mens. vcto'].values[-2] and primeros['Cuota teórica'].values[-2] == primeros['Mens. vcto'].values[-2]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2]} mensualidades, por importe de {f'{primeros['Cuota teórica'].values[-2]:.2f}'.replace('.', ',')} € al mes, y la última mensualidad de {f'{ultimos['Mens. vcto'].values[-2]:.2f}'.replace('.', ',')} € "
            elif primeros['Cuota teórica'].values[-2] == ultimos['Mens. vcto'].values[-2] and primeros['Cuota teórica'].values[-2] != primeros['Mens. vcto'].values[-2]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2]} mensualidades, por importe de {f'{primeros['Cuota teórica'].values[-2]:.2f}'.replace('.', ',')} € al mes, la primera mensualidad de {f'{primeros['Mens. vcto'].values[-2]:.2f}'.replace('.', ',')} € "
            else:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2]} mensualidades, por importe de {f'{primeros['Cuota teórica'].values[-2]:.2f}'.replace('.', ',')} € al mes, la primera mensualidad de {f'{primeros['Mens. vcto'].values[-2]:.2f}'.replace('.', ',')} € y la última mensualidad de {f'{ultimos['Mens. vcto'].values[-2]:.2f}'.replace('.', ',')} € "
        if cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1] == 1:
            ej_repr_seccion_2 = ej_repr_seccion_2 + f"y {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades con un tipo de interés fijo del {f'{tasa_2sec:.2f}'.replace('.', ',')} % anual, de {f'{primeros['Mens. vcto'].values[-1]:.2f}'.replace('.', ',')} € al mes. "
        else:
            if primeros['Cuota teórica'].values[-1] == ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] == primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = ej_repr_seccion_2 + f"y {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades con un tipo de interés fijo del {f'{tasa_2sec:.2f}'.replace('.', ',')} % anual, de {f'{primeros['Cuota teórica'].values[-1]:.2f}'.replace('.', ',')} € al mes. "
            elif primeros['Cuota teórica'].values[-1] != ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] == primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = ej_repr_seccion_2 + f"y {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades con un tipo de interés fijo del {f'{tasa_2sec:.2f}'.replace('.', ',')} % anual, por importe de {f'{primeros['Cuota teórica'].values[-1]:.2f}'.replace('.', ',')} € al mes, y la última mensualidad de {f'{ultimos['Mens. vcto'].values[-1]:.2f}'.replace('.', ',')} €. "
            elif primeros['Cuota teórica'].values[-1] == ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] != primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = ej_repr_seccion_2 + f"y {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades con un tipo de interés fijo del {f'{tasa_2sec:.2f}'.replace('.', ',')} % anual, por importe de {f'{primeros['Cuota teórica'].values[-1]:.2f}'.replace('.', ',')} € al mes, la primera mensualidad de {f'{primeros['Mens. vcto'].values[-1]:.2f}'.replace('.', ',')} €. "
            else:
                ej_repr_seccion_2 = ej_repr_seccion_2 + f"y {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades con un tipo de interés fijo del {f'{tasa_2sec:.2f}'.replace('.', ',')} % anual, por importe de {f'{primeros['Cuota teórica'].values[-1]:.2f}'.replace('.', ',')} € al mes, la primera mensualidad de {f'{primeros['Mens. vcto'].values[-1]:.2f}'.replace('.', ',')} € y la última mensualidad de {f'{ultimos['Mens. vcto'].values[-1]:.2f}'.replace('.', ',')} €. "
    else:
        if cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1] == 1:
            ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades, de {f'{primeros['Mens. vcto'].values[-1]:.2f}'.replace('.', ',')} € al mes. "
        else:
            if primeros['Cuota teórica'].values[-1] == ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] == primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades, de {f'{primeros['Cuota teórica'].values[-1]:.2f}'.replace('.', ',')} € al mes. "
            elif primeros['Cuota teórica'].values[-1] != ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] == primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades, por importe de {f'{primeros['Cuota teórica'].values[-1]:.2f}'.replace('.', ',')} € al mes, y la última mensualidad de {f'{ultimos['Mens. vcto'].values[-1]:.2f}'.replace('.', ',')} €. "
            elif primeros['Cuota teórica'].values[-1] == ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] != primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades, por importe de {f'{primeros['Cuota teórica'].values[-1]:.2f}'.replace('.', ',')} € al mes, la primera mensualidad de {f'{primeros['Mens. vcto'].values[-1]:.2f}'.replace('.', ',')} €. "
            else:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades, por importe de {f'{primeros['Cuota teórica'].values[-1]:.2f}'.replace('.', ',')} € al mes, la primera mensualidad de {f'{primeros['Mens. vcto'].values[-1]:.2f}'.replace('.', ',')} € y la última mensualidad de {f'{ultimos['Mens. vcto'].values[-1]:.2f}'.replace('.', ',')} €. "
    if carencia >0:
        ej_repr_seccion_2 = f"con un período de carencia de {carencia} meses, " + ej_repr_seccion_2

    if comision_apertura > 0:
        if comision_apertura_capitalizada:
            ej_repr_seccion_3 = f"Comisión de apertura financiada: {f'{comision_apertura:.2f}'.replace('.', ',')} € (del {f'{tasa_comision_apertura:.2f}'.replace('.', ',')} %). Importe total de los intereses: {f'{intereses:.2f}'.replace('.', ',')} €. Coste total del préstamo: {f'{coste_total:.2f}'.replace('.', ',')} €. "
        else:
            ej_repr_seccion_3 = f"Comisión de apertura en la primera mensualidad: {f'{comision_apertura:.2f}'.replace('.', ',')} € (del {f'{tasa_comision_apertura:.2f}'.replace('.', ',')} %). Importe total de los intereses: {f'{intereses:.2f}'.replace('.', ',')} €. Coste total del préstamo: {f'{coste_total:.2f}'.replace('.', ',')} €. "
    else:
        ej_repr_seccion_3 = f"Coste total del préstamo / Importe total de intereses: {f'{coste_total:.2f}'.replace('.', ',')} €. "

    ej_repr_seccion_4 = f"Importe total adeudado/precio total a plazos: {f'{importe_total_a_pagar:.2f}'.replace('.', ',')} €. Sistema de amortización francés."
    
    
    ejemplo_representativo = ej_repr_seccion_1 + ej_repr_seccion_2 + ej_repr_seccion_3 + ej_repr_seccion_4
    
    return (tae,
            comision_apertura,
            importe_total_a_pagar,
            coste_total, intereses,
            coste_seguro, 
            importe_crédito, 
            descuento, 
            tasa, 
            cuota_1sec, 
            cuota_2sec, 
            fecha_fin_carencia_gratuita_forzada, 
            fecha_fin_carencia_diferida, 
            fecha_fin_carencia, 
            fecha_primer_vencimiento, 
            cuadro_amortizacion, 
            input_tae, 
            resumen1, 
            resumen2, 
            resumen3, 
            ejemplo_representativo)

def visualizar_simulacion_unitaria(etiqueta_producto,
                                   fecha_financiacion,
                                   dia_pago,
                                   tasa,
                                   capital_prestado, 
                                   plazo, 
                                   carencia, 
                                   tasa_2sec, 
                                   capital_2sec, 
                                   plazo_2sec, 
                                   seguro_titular_1, 
                                   seguro_titular_2, 
                                   tasa_comision_apertura, 
                                   comision_apertura_capitalizada, 
                                   imp_max_com_apertura):
    ''' Función para simplificar el retorno de la simulación completa que es utilizada para mostrar las simulaciones unitarias '''
    (
        tae,
        comision_apertura,
        importe_total_a_pagar,
        coste_total,
        intereses,
        coste_seguro,
        importe_crédito,
        descuento,
        tasa,
        cuota_1sec,
        cuota_2sec,
        fecha_fin_carencia_gratuita_forzada,
        fecha_fin_carencia_diferida,
        fecha_fin_carencia,
        fecha_primer_vencimiento,
        cuadro_amortizacion,
        input_tae,
        resumen1,
        resumen2,
        resumen3,
        ejemplo_representativo
    ) = simular_prestamo_CLB(
        etiqueta_producto,
        fecha_financiacion,
        dia_pago,
        tasa,
        capital_prestado,
        plazo,
        carencia,
        tasa_2sec,
        capital_2sec,
        plazo_2sec,
        seguro_titular_1,
        seguro_titular_2,
        tasa_comision_apertura,
        comision_apertura_capitalizada,
        imp_max_com_apertura
    )
        
    return resumen1, resumen2, resumen3, ejemplo_representativo, cuadro_amortizacion, input_tae