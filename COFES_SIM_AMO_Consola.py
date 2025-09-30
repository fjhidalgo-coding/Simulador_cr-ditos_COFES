#!
'''Programa para la simulación de los productos amortizables de Cofidis España'''

import math
import pandas as pd 



''' Definir los parámetros básicos para realizar las simulaciones'''

LISTA_SEGURO = ["Seguro ADE", "SIN SEGURO", "VIDA PLUS", "VIDA"]
LISTA_PRODUCTOS = ["CREDITO FUSION","Crédito Proyecto","Compra a plazos","Compra a plazos Vorwerk","Compra financiada","COMPRA FINANCIADA VORWERK","AMORTIZABLE OPTION PH IP","AMORTIZABLE OPTION PH IC","CREDITO FINANCIACION AUTO OCASION","CREDITO FINANCIACION MOTO OCASION","CREDITO FINANCIACION AUTO NUEVO","CREDITO FINANCIACION MOTO NUEVO","CREDITO FINANCIACION AUTO OCASION","CREDITO FINANCIACION MOTO OCASION"]
PRODUCTOS_DICCIONARIO = {
"Nombre del producto": ["CREDITO FUSION", "Crédito Proyecto", "Compra a plazos", "Compra a plazos Vorwerk", "Compra financiada", "COMPRA FINANCIADA VORWERK", "AMORTIZABLE OPTION PH IP", "AMORTIZABLE OPTION PH IC", "CREDITO FINANCIACION AUTO OCASION", "CREDITO FINANCIACION MOTO OCASION", "CREDITO FINANCIACION AUTO NUEVO", "CREDITO FINANCIACION MOTO NUEVO"],
"Código de producto POPS": ["B 2141650000", "B 2150850001", "B 2460050000", "B 2460050001", "B 2460050002", "B 2460050003", "B 2460050004", "B 2460050005", "B 2460050006", "B 2460050007", "B 2460050008", "B 2460050009"],
"Familia de productos": ["Amortizable Rachat Directo ", "Amortizable Directo ", "Amortizable Punto de Venta ", "Amortizable Punto de Venta ", "Amortizable Punto de Venta ", "Amortizable Punto de Venta ", "Amortizable OPTION+ ", "Amortizable OPTION+", "Amortizable AUTO ", "Amortizable AUTO ", "Amortizable AUTO ", "Amortizable AUTO "],
"Interés": ["A cargo del cliente", "A cargo del cliente", "A cargo del cliente", "A cargo del cliente", "A cargo del partner ", "A cargo del partner ", "A cargo del partner ", "A cargo del cliente", "A cargo del cliente", "A cargo del cliente", "A cargo del cliente", "A cargo del cliente"],
"Carencia": ["Hasta 2 meses en función del PROCOM ", "No aplicable ", "Hasta 4 meses en función del baremo y el PROCOM ", "Hasta 4 meses en función del baremo y el PROCOM ", "Hasta 4 meses en función del baremo y el PROCOM ", "Hasta 4 meses en función del baremo y el PROCOM ", "Hasta 4 meses en función del baremo y el PROCOM ", "Hasta 4 meses en función del baremo y el PROCOM ", "No aplicable ", "No aplicable ", "No aplicable ", "No aplicable "],
"Comisión de apertura": ["En función del PROCOM y parametrización TACT. Presentada en el primer vencimiento ", "No aplicable", "En función del baremo y el PROCOM. Capitalizada o presentada en el primer vencimiento en función del PROCOM ", "En función del baremo y el PROCOM. Capitalizada o presentada en el primer vencimiento en función del PROCOM ", "En función del baremo y el PROCOM. Capitalizada o presentada en el primer vencimiento en función del PROCOM ", "En función del baremo y el PROCOM. Capitalizada o presentada en el primer vencimiento en función del PROCOM ", "En función del baremo y el PROCOM. Capitalizada o presentada en el primer vencimiento en función del PROCOM ", "En función del baremo y el PROCOM. Capitalizada o presentada en el primer vencimiento en función del PROCOM ", "En función del baremo y el PROCOM. Capitalizada ", "En función del baremo y el PROCOM. Capitalizada ", "En función del baremo y el PROCOM. Capitalizada ", "En función del baremo y el PROCOM. Capitalizada "],
"Secuencia financiera": ["Única ", "Única ", "Única ", "Única ", "Única ", "Única ", "Doble ", "Doble ", "Única ", "Única ", "Única ", "Única "],
"Producto de seguro asociado": ["ADE", "ADE", "No asegurable ", "No asegurable ", "No asegurable ", "No asegurable ", "No asegurable ", "No asegurable ", "Vida y Vida+. Prima única capitalizada ", "Vida y Vida+. Prima única capitalizada ", "Vida y Vida+. Prima única capitalizada ", "Vida y Vida+. Prima única capitalizada "],
"Mínimo entre fecha de financiación y el primer vencimiento": ["Debe transcurrir un mínimo de 14 días", "Debe transcurrir un mínimo de 14 días", "Debe haber una fecha de bloqueo", "Debe haber una fecha de bloqueo", "Debe haber una fecha de bloqueo", "Debe haber una fecha de bloqueo", "Debe haber una fecha de bloqueo", "Debe haber una fecha de bloqueo", "Debe haber una fecha de bloqueo", "Debe haber una fecha de bloqueo", "Debe haber una fecha de bloqueo", "Debe haber una fecha de bloqueo"],
}
DIAS_BASE = 360

