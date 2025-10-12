#!
'''Programa para la simulación de los productos amortizables de COF_ES'''

import math
import pandas as pd 
import calendar



''' Declarar constantes'''

DIAS_BASE = 360
LISTA_SEGURO = ["Seguro ADE", "SIN SEGURO", "VIDA PLUS", "VIDA"]
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
Tipo_vencimiento = []
Numero_Vencimiento = []
Fecha_Vencimiento = []
Capital_inicial = []
Mensualidad_vencimiento = []
Intereses_vencimiento = []
Intereses_diferidos_vencimiento = []
Intereses_capitalizados_vencimiento = []
Seguro_vencimiento = []
Seguro_diferidos_vencimiento = []
Seguro_capitalizados_vencimiento = []
Comisiones_vencimiento = []
Capital_financiado_periodo = []
Capital_vencimiento = []
Capital_Pendiente = []
Cuota_TAE = []
Año_Base = []
Tiempo = []
van_cuota_TAE = []
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



def obtener_tasa_seguro_ADE(seguro_titular_1, seguro_titular_2):
    if seguro_titular_1 == "Seguro ADE" and seguro_titular_2 == "Seguro ADE":
        tasa_ADE = 7.68
    elif seguro_titular_1 == "Seguro ADE" or seguro_titular_2 == "Seguro ADE":
        tasa_ADE = 4.44
    else:
        tasa_ADE = 0.00
    
    return tasa_ADE



def obtener_tasa_seguro_AUTO(plazo, tipo_seguro):
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
                tasa_vida_plus if tipo_seguro == "VIDA PLUS"
                else tasa_plus if tipo_seguro == "VIDA"
                else tasa_otro
                )
    
    return 0.0



def calcular_seguro_capitalizado(capital_com_apertura, plazo, seguro_titular_1, seguro_titular_2):
    '''Calcular el seguro de vida en base al capital prestado, el tipo de seguro, el número de personas aseguradas y la duración del préstamo'''
    tasa_titular_1 = obtener_tasa_seguro_AUTO(plazo, seguro_titular_1)
    tasa_titular_2 = obtener_tasa_seguro_AUTO(plazo, seguro_titular_2)
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



def descuento_partner(importe_crédito, tasa, carencia, plazo, plazo_2SEC):
    '''Función para calcular el descuento partner de los productos amortizables de COF_ES'''
    if tasa != 0.00:
        # En este cálculo, asumimos que la capitalización de la comisión de apertura debe ser abonada por el partner
        # Existe un descuadre en las operaciones con carencia --> El excel de EI no contenía la manera de calcular con carencia
        duracion_total = plazo + plazo_2SEC
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



def calcular_mensualidad_estandar(importe_crédito, tasa_global, plazo, carencia, tasa_2SEC, capital_2SEC, plazo_2SEC, tasa, tasa_ADE, fecha_financiacion, fecha_fin_carencia_gratuita_forzada, fecha_fin_carencia_diferida, fecha_fin_carencia):
    '''Función para calcular la mensualidad estándar de los productos amortizables de COF_ES'''
    
    '''Incremantar el capital de la operación con el interés y seguro capitalizado al finalizar carencia'''
    if carencia == 1:
        importe_crédito += round((importe_crédito * tasa_global / 1200),2) * carencia
    if carencia > 1:
        w_Fecha_ultimo_vencimiento_tratado = fecha_fin_carencia_gratuita_forzada if fecha_fin_carencia_gratuita_forzada is not None and pd.notnull(fecha_fin_carencia_gratuita_forzada) else fecha_fin_carencia_diferida if fecha_fin_carencia_diferida is not None and pd.notnull(fecha_fin_carencia_diferida) else fecha_financiacion
        importe_crédito += calcular_periodo_roto(importe_crédito, w_Fecha_ultimo_vencimiento_tratado, fecha_fin_carencia, tasa_ADE)
        importe_crédito += round((importe_crédito * tasa / 1200),2) * carencia
        
    '''Calcular la mensualidad contractual del préstamo rendondeando al céntimo superior para asegurar la ventilación de todo el capital'''
    if tasa_global == 0.00:
        cuota_1SEC = math.ceil((importe_crédito - capital_2SEC) / plazo * 100) / 100
    else:
        cuota_1SEC = round(capital_2SEC * tasa_global / 1200, 2) + math.ceil((importe_crédito - capital_2SEC) * tasa_global / 1200 * ((1 + (tasa_global / 1200)) ** plazo) / (((1 + (tasa_global / 1200)) ** plazo) - 1) * 100 ) / 100
    
    '''Calcular la mensualidad de la segunda secuencia en caso de que exista'''
    if capital_2SEC != 0.00:
        if tasa_2SEC == 0.00:
            cuota_2SEC = math.ceil(capital_2SEC / plazo_2SEC * 100) / 100
        else:
            cuota_2SEC = math.ceil(capital_2SEC * tasa_2SEC / 1200 * ((1 + (tasa_2SEC / 1200)) ** plazo_2SEC) / (((1 + (tasa_2SEC / 1200)) ** plazo_2SEC) - 1) * 100 ) / 100
    else:
        cuota_2SEC = 0.00
    
    return cuota_1SEC, cuota_2SEC



def calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion,w_Fecha_ultimo_vencimiento_tratado, w_dia_año):
    '''Función para calcular la fracción del año entre la fecha de financiación y el vencimiento tratado'''
    w_dia_año_anterior = 366 if calendar.isleap(w_Fecha_ultimo_vencimiento_tratado.year - 1) else 365
    w_dia_año_anterior = w_dia_año if pd.to_datetime(w_Fecha_ultimo_vencimiento_tratado).year ==  pd.to_datetime(fecha_financiacion).year else w_dia_año_anterior 
    delta_años = 0 if (w_Fecha_ultimo_vencimiento_tratado.year - fecha_financiacion.year + 1) < 1 else w_Fecha_ultimo_vencimiento_tratado.year - fecha_financiacion.year + 1
    w_aniversario_fecha_financiación = fecha_financiacion + pd.DateOffset(years=delta_años)
    
    if w_dia_año != w_dia_año_anterior and w_Fecha_ultimo_vencimiento_tratado < w_aniversario_fecha_financiación:
        delta_años = delta_años - 1 if delta_años > 1 else 0
        w_aniversario_fecha_financiación += pd.DateOffset(years=-1)
        fraccion_año = delta_años + ((w_dia_año_anterior - pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año_anterior)  + ((pd.to_datetime(w_Fecha_ultimo_vencimiento_tratado).dayofyear) / w_dia_año)
    elif w_Fecha_ultimo_vencimiento_tratado > w_aniversario_fecha_financiación:
        fraccion_año = (0 if delta_años < 1 else delta_años) + ((pd.to_datetime(w_Fecha_ultimo_vencimiento_tratado).dayofyear - pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año)
    else:
        delta_años = delta_años - 1 if delta_años > 1 else 0
        w_aniversario_fecha_financiación += pd.DateOffset(years=-1)
        fraccion_año = delta_años + ((pd.to_datetime(w_Fecha_ultimo_vencimiento_tratado).dayofyear - pd.to_datetime(w_aniversario_fecha_financiación).dayofyear) / w_dia_año)

    return round(fraccion_año, 7)



def calcular_tae(Cuota_TAE, Tiempo, tasa, tolerancia=0.000001, max_iteraciones=1000):
    '''Función para calcular la TAE de la operación'''
    tae = (1 + tasa / 1200) ** 12 - 1  # TAE inicial aproximada
    for _ in range(max_iteraciones):
        van_cuota_TAE.clear()
        for i in range(len(Cuota_TAE)):
            van_cuota_TAE.append(round(Cuota_TAE[i] / ((1 + tae) ** Tiempo[i]),7))
            
        if abs(sum(van_cuota_TAE)) < tolerancia:  # Comprueba si el VAN está dentro de la tolerancia
            return tae
        
        if sum(van_cuota_TAE) < 0:
            tae -= 0.0001
        else:
            tae += 0.0001
        
    return round(tae * 100,2)



def alimentar_cuadro_amortizacion(w_Tipo_vencimiento, w_Numero_Vencimiento, w_Fecha_Vencimiento, w_Capital_inicial, w_Mensualidad_vencimiento, w_Intereses_vencimiento, w_Intereses_diferidos_vencimiento, w_Intereses_capitalizados_vencimiento, w_Seguro_vencimiento, w_Seguro_diferidos_vencimiento, w_Seguro_capitalizados_vencimiento, w_Comisiones_vencimiento, w_Capital_financiado_periodo, w_Capital_vencimiento, w_Capital_Pendiente, w_Cuota_TAE, w_Año_Base, w_Tiempo, w_f_inicio_periodo, w_mensualidad_contractual, w_tasa_periodo):
    '''Función para almacenar la construcción del cuadro de amortización asociado a la instrucción'''
    Tipo_vencimiento.append(w_Tipo_vencimiento)
    Numero_Vencimiento.append(w_Numero_Vencimiento)
    Fecha_Vencimiento.append(w_Fecha_Vencimiento)
    Capital_inicial.append(w_Capital_inicial)
    Mensualidad_vencimiento.append(w_Mensualidad_vencimiento)
    Intereses_vencimiento.append(w_Intereses_vencimiento)
    Intereses_diferidos_vencimiento.append(w_Intereses_diferidos_vencimiento)
    Intereses_capitalizados_vencimiento.append(w_Intereses_capitalizados_vencimiento)
    Seguro_vencimiento.append(w_Seguro_vencimiento)
    Seguro_diferidos_vencimiento.append(w_Seguro_diferidos_vencimiento)
    Seguro_capitalizados_vencimiento.append(w_Seguro_capitalizados_vencimiento)
    Comisiones_vencimiento.append(w_Comisiones_vencimiento)
    Capital_financiado_periodo.append(w_Capital_financiado_periodo)
    Capital_vencimiento.append(w_Capital_vencimiento)
    Capital_Pendiente.append(w_Capital_Pendiente)
    Cuota_TAE.append(w_Cuota_TAE)
    Año_Base.append(w_Año_Base)
    Tiempo.append(w_Tiempo)
    f_inicio_periodo.append(w_f_inicio_periodo)
    mensualidad_contractual.append(w_mensualidad_contractual)
    tasa_periodo.append(w_tasa_periodo)



def simular_prestamo_CLB(etiqueta_producto, fecha_financiacion, dia_pago, tasa, capital_prestado, plazo, carencia, tasa_2SEC, capital_2SEC, plazo_2SEC, seguro_titular_1, seguro_titular_2, tasa_comision_apertura, comision_apertura_capitalizada, imp_max_com_apertura):
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
        descuento = descuento_partner(importe_crédito, tasa, carencia, plazo, plazo_2SEC)
        tasa = 0.00
    else:
        descuento = 0.00
    
    '''Calcular la tasa del seguro ADE'''
    tasa_ADE = obtener_tasa_seguro_ADE(seguro_titular_1, seguro_titular_2)
    
    '''Calcular la tasa a utilizar para el cálculo de la mensualidad (incluye el seguro ADE; de la primera secuencia para los productos con 2 secuencias)'''
    tasa_global = tasa + tasa_ADE
    
    '''Calcular las fechas que nos permiten generar el cuadro de amortización'''
    fecha_fin_carencia_gratuita_forzada, fecha_fin_carencia_diferida, fecha_fin_carencia, fecha_primer_vencimiento = calculo_fechas(etiqueta_producto, fecha_financiacion, dia_pago, carencia)
    
    '''Calcular las mensualidades contractuales de todas las secuencias del contrato'''
    cuota_1SEC, cuota_2SEC = calcular_mensualidad_estandar(importe_crédito, tasa_global, plazo, carencia, tasa_2SEC, capital_2SEC, plazo_2SEC, tasa, tasa_ADE, fecha_financiacion, fecha_fin_carencia_gratuita_forzada, fecha_fin_carencia_diferida, fecha_fin_carencia)
    
    '''Generar el cuadro de amortización de la operación simulada'''
    Tipo_vencimiento.clear()
    Numero_Vencimiento.clear()
    Fecha_Vencimiento.clear()
    Capital_inicial.clear()
    Mensualidad_vencimiento.clear()
    Intereses_vencimiento.clear()
    Intereses_diferidos_vencimiento.clear()
    Intereses_capitalizados_vencimiento.clear()
    Seguro_vencimiento.clear()
    Seguro_diferidos_vencimiento.clear()
    Seguro_capitalizados_vencimiento.clear()
    Comisiones_vencimiento.clear()
    Capital_financiado_periodo.clear()
    Capital_vencimiento.clear()
    Capital_Pendiente.clear()
    Cuota_TAE.clear()
    Año_Base.clear()
    Tiempo.clear()
    van_cuota_TAE.clear()
    f_inicio_periodo.clear()
    mensualidad_contractual.clear()
    tasa_periodo.clear()

    '''Generar el vencimiento de financiación'''
    cuadro_amortizacion = pd.DataFrame()
    if plazo_2SEC > 0:
        w_tipo_vencimiento="Amort. 1ª sec."
    else:
        w_tipo_vencimiento="Amortización"
    w_Fecha_ultimo_vencimiento_tratado = fecha_financiacion
    w_Capital_Pendiente = importe_crédito
    w_Intereses_diferidos_vencimiento = 0.00
    w_Seguro_diferidos_vencimiento = 0.00
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
                                      w_Capital_Pendiente,
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
                                      w_Capital_Pendiente,
                                      0.00,
                                      366 if calendar.isleap(fecha_fin_carencia_gratuita_forzada.year) else 365,
                                      0,
                                      w_Fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                      0.00,
                                      0.00)
        w_Fecha_ultimo_vencimiento_tratado = fecha_fin_carencia_gratuita_forzada

    '''Generar el vencimiento de carencia diferida'''
    if fecha_fin_carencia_diferida is not None and pd.notnull(fecha_fin_carencia_diferida):        
        w_Intereses_diferidos_vencimiento = calcular_periodo_roto(w_Capital_Pendiente, w_Fecha_ultimo_vencimiento_tratado, fecha_fin_carencia_diferida, tasa)
        w_Seguro_diferidos_vencimiento = calcular_periodo_roto(w_Capital_Pendiente, w_Fecha_ultimo_vencimiento_tratado, fecha_fin_carencia_diferida, tasa_ADE)
        alimentar_cuadro_amortizacion("Carencia diferida",
                                      0,
                                      fecha_fin_carencia_diferida,
                                      w_Capital_Pendiente,
                                      0.00,
                                      0.00,
                                      w_Intereses_diferidos_vencimiento,
                                      0.00,
                                      0.00,
                                      w_Seguro_diferidos_vencimiento,
                                      0.00,
                                      0.00,
                                      0.00,
                                      0.00,
                                      w_Capital_Pendiente,
                                      0.00,
                                      366 if calendar.isleap(fecha_fin_carencia_diferida.year) else 365,
                                      0,
                                      w_Fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                      0.00,
                                      tasa)
        w_Fecha_ultimo_vencimiento_tratado = fecha_fin_carencia_diferida

    '''Generar el vencimiento de carencia normal'''
    if fecha_fin_carencia is not None and pd.notnull(fecha_fin_carencia):        
        w_Capital_inicial = w_Capital_Pendiente
        w_Intereses_capitalizados_vencimiento = calcular_periodo(w_Capital_Pendiente, w_Fecha_ultimo_vencimiento_tratado, fecha_fin_carencia, tasa)
        if carencia == 1:
            w_Seguro_capitalizados_vencimiento = calcular_periodo(w_Capital_Pendiente, w_Fecha_ultimo_vencimiento_tratado, fecha_fin_carencia, tasa_ADE)
        else:
            w_Seguro_capitalizados_vencimiento = calcular_periodo_roto(w_Capital_Pendiente, w_Fecha_ultimo_vencimiento_tratado, fecha_fin_carencia, tasa_ADE)
        w_Capital_Pendiente = round(w_Capital_inicial + w_Intereses_capitalizados_vencimiento + w_Seguro_capitalizados_vencimiento, 2)
        alimentar_cuadro_amortizacion("Carencia normal",
                                      0,
                                      fecha_fin_carencia,
                                      w_Capital_inicial,
                                      0.00,
                                      0.00,
                                      0.00,
                                      w_Intereses_capitalizados_vencimiento,
                                      0.00,
                                      0.00,
                                      w_Seguro_capitalizados_vencimiento,
                                      0.00,
                                      0.00,
                                      -w_Intereses_capitalizados_vencimiento - w_Seguro_capitalizados_vencimiento,
                                      w_Capital_Pendiente,
                                      0.00,
                                      366 if calendar.isleap(fecha_fin_carencia.year) else 365,
                                      0,
                                      w_Fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                      0.00,
                                      tasa)
        w_Fecha_ultimo_vencimiento_tratado = fecha_fin_carencia

    '''Primer vencimiento de amortización'''
    w_numero_vencimiento = 1
    w_Capital_inicial = w_Capital_Pendiente
    if pd.to_datetime(w_Fecha_ultimo_vencimiento_tratado).day == pd.to_datetime(fecha_primer_vencimiento).day:
        w_Intereses_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa) + w_Intereses_diferidos_vencimiento
        w_Seguro_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa_ADE) + w_Seguro_diferidos_vencimiento
        w_ajustes = w_Intereses_diferidos_vencimiento + w_Seguro_diferidos_vencimiento
    else:
        w_Intereses_vencimiento = calcular_periodo_roto(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa) + w_Intereses_diferidos_vencimiento
        w_Seguro_vencimiento = calcular_periodo_roto(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa_ADE) + w_Seguro_diferidos_vencimiento
        w_ajustes = w_Intereses_vencimiento + w_Seguro_vencimiento - calcular_periodo(w_Capital_inicial, fecha_primer_vencimiento + pd.DateOffset(months=-1), fecha_primer_vencimiento, tasa) - calcular_periodo(w_Capital_inicial, fecha_primer_vencimiento + pd.DateOffset(months=-1), fecha_primer_vencimiento, tasa_ADE)
    w_comision_apertura = comision_apertura - capitalizacion_comision_apertura
    w_Mensualidad_vencimiento = cuota_1SEC + w_comision_apertura + w_ajustes
    w_Capital_vencimiento = round(w_Mensualidad_vencimiento - w_Intereses_vencimiento - w_Seguro_vencimiento - w_comision_apertura, 2)
    w_Capital_Pendiente = round(w_Capital_inicial - w_Capital_vencimiento, 2)
    w_dia_año = 366 if calendar.isleap(fecha_primer_vencimiento.year) else 365
    alimentar_cuadro_amortizacion(w_tipo_vencimiento,
                                  w_numero_vencimiento,
                                  fecha_primer_vencimiento,
                                  w_Capital_inicial,
                                  w_Mensualidad_vencimiento,
                                  w_Intereses_vencimiento,
                                  0.00,
                                  0.00,
                                  w_Seguro_vencimiento,
                                  0.00,
                                  0.00,
                                  w_comision_apertura,
                                  0.00,
                                  w_Capital_vencimiento,
                                  w_Capital_Pendiente,
                                  w_Intereses_vencimiento + w_Capital_vencimiento + comision_apertura,  # Forzamos la cuota TAE para que incluya la comisión de apertura (ver SARA)
                                  w_dia_año,
                                  calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion, fecha_primer_vencimiento,w_dia_año),
                                  w_Fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                  cuota_1SEC,
                                  tasa)
    w_Fecha_ultimo_vencimiento_tratado = fecha_primer_vencimiento

    '''Resto de vencimientos de la primera secuencia'''
    for i in range(2, plazo + 1):
        w_numero_vencimiento += 1
        w_Capital_inicial = w_Capital_Pendiente
        w_Fecha_vencimiento_calculado = w_Fecha_ultimo_vencimiento_tratado + pd.DateOffset(months=1)
        w_Seguro_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa_ADE)
        if w_numero_vencimiento == plazo and cuota_1SEC < calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa) + w_Capital_inicial + w_Seguro_vencimiento - capital_2SEC:
            w_Intereses_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa) - (calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa) + w_Capital_inicial + w_Seguro_vencimiento - capital_2SEC - cuota_1SEC)
        else:
            w_Intereses_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa)
        if cuota_1SEC < w_Capital_inicial + w_Intereses_vencimiento + w_Seguro_vencimiento - capital_2SEC:
            w_Mensualidad_vencimiento = cuota_1SEC
        else:
            w_Mensualidad_vencimiento = w_Capital_inicial + w_Intereses_vencimiento + w_Seguro_vencimiento - capital_2SEC
        w_Capital_vencimiento = round(w_Mensualidad_vencimiento - w_Intereses_vencimiento - w_Seguro_vencimiento, 2)
        w_Capital_Pendiente = round(w_Capital_inicial - w_Capital_vencimiento, 2)
        w_dia_año = 366 if calendar.isleap(fecha_primer_vencimiento.year) else 365
        alimentar_cuadro_amortizacion(w_tipo_vencimiento,
                                      w_numero_vencimiento,
                                      w_Fecha_ultimo_vencimiento_tratado,
                                      w_Capital_inicial,
                                      w_Mensualidad_vencimiento,
                                      w_Intereses_vencimiento,
                                      0.00,
                                      0.00,
                                      w_Seguro_vencimiento,
                                      0.00,
                                      0.00,
                                      0.00,
                                      0.00,
                                      w_Capital_vencimiento,
                                      w_Capital_Pendiente,
                                      w_Intereses_vencimiento + w_Capital_vencimiento,
                                      w_dia_año,
                                      calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion, w_Fecha_ultimo_vencimiento_tratado,w_dia_año),
                                      w_Fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                      cuota_1SEC,
                                      tasa)
        w_Fecha_ultimo_vencimiento_tratado = w_Fecha_vencimiento_calculado

    '''Generar los vencimientos de la segunda secuencia en caso de que exista'''
    if plazo_2SEC > 0:
        for i in range(1, plazo_2SEC + 1):
            w_numero_vencimiento += 1
            w_Capital_inicial = w_Capital_Pendiente
            w_Fecha_vencimiento_calculado = w_Fecha_ultimo_vencimiento_tratado + pd.DateOffset(months=1)
            w_Seguro_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa_ADE)
            if w_numero_vencimiento == plazo_2SEC + plazo and cuota_2SEC < calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa_2SEC) + w_Capital_inicial + w_Seguro_vencimiento:
                w_Intereses_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa_2SEC) - (calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa_2SEC) + w_Capital_inicial + w_Seguro_vencimiento - cuota_2SEC)
            else:
                w_Intereses_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa_2SEC)
            if cuota_2SEC < w_Capital_inicial + w_Intereses_vencimiento + w_Seguro_vencimiento:
                w_Mensualidad_vencimiento = cuota_2SEC
            else:
                w_Mensualidad_vencimiento = w_Capital_inicial + w_Intereses_vencimiento + w_Seguro_vencimiento
            w_Capital_vencimiento = round(w_Mensualidad_vencimiento - w_Intereses_vencimiento - w_Seguro_vencimiento, 2)
            w_Capital_Pendiente = round(w_Capital_inicial - w_Capital_vencimiento, 2)
            w_dia_año = 366 if calendar.isleap(fecha_primer_vencimiento.year) else 365
            alimentar_cuadro_amortizacion("Amort. 2ª sec.",
                                          w_numero_vencimiento,
                                          w_Fecha_ultimo_vencimiento_tratado,
                                          w_Capital_inicial,
                                          w_Mensualidad_vencimiento,
                                          w_Intereses_vencimiento,
                                          0.00,
                                          0.00,
                                          w_Seguro_vencimiento,
                                          0.00,
                                          0.00,
                                          0.00,
                                          0.00,
                                          w_Capital_vencimiento,
                                          w_Capital_Pendiente,
                                          w_Intereses_vencimiento + w_Capital_vencimiento,
                                          w_dia_año,
                                          calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion, w_Fecha_ultimo_vencimiento_tratado,w_dia_año),
                                          w_Fecha_ultimo_vencimiento_tratado + pd.DateOffset(days=1),
                                          cuota_2SEC,
                                          tasa_2SEC)
            w_Fecha_ultimo_vencimiento_tratado = w_Fecha_vencimiento_calculado
    
    ''' Calcular la TAE de la operación con el listado de "Cuota_TAE", la fracción temporal entre la financiación y el vencimiento y el TIN'''
    tae = calcular_tae(Cuota_TAE, Tiempo, tasa)
    
    ''' Crear el diccionario con los datos del cuadro de amortización y de la TAE'''
    datos_amortizacion = {
    'Tipo vcto' : Tipo_vencimiento,
    'Nº Vcto' : Numero_Vencimiento,
    'F_Inicio' : f_inicio_periodo,
    'F_Vcto' : Fecha_Vencimiento,
    'TIN' : tasa_periodo,
    'Int. CAP. vcto' : Intereses_capitalizados_vencimiento,
    'ASS CAP. vcto' : Seguro_capitalizados_vencimiento,
    'Com. vcto' : Comisiones_vencimiento,
    'Cap. finan.' : Capital_financiado_periodo,
    'Cap. inicial' : Capital_inicial,
    'Mens. vcto' : Mensualidad_vencimiento,
    'Int. vcto' : Intereses_vencimiento,
    'ASS vcto' : Seguro_vencimiento,
    'Cap. vcto' : Capital_vencimiento,
    'Cap. PDTE' : Capital_Pendiente,
    'Cuota teórica' : mensualidad_contractual,
    'Int. DIFF vcto' : Intereses_diferidos_vencimiento,
    'ASS DIFF vcto' : Seguro_diferidos_vencimiento,
}
    datos_TAE = {
    'Fecha_Vencimiento' : Fecha_Vencimiento,
    'Cuota_TAE' : Cuota_TAE,
    'Año_Base' : Año_Base,
    'Tiempo': Tiempo,
    'van_cuota_TAE' : van_cuota_TAE
}
    '''Crear el dataframe con el cuadro de amortización a mostrar'''
    cuadro_amortizacion = pd.DataFrame(datos_amortizacion)
    
    '''Crear el dataframe con el cuadro de cálculo TAE a mostrar'''
    input_TAE = pd.DataFrame(datos_TAE)
    
    ''' Crear las variables con los sumatorios del cuadro de amortización'''
    intereses = sum(Intereses_capitalizados_vencimiento) + sum(Intereses_vencimiento)
    coste_seguro = seguro_capitalizado + sum(Seguro_vencimiento) + sum(Seguro_capitalizados_vencimiento)
    coste_total = intereses + comision_apertura # + coste_seguro
    importe_total_a_pagar = sum(Mensualidad_vencimiento)
    
    mostrar_fecha = lambda fecha: fecha.strftime('%d/%m/%Y') if fecha is not None and pd.notnull(fecha) else "No disponible"
        
    cuadro_secuencias = cuadro_amortizacion[cuadro_amortizacion['Tipo vcto'] != "Financiación"]
    
    cuenta_vencimientos = cuadro_secuencias['Tipo vcto'].value_counts()
    primeros = cuadro_secuencias.groupby('Tipo vcto').head(1)
    ultimos = cuadro_secuencias.groupby('Tipo vcto').tail(1)

    resumen1 = pd.DataFrame(
        {
            "TAE": [f"{tae:.2f}"],
        },
    index=["%"],
    )

    resumen2 = pd.DataFrame(
        {
            "Importe total a pagar": [f"{importe_total_a_pagar:.2f}"],
            "Coste total": [f"{coste_total:.2f}"],
            "Intereses": [f"{intereses:.2f}"],
            "Prima de seguro": [f"{coste_seguro:.2f}"],
            "Comisión de apertura": [f"{comision_apertura:.2f}"],
            "Capital": [f"{capital_prestado:.2f}"],
            "Importe del crédito": [f"{importe_crédito:.2f}"],
            "Descuento Partner": [f"{descuento:.2f}"],
        },
    index=["EUR"],
    )

    resumen3 = pd.DataFrame(
    {
        "Nº Vencimientos": cuenta_vencimientos.loc[ultimos['Tipo vcto']].values,
        "TIN": primeros['TIN'].values,
        "F_INI": [mostrar_fecha(fecha) for fecha in primeros['F_Inicio'].values],
        "IMP_Cuota": primeros['Cuota teórica'].values,
        "F_1er_VCTO":  [mostrar_fecha(fecha) for fecha in primeros['F_Vcto'].values],
        "IMP_1era_Cuota": primeros['Mens. vcto'].values,
        "F_FIN":  [mostrar_fecha(fecha) for fecha in ultimos['F_Vcto'].values],
        "IMP_ULT_Cuota": ultimos['Mens. vcto'].values,
    },
    index=ultimos['Tipo vcto'].values,
    )
    
    ejemplo_representativo = "No disponible. En construcción"
    
    if LISTA_PRODUCTOS.index(etiqueta_producto) == 1:
        ejemplo_representativo = f"Para un ejemplo de importe de {importe_crédito} € para “XXXXXXXXXX”, {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values} cuotas mensuales de {primeros['Cuota teórica'].values}€ y una última residual de {ultimos['Mens. vcto'].values} €. El importe total adeudado será de {importe_total_a_pagar} €. Coste total del préstamo/importe de los intereses: {intereses} €. Sistema de amortización francés. TAE: {tae}%. TIN: {tasa}%."
    
    
    return tae, comision_apertura, importe_total_a_pagar, coste_total, intereses, coste_seguro, importe_crédito, descuento, tasa, cuota_1SEC, cuota_2SEC, fecha_fin_carencia_gratuita_forzada, fecha_fin_carencia_diferida, fecha_fin_carencia, fecha_primer_vencimiento, cuadro_amortizacion, input_TAE, resumen1, resumen2, resumen3, ejemplo_representativo