capital_prestado = 0.00
comision_apertura = 0.00
tasa_comision_apertura = 0.00
imp_max_com_apertura = 0.00
comision_apertura_capitalizada = False
etiqueta_producto = ""
fechas_bloqueo = pd.read_csv('COFES_Date_Blocage.csv', sep=';', parse_dates=['Fecha_BLOQUEO'], dayfirst=True).sort_values(by='Fecha_BLOQUEO')
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

        

def truncar_decimal(valor, decimales):
    '''Función para truncar un número decimal a un número específico de decimales sin redondear'''
    factor = 10 ** decimales
    return int(valor * factor) / factor



''' Crear las funciones necesarias para la simulación '''

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

def calcular_mensualidad_estandar(importe_crédito, tasa_global, plazo, carencia, tasa_2SEC, capital_2SEC, plazo_2SEC):
    '''Función para calcular la mensualidad estándar de los productos amortizables de Cofidis España'''
    
    '''Incremantar el capital de la operación con el interés y seguro capitalizado al finalizar carencia'''
    if carencia > 0:
        importe_crédito += round((importe_crédito * tasa_global / 1200),2) * carencia
    
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
    if LISTA_PRODUCTOS.index(etiqueta_producto) < 2 and carencia == 0 and (fecha_primer_vencimiento - fecha_financiacion).days  < 14:
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
    '''Función para calcular el descuento partner de los productos amortizables de Cofidis España'''
    
    if tasa != 0.00:
        # En este cálculo, asumimos que la capitalización de la comisión de apertura debe ser abonada por el partner
        # Existe un descuadre con simulador excel si el tipo de interés no es entero -- A revisar en cuanto sea posible ¿corrige el error que tenía el excel?
        duracion_total = plazo + plazo_2SEC
        capital_mensual = truncar_decimal(importe_crédito / duracion_total, 10)
        tasa_mensual = 1 + truncar_decimal(tasa / 1200, 10)
        tasa_descuento = 1 - truncar_decimal(tasa_mensual ** -duracion_total, 10)
        ajuste_carencia = truncar_decimal(tasa_mensual ** -carencia, 10)
        capital_mensual_ajustado = truncar_decimal(capital_mensual * tasa_descuento, 10) * 1200
        capital_ajustado = truncar_decimal(capital_mensual_ajustado / tasa * ajuste_carencia, 10)
        
        descuento = round(importe_crédito - capital_ajustado, 2)
    else:
        descuento = 0.00

    return descuento

def alimentar_cuadro_amortizacion(w_Tipo_vencimiento, w_Numero_Vencimiento, w_Fecha_Vencimiento, w_Capital_inicial, w_Mensualidad_vencimiento, w_Intereses_vencimiento, w_Intereses_diferidos_vencimiento, w_Intereses_capitalizados_vencimiento, w_Seguro_vencimiento, w_Seguro_diferidos_vencimiento, w_Seguro_capitalizados_vencimiento, w_Comisiones_vencimiento, w_Capital_financiado_periodo, w_Capital_vencimiento, w_Capital_Pendiente, w_Cuota_TAE):
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

def calcular_periodo_roto(base_calculo, fecha_inicio, fecha_fin, tasa_a_aplicar):
    '''Calcular el interés o el seguro cuando el día de inicio de periodo no coincide con el día de fin de periodo'''
    importe_calculo_periodo_roto = round(base_calculo * tasa_a_aplicar / 100 * (pd.to_datetime(fecha_fin) - pd.to_datetime(fecha_inicio)).days / DIAS_BASE, 2)
    return importe_calculo_periodo_roto

def calcular_periodo(base_calculo, fecha_inicio, fecha_fin, tasa_a_aplicar):
    '''Calcular el interés o el seguro cuando el periodo está completo'''
    importe_calculo_periodo = round(base_calculo * tasa_a_aplicar / 1200, 2) * ((fecha_fin.year - fecha_inicio.year) * 12 + (fecha_fin.month - fecha_inicio.month))
    return importe_calculo_periodo