def visualizar_simulacion_unitaria(etiqueta_producto, fecha_financiacion, dia_pago, tasa, capital_prestado, plazo, carencia, tasa_2SEC, capital_2SEC, plazo_2SEC, seguro_titular_1, seguro_titular_2, tasa_comision_apertura, comision_apertura_capitalizada, imp_max_com_apertura):
    ''' Función para simplificar el retorno de la simulación completa que es utilizada para mostrar las simulaciones unitarias '''
    tae, comision_apertura, importe_total_a_pagar, coste_total, intereses, coste_seguro, importe_crédito, descuento, tasa, cuota_1SEC, cuota_2SEC, fecha_fin_carencia_gratuita_forzada, fecha_fin_carencia_diferida, fecha_fin_carencia, fecha_primer_vencimiento, cuadro_amortizacion, input_TAE, resumen1, resumen2, resumen3, ejemplo_representativo = simular_prestamo_CLB(etiqueta_producto,
                                                                                                                                                                                                                                                                                                                                                                               fecha_financiacion,
                                                                                                                                                                                                                                                                                                                                                                               dia_pago,
                                                                                                                                                                                                                                                                                                                                                                               tasa,
                                                                                                                                                                                                                                                                                                                                                                               capital_prestado,
                                                                                                                                                                                                                                                                                                                                                                               plazo,
                                                                                                                                                                                                                                                                                                                                                                               carencia,
                                                                                                                                                                                                                                                                                                                                                                               tasa_2SEC,
                                                                                                                                                                                                                                                                                                                                                                               capital_2SEC,
                                                                                                                                                                                                                                                                                                                                                                               plazo_2SEC,
                                                                                                                                                                                                                                                                                                                                                                               seguro_titular_1,
                                                                                                                                                                                                                                                                                                                                                                               seguro_titular_2,
                                                                                                                                                                                                                                                                                                                                                                               tasa_comision_apertura,
                                                                                                                                                                                                                                                                                                                                                                               comision_apertura_capitalizada,
                                                                                                                                                                                                                                                                                                                                                                               imp_max_com_apertura)
        
    return resumen1, resumen2, resumen3, ejemplo_representativo, cuadro_amortizacion, input_TAE