def simular_prestamo_CLB(etiqueta_producto, fecha_financiacion, dia_pago, tasa, capital_prestado, plazo, carencia, tasa_2SEC, capital_2SEC, plazo_2SEC, seguro_titular_1, seguro_titular_2, tasa_comision_apertura, comision_apertura_capitalizada, imp_max_com_apertura):
    '''Función principal para la simulación de los productos amortizables de Cofidis España'''
    
    '''Calcular la comisión de apertura'''
    comision_apertura, capitalizacion_comision_apertura = calcular_comision_apertura(capital_prestado, tasa_comision_apertura, imp_max_com_apertura, comision_apertura_capitalizada)
    
    '''Calcular variable con la capitalización de la comisión de apertura'''
    capital_com_apertura = capital_prestado + capitalizacion_comision_apertura
    
    '''Calcular el seguro de vida capitalizado'''
    seguro_capitalizado = calcular_seguro_capitalizado(capital_com_apertura, plazo, seguro_titular_1, seguro_titular_2)
    
    '''Calcular el importe del crédito incluyendo capital, comisión de apertura capitalizada y seguro capitalizado'''
    importe_crédito = capital_com_apertura + seguro_capitalizado
    
    '''Calcular el descuento y modificar la tasa de interés de los productos con interés partner'''
    descuento = descuento_partner(importe_crédito, tasa, carencia, plazo, plazo_2SEC)
    if 3 < LISTA_PRODUCTOS.index(etiqueta_producto) < 7:
        tasa = 0.00
    
    '''Calcular la tasa del seguro ADE'''
    tasa_ADE = obtener_tasa_seguro_ADE(seguro_titular_1, seguro_titular_2)
    
    '''Calcular la tasa a utilizar para el cálculo de la mensualidad (incluye el seguro ADE; de la primera secuencia para los productos con 2 secuencias)'''
    tasa_global = tasa + tasa_ADE
    
    '''Calcular las mensualidades contractuales de todas las secuencias del contrato'''
    cuota_1SEC, cuota_2SEC = calcular_mensualidad_estandar(importe_crédito, tasa_global, plazo, carencia, tasa_2SEC, capital_2SEC, plazo_2SEC)
    
    '''Calcular las fechas que nos permiten generar el cuadro de amortización'''
    fecha_fin_carencia_gratuita_forzada, fecha_fin_carencia_diferida, fecha_fin_carencia, fecha_primer_vencimiento = calculo_fechas(etiqueta_producto, fecha_financiacion, dia_pago, carencia)
    
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
                                  -capital_prestado)
    '''Generar el vencimiento de carencia gratuita forzada'''
    if fecha_fin_carencia_gratuita_forzada is not None and pd.notnull(fecha_fin_carencia_gratuita_forzada):        
        w_Fecha_ultimo_vencimiento_tratado = fecha_fin_carencia_gratuita_forzada
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
                                      0.00)
    '''Generar el vencimiento de carencia diferida'''
    if fecha_fin_carencia_diferida is not None and pd.notnull(fecha_fin_carencia_diferida):        
        w_Intereses_diferidos_vencimiento = calcular_periodo_roto(w_Capital_Pendiente, w_Fecha_ultimo_vencimiento_tratado, fecha_fin_carencia_diferida, tasa)
        w_Seguro_diferidos_vencimiento = calcular_periodo_roto(w_Capital_Pendiente, w_Fecha_ultimo_vencimiento_tratado, fecha_fin_carencia_diferida, tasa_ADE)
        w_Fecha_ultimo_vencimiento_tratado = fecha_fin_carencia_diferida
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
                                      0.00)
    '''Generar el vencimiento de carencia normal'''
    if fecha_fin_carencia is not None and pd.notnull(fecha_fin_carencia):        
        w_Capital_inicial = w_Capital_Pendiente
        w_Intereses_capitalizados_vencimiento = calcular_periodo(w_Capital_Pendiente, w_Fecha_ultimo_vencimiento_tratado, fecha_fin_carencia, tasa)
        w_Seguro_capitalizados_vencimiento = calcular_periodo(w_Capital_Pendiente, w_Fecha_ultimo_vencimiento_tratado, fecha_fin_carencia, tasa_ADE)
        w_Capital_Pendiente = w_Capital_inicial + w_Intereses_capitalizados_vencimiento + w_Seguro_capitalizados_vencimiento
        w_Fecha_ultimo_vencimiento_tratado = fecha_fin_carencia
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
                                      0.00)
    '''Primer vencimiento de amortización'''
    w_numero_vencimiento = 1
    w_Capital_inicial = w_Capital_Pendiente
    if pd.to_datetime(w_Fecha_ultimo_vencimiento_tratado).day == pd.to_datetime(fecha_primer_vencimiento).day:
        w_Intereses_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa) + w_Intereses_diferidos_vencimiento
        w_Seguro_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa_ADE) + w_Seguro_diferidos_vencimiento
        # Hay un error en el ajuste de la primera mensualidad cuando tiene carencia
        w_ajustes = w_Intereses_diferidos_vencimiento + w_Seguro_diferidos_vencimiento
    else:
        w_Intereses_vencimiento = calcular_periodo_roto(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa) + w_Intereses_diferidos_vencimiento
        w_Seguro_vencimiento = calcular_periodo_roto(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, fecha_primer_vencimiento, tasa_ADE) + w_Seguro_diferidos_vencimiento
        w_ajustes = w_Intereses_vencimiento + w_Seguro_vencimiento - calcular_periodo(w_Capital_inicial, fecha_primer_vencimiento + pd.DateOffset(months=-1), fecha_primer_vencimiento, tasa) - calcular_periodo(w_Capital_inicial, fecha_primer_vencimiento + pd.DateOffset(months=-1), fecha_primer_vencimiento, tasa_ADE)
    w_comision_apertura = comision_apertura - capitalizacion_comision_apertura
    w_Mensualidad_vencimiento = cuota_1SEC + w_comision_apertura + w_ajustes
    w_Capital_vencimiento = w_Mensualidad_vencimiento - w_Intereses_vencimiento - w_Seguro_vencimiento - w_comision_apertura
    w_Capital_Pendiente = w_Capital_inicial - w_Capital_vencimiento
    w_Fecha_ultimo_vencimiento_tratado = fecha_primer_vencimiento
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
                                  0.00)
    '''Resto de vencimientos de la primera secuencia'''
    for i in range(2, plazo + 1):
        w_numero_vencimiento += 1
        w_Capital_inicial = w_Capital_Pendiente
        w_Fecha_vencimiento_calculado = w_Fecha_ultimo_vencimiento_tratado + pd.DateOffset(months=1)
        w_Intereses_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa)
        w_Seguro_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa_ADE)
        if cuota_1SEC < w_Capital_inicial + w_Intereses_vencimiento + w_Seguro_vencimiento - capital_2SEC:
            w_Mensualidad_vencimiento = cuota_1SEC
        else:
            w_Mensualidad_vencimiento = w_Capital_inicial + w_Intereses_vencimiento + w_Seguro_vencimiento - capital_2SEC
        w_Capital_vencimiento = w_Mensualidad_vencimiento - w_Intereses_vencimiento - w_Seguro_vencimiento
        w_Capital_Pendiente = w_Capital_inicial - w_Capital_vencimiento
        w_Fecha_ultimo_vencimiento_tratado = w_Fecha_vencimiento_calculado
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
                                      0.00)
    '''Generar los vencimientos de la segunda secuencia en caso de que exista'''
    if plazo_2SEC > 0:
        for i in range(1, plazo_2SEC + 1):
            w_numero_vencimiento += 1
            w_Capital_inicial = w_Capital_Pendiente
            w_Fecha_vencimiento_calculado = w_Fecha_ultimo_vencimiento_tratado + pd.DateOffset(months=1)
            w_Intereses_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa_2SEC)
            w_Seguro_vencimiento = calcular_periodo(w_Capital_inicial, w_Fecha_ultimo_vencimiento_tratado, w_Fecha_vencimiento_calculado, tasa_ADE)
            if cuota_2SEC < w_Capital_inicial + w_Intereses_vencimiento + w_Seguro_vencimiento:
                w_Mensualidad_vencimiento = cuota_2SEC
            else:
                w_Mensualidad_vencimiento = w_Capital_inicial + w_Intereses_vencimiento + w_Seguro_vencimiento
            w_Capital_vencimiento = w_Mensualidad_vencimiento - w_Intereses_vencimiento - w_Seguro_vencimiento
            w_Capital_Pendiente = w_Capital_inicial - w_Capital_vencimiento
            w_Fecha_ultimo_vencimiento_tratado = w_Fecha_vencimiento_calculado
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
                                          0.00)


           

    
    datos_amortizacion = {
    'Tipo vcto' : Tipo_vencimiento,
    'Nº Vcto' : Numero_Vencimiento,
    'F_Vcto' : Fecha_Vencimiento,
    'Int. DIFF vcto' : Intereses_diferidos_vencimiento,
    'ASS DIFF vcto' : Seguro_diferidos_vencimiento,
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
}
    datos_TAE = {
    'Fecha_Vencimiento' : Fecha_Vencimiento,
    'Cuota_TAE' : Cuota_TAE
}
    '''Crear el dataframe con el cuadro de amortización a mostrar'''
    cuadro_amortizacion = pd.DataFrame(datos_amortizacion)
    
    
    
    
    
    coste_seguro = seguro_capitalizado + sum(Seguro_vencimiento)
    
    return comision_apertura, coste_seguro, importe_crédito, descuento, tasa, cuota_1SEC, cuota_2SEC, fecha_fin_carencia_gratuita_forzada, fecha_fin_carencia_diferida, fecha_fin_carencia, fecha_primer_vencimiento, cuadro_amortizacion



#  def cuota_fija(tasa,importe_a_financiar, plazo, cuota_inicial):
#      '''
#      La función cuota_fija permite generar la simulación de un cuadro de amortización a partir de las variables de entrada:
#      tasa                : Contiene el tipo de interés solicitado al usuario
#      importe_a_financiar : Contiene el capital inicial del préstamos solicitado al cliente
#      plazo               : Contiene la duración inicial del crédito 
#      cuota_inicial       : Contiene la mensualidad al inicio de la simulación
#      '''
#      
#      base_liquidador=pd.DataFrame([])
#      cuota=npf.pmt(tasa, plazo,-importe_a_financiar, 0)
#      cuotas_iniciales=int(input("Ingrese el valor: "))
#      if cuotas_iniciales==1:
#          base_liquidador=pd.DataFrame([])
#          base_liquidador['Mes_cuota']=["Mes_%s"%(i+1) for i in range(plazo+1)]
#          base_liquidador['Saldo']=0
#          base_liquidador['Intereses']=0
#          base_liquidador['Saldo'][0]=importe_a_financiar
#          base_liquidador['Saldo'][1]=importe_a_financiar-cuota_inicial 
#          
#          base_liquidador['pago_mes']=int(cuota)
#          base_liquidador['pago_mes'][0]=cuota_inicial
#          base_liquidador['amortización']=0
#          base_liquidador['amortización'][0]=cuota_inicial
#          base_liquidador['tasa_interes']=tasa
#          base_liquidador['Saldo_final']=0
#  
#          for i in range(0, len(base_liquidador)):
#              base_liquidador['Intereses'][i+1]=(base_liquidador['Saldo'][i]*base_liquidador['tasa_interes'][i])
#              base_liquidador['amortización'][i]=np.where(base_liquidador['Saldo'][i]>base_liquidador['Intereses'][i],(base_liquidador['pago_mes'][i]-base_liquidador['Intereses'][i]),base_liquidador['Saldo'][i] )
#              base_liquidador['Saldo'][i+1]=base_liquidador['Saldo'][i]-base_liquidador['amortización'][i]
#              base_liquidador['pago_mes'][i]=np.where(base_liquidador['Saldo'][i]>base_liquidador['amortización'][i], base_liquidador['pago_mes'][i], base_liquidador['Saldo'][i])
#              base_liquidador['Saldo_final'][i]=base_liquidador['Saldo'][i]-base_liquidador['amortización'][i] 
#  
#      elif cuotas_iniciales==0:
#          base_liquidador=pd.DataFrame([])
#          base_liquidador['Mes_cuota']=["Mes_%s"%(i+1) for i in range(plazo)]
#          base_liquidador['Saldo']=0
#          base_liquidador['Saldo'][0]=importe_a_financiar
#          base_liquidador['Intereses']=0
#          base_liquidador['pago_mes']=int(cuota)
#          base_liquidador['amortización']=0
#          base_liquidador['tasa_interes']=tasa
#          base_liquidador['Saldo_final']=0
#          
#          for i in range(0, len(base_liquidador)):
#              base_liquidador['Intereses'][i]=(base_liquidador['Saldo'][i]*base_liquidador['tasa_interes'][i])
#              base_liquidador['amortización'][i]=np.where(base_liquidador['Saldo'][i]>base_liquidador['Intereses'][i],(base_liquidador['pago_mes'][i]-base_liquidador['Intereses'][i]),base_liquidador['Saldo'][i] )
#              base_liquidador['Saldo'][i+1]=base_liquidador['Saldo'][i]-base_liquidador['amortización'][i]
#              base_liquidador['Saldo_final'][i]=base_liquidador['Saldo'][i]-base_liquidador['amortización'][i]    
#      else: 
#          print("Oops!  Este es un valor incorrecto.  Pruebe de nuevo...")    
#      return base_liquidador
#  
#  
#  # Generación del Cuadro de amortización - TAMO - a partir de la salida de la función cuota_fija 
#  
#  print(df)
#  
#  
#  # Generación del gráfico con la caída de capital e intereses 
#  
#  plt.figure(figsize=(15,8))
#  plt.plot(df.Mes_cuota,df.Saldo,label='Saldo')
#  plt.xlabel('Meses')
#  plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
#  plt.title('Saldo de la deuda')
#  for a,b in zip(df.Mes_cuota,df.Saldo): 
#      plt.text(a, b, str(b))
#  plt.legend()
#  plt.show()

