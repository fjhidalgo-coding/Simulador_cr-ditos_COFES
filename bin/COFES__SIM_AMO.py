#!
'''Programa para la simulación de los productos amortizables'''

import bin.COFES___TAE as tools_tae
import bin.COFES___tools as tools



''' Declarar constantes'''

DIAS_BASE = 360
LISTA_PRODUCTOS = tools.LISTA_PRODUCTOS
LISTA_SEGURO = tools.LISTA_SEGURO
PRODUCTOS_DICCIONARIO = tools.PRODUCTOS_DICCIONARIO


''' Declarar variables globales '''

capital_prestado = tools.redondear_decimal(0.00)
comision_apertura = tools.redondear_decimal(0.00)
tasa_comision_apertura = tools.redondear_decimal(0.00)
imp_max_com_apertura = tools.redondear_decimal(0.00)
comision_apertura_capitalizada = False
etiqueta_producto = ""
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
acumulado_tae = []
acumulado_comision_apertura = []
acumulado_importe_total_a_pagar = []
acumulado_coste_total = []
acumulado_intereses = []
acumulado_coste_seguro = []
acumulado_importe_crédito = []
acumulado_descuento = []
acumulado_tasa = []
acumulado_cuota_1sec = []
acumulado_cuota_2sec = []
acumulado_fecha_fin_carencia_gratuita_forzada = []
acumulado_fecha_fin_carencia_diferida = []
acumulado_fecha_fin_carencia = []
acumulado_fecha_primer_vencimiento = []
acumulado_ejemplo_representativo = []
acumulado_capital_2sec = []
acumulado_carencia = []
acumulado_comision_apertura_capitalizada = []
acumulado_dia_pago = []
acumulado_etiqueta_producto = []
acumulado_fecha_financiacion = []
acumulado_imp_max_com_apertura = []
acumulado_capital_prestado = []
acumulado_on = []
acumulado_plazo_2sec = []
acumulado_plazos = []
acumulado_seguro_titular_1 = []
acumulado_seguro_titular_2 = []
acumulado_tasa_2sec = []
acumulado_tasa_comision_apertura = []



''' Crear las funciones necesarias para la simulación amortizable'''

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
    
    '''Forzar formato Decimal para los cálculos y evitar problemas de precisión con los floats'''
    capital_prestado = tools.redondear_decimal(capital_prestado)
    tasa = tools.redondear_decimal(tasa)
    capital_2sec = tools.redondear_decimal(capital_2sec)
    tasa_2sec = tools.redondear_decimal(tasa_2sec)
    tasa_comision_apertura = tools.redondear_decimal(tasa_comision_apertura)
    imp_max_com_apertura = tools.redondear_decimal(imp_max_com_apertura)

    '''Control sobre el capital'''
    if capital_prestado <= 0.00 or capital_2sec >= capital_prestado:
        return (tools.redondear_decimal(0.00),
                tools.redondear_decimal(0.00),
                tools.redondear_decimal(0.00),
                tools.redondear_decimal(0.00),
                tools.redondear_decimal(0.00),
                tools.redondear_decimal(0.00),
                tools.redondear_decimal(0.00),
                tools.redondear_decimal(0.00),
                tools.redondear_decimal(0.00),
                tools.redondear_decimal(0.00), 
                tools.redondear_decimal(0.00), 
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                "El capital de las secuencias financieras es incoherente.")

    '''Calcular la comisión de apertura'''
    comision_apertura, capitalizacion_comision_apertura = tools.calcular_comision_apertura(capital_prestado,
                                                                                           tasa_comision_apertura,
                                                                                           imp_max_com_apertura,
                                                                                           comision_apertura_capitalizada)
    
    '''Calcular capital capitalizando la comisión de apertura'''
    capital_com_apertura = tools.redondear_decimal(capital_prestado + capitalizacion_comision_apertura)
    
    '''Calcular el seguro de vida capitalizado'''
    seguro_capitalizado = tools.calcular_seguro_capitalizado(capital_com_apertura,
                                                             plazo,
                                                             seguro_titular_1,
                                                             seguro_titular_2)

    '''Calcular el importe del crédito incluyendo capital, comisión de apertura capitalizada y seguro capitalizado'''
    importe_crédito = tools.redondear_decimal(capital_com_apertura + seguro_capitalizado)
    
    '''Calcular el descuento y modificar la tasa de interés de los productos con interés partner'''
    if LISTA_PRODUCTOS.index(etiqueta_producto) in (4, 5, 6):
        descuento = tools.calcular_descuento_partner(importe_crédito,
                                                     tasa,
                                                     carencia,
                                                     plazo,
                                                     plazo_2sec)
        tasa = tools.redondear_decimal(0.00)
    else:
        descuento = tools.redondear_decimal(0.00)
    
    '''Calcular la tasa del seguro ADE'''
    tasa_ade = tools.obtener_tasa_seguro_ade(seguro_titular_1,
                                             seguro_titular_2)
    
    '''Calcular la tasa a utilizar para el cálculo de la mensualidad (incluye el seguro ADE; de la primera secuencia para los productos con 2 secuencias)'''
    tasa_global = tasa + tasa_ade
    
    '''Calcular las fechas que nos permiten generar el cuadro de amortización'''
    (fecha_fin_carencia_gratuita_forzada,
     fecha_fin_carencia_diferida,
     fecha_fin_carencia,
     fecha_primer_vencimiento) = tools.calcular_fechas(etiqueta_producto,
                                                       fecha_financiacion,
                                                       dia_pago,
                                                       carencia)
    
    '''Calcular las mensualidades contractuales de todas las secuencias del contrato'''
    cuota_1sec, cuota_2sec = tools.calcular_mensualidad_estandar(importe_crédito,
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
                                                                 DIAS_BASE)
    
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
    cuadro_amortizacion = tools.pd.DataFrame()
    if plazo_2sec > 0:
        w_tipo_vencimiento="Amort. 1ª sec."
    else:
        w_tipo_vencimiento="Amortización"
    w_fecha_ultimo_vencimiento_tratado = fecha_financiacion
    w_capital_pendiente = importe_crédito
    w_intereses_diferidos_vencimiento = tools.redondear_decimal(0.00)
    w_seguro_diferidos_vencimiento = tools.redondear_decimal(0.00)
    alimentar_cuadro_amortizacion("Financiación",
                                  0,
                                  tools.mostrar_fecha(fecha_financiacion),
                                  tools.redondear_decimal(0.00),
                                  tools.redondear_decimal(0.00),
                                  tools.redondear_decimal(0.00),
                                  tools.redondear_decimal(0.00),
                                  tools.redondear_decimal(0.00),
                                  tools.redondear_decimal(0.00),
                                  tools.redondear_decimal(0.00),
                                  seguro_capitalizado,
                                  capitalizacion_comision_apertura,
                                  capital_prestado,
                                  -importe_crédito,
                                  importe_crédito,
                                  tools.redondear_decimal(-capital_prestado - seguro_capitalizado),
                                  tools.dias_año(fecha_financiacion),
                                  0,
                                  tools.mostrar_fecha(fecha_financiacion),
                                  tools.redondear_decimal(0.00),
                                  tools.redondear_decimal(0.00))

    '''Generar el vencimiento de carencia gratuita forzada'''
    if fecha_fin_carencia_gratuita_forzada is not None and tools.pd.notnull(fecha_fin_carencia_gratuita_forzada):        
        alimentar_cuadro_amortizacion("Carencia gratuita forzada",
                                      0,
                                      tools.mostrar_fecha(fecha_fin_carencia_gratuita_forzada),
                                      w_capital_pendiente,
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      w_capital_pendiente,
                                      tools.redondear_decimal(0.00),
                                      tools.dias_año(fecha_fin_carencia_gratuita_forzada),
                                      0,
                                      tools.mostrar_fecha(w_fecha_ultimo_vencimiento_tratado + tools.pd.DateOffset(days=1)),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00))
        w_fecha_ultimo_vencimiento_tratado = fecha_fin_carencia_gratuita_forzada

    '''Generar el vencimiento de carencia diferida'''
    if fecha_fin_carencia_diferida is not None and tools.pd.notnull(fecha_fin_carencia_diferida):        
        if LISTA_PRODUCTOS.index(etiqueta_producto) in (3, 5):
            w_intereses_diferidos_vencimiento = tools.redondear_decimal(0.00)
        else:
            w_intereses_diferidos_vencimiento = tools.calcular_periodo_roto(w_capital_pendiente,
                                                                            w_fecha_ultimo_vencimiento_tratado,
                                                                            fecha_fin_carencia_diferida, tasa, DIAS_BASE)
        w_seguro_diferidos_vencimiento = tools.calcular_periodo_roto(w_capital_pendiente,
                                                                     w_fecha_ultimo_vencimiento_tratado,
                                                                     fecha_fin_carencia_diferida,
                                                                     tasa_ade, DIAS_BASE)
        alimentar_cuadro_amortizacion("Carencia diferida",
                                      0,
                                      tools.mostrar_fecha(fecha_fin_carencia_diferida),
                                      w_capital_pendiente,
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      w_intereses_diferidos_vencimiento,
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      w_seguro_diferidos_vencimiento,
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      w_capital_pendiente,
                                      tools.redondear_decimal(0.00),
                                      tools.dias_año(fecha_fin_carencia_diferida),
                                      tools.redondear_decimal(0.00),
                                      tools.mostrar_fecha(w_fecha_ultimo_vencimiento_tratado + tools.pd.DateOffset(days=1)),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00) if LISTA_PRODUCTOS.index(etiqueta_producto) in (3, 5) else tasa)
        w_fecha_ultimo_vencimiento_tratado = fecha_fin_carencia_diferida

    '''Generar el vencimiento de carencia normal'''
    if fecha_fin_carencia is not None and tools.pd.notnull(fecha_fin_carencia):        
        w_capital_inicial = w_capital_pendiente
        w_intereses_capitalizados_vencimiento = tools.calcular_periodo(w_capital_pendiente,
                                                                       w_fecha_ultimo_vencimiento_tratado,
                                                                       fecha_fin_carencia,
                                                                       tasa)
        if carencia == 1:
          w_seguro_capitalizados_vencimiento = tools.calcular_periodo(w_capital_pendiente,
                                                                      w_fecha_ultimo_vencimiento_tratado,
                                                                      fecha_fin_carencia,
                                                                      tasa_ade)
        else:
          w_seguro_capitalizados_vencimiento = tools.calcular_periodo_roto(w_capital_pendiente,
                                                                           w_fecha_ultimo_vencimiento_tratado,
                                                                           fecha_fin_carencia,
                                                                           tasa_ade,
                                                                           DIAS_BASE)
        w_capital_pendiente = tools.redondear_decimal(w_capital_inicial + w_intereses_capitalizados_vencimiento + w_seguro_capitalizados_vencimiento)
        alimentar_cuadro_amortizacion("Carencia normal",
                                      0,
                                      tools.mostrar_fecha(fecha_fin_carencia),
                                      w_capital_inicial,
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      w_intereses_capitalizados_vencimiento,
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      w_seguro_capitalizados_vencimiento,
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(-w_intereses_capitalizados_vencimiento - w_seguro_capitalizados_vencimiento),
                                      w_capital_pendiente,
                                      tools.redondear_decimal(0.00),
                                      tools.dias_año(fecha_fin_carencia),
                                      0,
                                      tools.mostrar_fecha(w_fecha_ultimo_vencimiento_tratado + tools.pd.DateOffset(days=1)),
                                      tools.redondear_decimal(0.00),
                                      tasa)
        w_fecha_ultimo_vencimiento_tratado = fecha_fin_carencia

    '''Primer vencimiento de amortización'''
    w_numero_vencimiento = 1
    w_capital_inicial = w_capital_pendiente
    if tools.pd.to_datetime(w_fecha_ultimo_vencimiento_tratado).day == tools.pd.to_datetime(fecha_primer_vencimiento).day:
        w_intereses_vencimiento = w_intereses_diferidos_vencimiento + tools.calcular_periodo(w_capital_inicial,
                                                                                             w_fecha_ultimo_vencimiento_tratado,
                                                                                             fecha_primer_vencimiento,
                                                                                             tasa)
        w_seguro_vencimiento = w_seguro_diferidos_vencimiento + tools.calcular_periodo(w_capital_inicial,
                                                                                       w_fecha_ultimo_vencimiento_tratado,
                                                                                       fecha_primer_vencimiento,
                                                                                       tasa_ade)
        w_ajustes = w_intereses_diferidos_vencimiento + w_seguro_diferidos_vencimiento
    else:
        w_intereses_vencimiento = w_intereses_diferidos_vencimiento + tools.calcular_periodo_roto(w_capital_inicial,
                                                                                                  w_fecha_ultimo_vencimiento_tratado,
                                                                                                  fecha_primer_vencimiento,
                                                                                                  tasa,
                                                                                                  DIAS_BASE)
        w_seguro_vencimiento = w_seguro_diferidos_vencimiento + tools.calcular_periodo_roto(w_capital_inicial,
                                                                                            w_fecha_ultimo_vencimiento_tratado,
                                                                                            fecha_primer_vencimiento,
                                                                                            tasa_ade,
                                                                                            DIAS_BASE)
        w_ajustes = (w_intereses_vencimiento
                     + w_seguro_vencimiento 
                     - tools.calcular_periodo(w_capital_inicial,
                                              fecha_primer_vencimiento + tools.pd.DateOffset(months=-1),
                                              fecha_primer_vencimiento,
                                              tasa) 
                     - tools.calcular_periodo(w_capital_inicial,
                                              fecha_primer_vencimiento + tools.pd.DateOffset(months=-1),
                                              fecha_primer_vencimiento,
                                              tasa_ade))
    w_comision_apertura = comision_apertura - capitalizacion_comision_apertura
    w_mensualidad_vencimiento = cuota_1sec + w_comision_apertura + w_ajustes
    w_capital_vencimiento = w_mensualidad_vencimiento - w_intereses_vencimiento - w_seguro_vencimiento - w_comision_apertura
    w_capital_pendiente = w_capital_inicial - w_capital_vencimiento
    w_dia_año = tools.dias_año(fecha_primer_vencimiento)
    alimentar_cuadro_amortizacion(w_tipo_vencimiento,
                                  w_numero_vencimiento,
                                  tools.mostrar_fecha(fecha_primer_vencimiento),
                                  w_capital_inicial,
                                  w_mensualidad_vencimiento,
                                  w_intereses_vencimiento,
                                  tools.redondear_decimal(0.00),
                                  tools.redondear_decimal(0.00),
                                  w_seguro_vencimiento,
                                  tools.redondear_decimal(0.00),
                                  tools.redondear_decimal(0.00),
                                  w_comision_apertura,
                                  tools.redondear_decimal(0.00),
                                  w_capital_vencimiento,
                                  w_capital_pendiente,
                                  w_intereses_vencimiento + w_capital_vencimiento + w_comision_apertura,
                                  w_dia_año,
                                  tools_tae.calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion, fecha_primer_vencimiento,w_dia_año),
                                  tools.mostrar_fecha(w_fecha_ultimo_vencimiento_tratado + tools.pd.DateOffset(days=1)),
                                  cuota_1sec,
                                  tasa)
    w_fecha_ultimo_vencimiento_tratado = fecha_primer_vencimiento

    '''Resto de vencimientos de la primera secuencia'''
    for i in range(2, plazo + 1):
        w_numero_vencimiento += 1
        w_capital_inicial = w_capital_pendiente
        w_fecha_vencimiento_calculado = w_fecha_ultimo_vencimiento_tratado + tools.pd.DateOffset(months=1)
        w_seguro_vencimiento = tools.calcular_periodo(w_capital_inicial,
                                                      w_fecha_ultimo_vencimiento_tratado,
                                                      w_fecha_vencimiento_calculado,
                                                      tasa_ade)
        if (w_numero_vencimiento == plazo 
            and cuota_1sec < w_capital_inicial + w_seguro_vencimiento - capital_2sec + tools.calcular_periodo(w_capital_inicial,
                                                                                                              w_fecha_ultimo_vencimiento_tratado,
                                                                                                              w_fecha_vencimiento_calculado,
                                                                                                              tasa)):
            w_intereses_vencimiento = (tools.calcular_periodo(w_capital_inicial,
                                                              w_fecha_ultimo_vencimiento_tratado,
                                                              w_fecha_vencimiento_calculado,
                                                              tasa) 
                                      - (tools.calcular_periodo(w_capital_inicial,
                                                                w_fecha_ultimo_vencimiento_tratado,
                                                                w_fecha_vencimiento_calculado,
                                                                tasa) 
                                      + w_capital_inicial + w_seguro_vencimiento - capital_2sec - cuota_1sec))
        else:
            w_intereses_vencimiento = tools.calcular_periodo(w_capital_inicial,
                                                             w_fecha_ultimo_vencimiento_tratado,
                                                             w_fecha_vencimiento_calculado,
                                                             tasa)
        if cuota_1sec < w_capital_inicial + w_intereses_vencimiento + w_seguro_vencimiento - capital_2sec:
            w_mensualidad_vencimiento = cuota_1sec
        else:
            w_mensualidad_vencimiento = w_capital_inicial + w_intereses_vencimiento + w_seguro_vencimiento - capital_2sec
        w_capital_vencimiento = w_mensualidad_vencimiento - w_intereses_vencimiento - w_seguro_vencimiento
        w_capital_pendiente = w_capital_inicial - w_capital_vencimiento
        w_dia_año = tools.dias_año(w_fecha_vencimiento_calculado)
        alimentar_cuadro_amortizacion(w_tipo_vencimiento,
                                      w_numero_vencimiento,
                                      tools.mostrar_fecha(w_fecha_vencimiento_calculado),
                                      w_capital_inicial,
                                      w_mensualidad_vencimiento,
                                      w_intereses_vencimiento,
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      w_seguro_vencimiento,
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      tools.redondear_decimal(0.00),
                                      w_capital_vencimiento,
                                      w_capital_pendiente,
                                      w_intereses_vencimiento + w_capital_vencimiento,
                                      w_dia_año,
                                      tools_tae.calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion, w_fecha_vencimiento_calculado,w_dia_año),
                                      tools.mostrar_fecha(w_fecha_ultimo_vencimiento_tratado + tools.pd.DateOffset(days=1)),
                                      cuota_1sec,
                                      tasa)
        w_fecha_ultimo_vencimiento_tratado = w_fecha_vencimiento_calculado

    '''Generar los vencimientos de la segunda secuencia en caso de que exista'''
    if plazo_2sec > 0:
        for i in range(1, plazo_2sec + 1):
            w_numero_vencimiento += 1
            w_capital_inicial = w_capital_pendiente
            w_fecha_vencimiento_calculado = w_fecha_ultimo_vencimiento_tratado + tools.pd.DateOffset(months=1)
            w_seguro_vencimiento = tools.calcular_periodo(w_capital_inicial,
                                                          w_fecha_ultimo_vencimiento_tratado,
                                                          w_fecha_vencimiento_calculado,
                                                          tasa_ade)
            if (w_numero_vencimiento == plazo_2sec + plazo
                and cuota_2sec <  w_capital_inicial + w_seguro_vencimiento + tools.calcular_periodo(w_capital_inicial,
                                                                                                    w_fecha_ultimo_vencimiento_tratado,
                                                                                                    w_fecha_vencimiento_calculado,
                                                                                                    tasa_2sec)):
                w_intereses_vencimiento = (tools.calcular_periodo(w_capital_inicial,
                                                                  w_fecha_ultimo_vencimiento_tratado,
                                                                  w_fecha_vencimiento_calculado,
                                                                  tasa_2sec)
                                           - tools.calcular_periodo(w_capital_inicial,
                                                                    w_fecha_ultimo_vencimiento_tratado,
                                                                    w_fecha_vencimiento_calculado,
                                                                    tasa_2sec)
                                           + w_capital_inicial + w_seguro_vencimiento - cuota_2sec)
            else:
                w_intereses_vencimiento = tools.calcular_periodo(w_capital_inicial,
                                                                 w_fecha_ultimo_vencimiento_tratado,
                                                                 w_fecha_vencimiento_calculado,
                                                                 tasa_2sec)
            if cuota_2sec < w_capital_inicial + w_intereses_vencimiento + w_seguro_vencimiento:
                w_mensualidad_vencimiento = cuota_2sec
            else:
                w_mensualidad_vencimiento = w_capital_inicial + w_intereses_vencimiento + w_seguro_vencimiento
            w_capital_vencimiento = w_mensualidad_vencimiento - w_intereses_vencimiento - w_seguro_vencimiento
            w_capital_pendiente = w_capital_inicial - w_capital_vencimiento
            w_dia_año = tools.dias_año(w_fecha_vencimiento_calculado)
            alimentar_cuadro_amortizacion("Amort. 2ª sec.",
                                          w_numero_vencimiento,
                                          tools.mostrar_fecha(w_fecha_vencimiento_calculado),
                                          w_capital_inicial,
                                          w_mensualidad_vencimiento,
                                          w_intereses_vencimiento,
                                          tools.redondear_decimal(0.00),
                                          tools.redondear_decimal(0.00),
                                          w_seguro_vencimiento,
                                          tools.redondear_decimal(0.00),
                                          tools.redondear_decimal(0.00),
                                          tools.redondear_decimal(0.00),
                                          tools.redondear_decimal(0.00),
                                          w_capital_vencimiento,
                                          w_capital_pendiente,
                                          w_intereses_vencimiento + w_capital_vencimiento,
                                          w_dia_año,
                                          tools_tae.calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion, w_fecha_vencimiento_calculado,w_dia_año),
                                          tools.mostrar_fecha(w_fecha_ultimo_vencimiento_tratado + tools.pd.DateOffset(days=1)),
                                          cuota_2sec,
                                          tasa_2sec)
            w_fecha_ultimo_vencimiento_tratado = w_fecha_vencimiento_calculado
    
    ''' Calcular la TAE de la operación con el listado de "cuota_tae", la fracción temporal entre la financiación y el vencimiento y el TIN'''
    tae = tools_tae.calcular_tae(cuota_tae, tiempo, tasa, van_cuota_tae)
    
    ''' Crear el diccionario con los datos del cuadro de amortización y de la TAE'''
    datos_amortizacion = {
    'Tipo vcto' : tipo_vencimiento,
    'Nº Vcto' : numero_vencimiento,
    'F_Inicio' : f_inicio_periodo,
    'F_Vcto' : fecha_vencimiento,
    'Int. CAP. vcto' : intereses_capitalizados_vencimiento,
    'ASS CAP. vcto' : seguro_capitalizados_vencimiento,
    'Com. vcto' : comisiones_vencimiento,
    'Cap. finan.' : capital_financiado_periodo,
    'Cap. inicial' : capital_inicial,
    'Mens. vcto' : mensualidad_vencimiento,
    'Int. DIFF vcto' : intereses_diferidos_vencimiento,
    'Int. vcto' : intereses_vencimiento,
    'ASS DIFF vcto' : seguro_diferidos_vencimiento,
    'ASS vcto' : seguro_vencimiento,
    'Cap. vcto' : capital_vencimiento,
    'Cap. PDTE' : capital_pendiente,
    'TIN' : tasa_periodo,
    'Cuota teórica' : mensualidad_contractual,
}
    datos_tae = {
    'Fecha_Vencimiento' : fecha_vencimiento,
    'cuota_tae' : cuota_tae,
    'Año_Base' : año_base,
    'Tiempo': tiempo,
    'van_cuota_tae' : van_cuota_tae
}
    '''Crear el dataframe con el cuadro de amortización a mostrar'''
    cuadro_amortizacion = tools.pd.DataFrame(datos_amortizacion)
    
    '''Crear el dataframe con el cuadro de cálculo TAE a mostrar'''
    input_tae = tools.pd.DataFrame(datos_tae)
    
    ''' Crear las variables con los sumatorios del cuadro de amortización'''
    intereses = sum(intereses_vencimiento) + sum(intereses_capitalizados_vencimiento) 
    coste_seguro = sum(seguro_vencimiento) + sum(seguro_capitalizados_vencimiento)
    coste_total = intereses + comision_apertura # + coste_seguro
    importe_total_a_pagar = sum(mensualidad_vencimiento)
    
    cuadro_secuencias = cuadro_amortizacion[cuadro_amortizacion['Tipo vcto'] != "Financiación"]
    
    cuenta_vencimientos = cuadro_secuencias['Tipo vcto'].value_counts()
    primeros = cuadro_secuencias.groupby('Tipo vcto').head(1)
    ultimos = cuadro_secuencias.groupby('Tipo vcto').tail(1)

    resumen1 = tools.pd.DataFrame(
        {
            "TAE": [tools.formatear_decimales(float(tae))],
        },
    index=["%"],
    )

    resumen2 = tools.pd.DataFrame(
        {
            "Importe total a pagar": [tools.formatear_decimales(importe_total_a_pagar)],
            "Capital": [tools.formatear_decimales(capital_prestado)],
            "Prima de seguro": [tools.formatear_decimales(coste_seguro)],
            "Coste total": [tools.formatear_decimales(coste_total)],
            "Intereses": [tools.formatear_decimales(intereses)],
            "Comisión de apertura": [tools.formatear_decimales(comision_apertura)],
            "Importe del crédito": [tools.formatear_decimales(importe_crédito)],
            "Descuento Partner": [tools.formatear_decimales(descuento)],
        },
    index=["EUR"],
    )

    resumen3 = tools.pd.DataFrame(
    {
        "Nº Vencimientos": cuenta_vencimientos.loc[ultimos['Tipo vcto']].values,
        "TIN": [tools.formatear_decimales(tin) for tin in primeros['TIN'].values],
        "F_INI": [tools.mostrar_fecha(fecha) for fecha in primeros['F_Inicio'].values],
        "IMP_Cuota": [tools.formatear_decimales(cuota) for cuota in primeros['Cuota teórica'].values],
        "F_1er_VCTO":  [tools.mostrar_fecha(fecha) for fecha in primeros['F_Vcto'].values],
        "IMP_1era_Cuota": [tools.formatear_decimales(prim_vcto) for prim_vcto in primeros['Mens. vcto'].values],
        "F_FIN":  [tools.mostrar_fecha(fecha) for fecha in ultimos['F_Vcto'].values],
        "IMP_ULT_Cuota": [tools.formatear_decimales(ult_vcto) for ult_vcto in ultimos['Mens. vcto'].values],
    },
    index=ultimos['Tipo vcto'].values,
    )
    
    ej_repr_seccion_1 = f"Para un préstamo de importe/PVP {tools.formatear_decimales(capital_prestado)} €, con un tipo de interés fijo del {tools.formatear_decimales(tasa)} % anual y TAE de {tools.formatear_decimales(float(tae))} %, "

    if LISTA_PRODUCTOS.index(etiqueta_producto) in (6, 7):
        if cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2] == 1:
            ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2]} mensualidades, de {tools.formatear_decimales(primeros['Mens. vcto'].values[-2])} € al mes. "
        else:
            if primeros['Cuota teórica'].values[-2] == ultimos['Mens. vcto'].values[-2] and primeros['Cuota teórica'].values[-2] == primeros['Mens. vcto'].values[-2]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2]} mensualidades, de {tools.formatear_decimales(primeros['Cuota teórica'].values[-2])} € al mes. "
            elif primeros['Cuota teórica'].values[-2] != ultimos['Mens. vcto'].values[-2] and primeros['Cuota teórica'].values[-2] == primeros['Mens. vcto'].values[-2]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2]} mensualidades, por importe de {tools.formatear_decimales(primeros['Cuota teórica'].values[-2])} € al mes, y la última mensualidad de {tools.formatear_decimales(ultimos['Mens. vcto'].values[-2])} € "
            elif primeros['Cuota teórica'].values[-2] == ultimos['Mens. vcto'].values[-2] and primeros['Cuota teórica'].values[-2] != primeros['Mens. vcto'].values[-2]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2]} mensualidades, por importe de {tools.formatear_decimales(primeros['Cuota teórica'].values[-2])} € al mes, la primera mensualidad de {tools.formatear_decimales(primeros['Mens. vcto'].values[-2])} € "
            else:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-2]} mensualidades, por importe de {tools.formatear_decimales(primeros['Cuota teórica'].values[-2])} € al mes, la primera mensualidad de {tools.formatear_decimales(primeros['Mens. vcto'].values[-2])} € y la última mensualidad de {tools.formatear_decimales(ultimos['Mens. vcto'].values[-2])} € "
        if cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1] == 1:
            ej_repr_seccion_2 = ej_repr_seccion_2 + f"y {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades con un tipo de interés fijo del {tools.formatear_decimales(tasa_2sec)} % anual, de {tools.formatear_decimales(primeros['Mens. vcto'].values[-1])} € al mes. "
        else:
            if primeros['Cuota teórica'].values[-1] == ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] == primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = ej_repr_seccion_2 + f"y {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades con un tipo de interés fijo del {tools.formatear_decimales(tasa_2sec)} % anual, de {tools.formatear_decimales(primeros['Cuota teórica'].values[-1])} € al mes. "
            elif primeros['Cuota teórica'].values[-1] != ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] == primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = ej_repr_seccion_2 + f"y {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades con un tipo de interés fijo del {tools.formatear_decimales(tasa_2sec)} % anual, por importe de {tools.formatear_decimales(primeros['Cuota teórica'].values[-1])} € al mes, y la última mensualidad de {tools.formatear_decimales(ultimos['Mens. vcto'].values[-1])} €. "
            elif primeros['Cuota teórica'].values[-1] == ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] != primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = ej_repr_seccion_2 + f"y {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades con un tipo de interés fijo del {tools.formatear_decimales(tasa_2sec)} % anual, por importe de {tools.formatear_decimales(primeros['Cuota teórica'].values[-1])} € al mes, la primera mensualidad de {tools.formatear_decimales(primeros['Mens. vcto'].values[-1])} €. "
            else:
                ej_repr_seccion_2 = ej_repr_seccion_2 + f"y {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades con un tipo de interés fijo del {tools.formatear_decimales(tasa_2sec)} % anual, por importe de {tools.formatear_decimales(primeros['Cuota teórica'].values[-1])} € al mes, la primera mensualidad de {tools.formatear_decimales(primeros['Mens. vcto'].values[-1])} € y la última mensualidad de {tools.formatear_decimales(ultimos['Mens. vcto'].values[-1])} €. "
    else:
        if cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1] == 1:
            ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades, de {tools.formatear_decimales(primeros['Mens. vcto'].values[-1])} € al mes. "
        else:
            if primeros['Cuota teórica'].values[-1] == ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] == primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades, de {tools.formatear_decimales(primeros['Cuota teórica'].values[-1])} € al mes. "
            elif primeros['Cuota teórica'].values[-1] != ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] == primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades, por importe de {tools.formatear_decimales(primeros['Cuota teórica'].values[-1])} € al mes, y la última mensualidad de {tools.formatear_decimales(ultimos['Mens. vcto'].values[-1])} €. "
            elif primeros['Cuota teórica'].values[-1] == ultimos['Mens. vcto'].values[-1] and primeros['Cuota teórica'].values[-1] != primeros['Mens. vcto'].values[-1]:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades, por importe de {tools.formatear_decimales(primeros['Cuota teórica'].values[-1])} € al mes, la primera mensualidad de {tools.formatear_decimales(primeros['Mens. vcto'].values[-1])} €. "
            else:
                ej_repr_seccion_2 = f"se paga en {cuenta_vencimientos.loc[ultimos['Tipo vcto']].values[-1]} mensualidades, por importe de {tools.formatear_decimales(primeros['Cuota teórica'].values[-1])} € al mes, la primera mensualidad de {tools.formatear_decimales(primeros['Mens. vcto'].values[-1])} € y la última mensualidad de {tools.formatear_decimales(ultimos['Mens. vcto'].values[-1])} €. "
    if carencia >0:
        ej_repr_seccion_2 = f"con un período de carencia de {carencia} meses, " + ej_repr_seccion_2

    if comision_apertura > 0:
        if comision_apertura_capitalizada:
            ej_repr_seccion_3 = f"Comisión de apertura financiada: {tools.formatear_decimales(comision_apertura)} € (del {tools.formatear_decimales(tasa_comision_apertura)} %). Importe total de los intereses: {tools.formatear_decimales(intereses)} €. Coste total del préstamo: {tools.formatear_decimales(coste_total)} €. "
        else:
            ej_repr_seccion_3 = f"Comisión de apertura en la primera mensualidad: {tools.formatear_decimales(comision_apertura)} € (del {tools.formatear_decimales(tasa_comision_apertura)} %). Importe total de los intereses: {tools.formatear_decimales(intereses)} €. Coste total del préstamo: {tools.formatear_decimales(coste_total)} €. "
    else:
        ej_repr_seccion_3 = f"Coste total del préstamo / Importe total de intereses: {tools.formatear_decimales(coste_total)} €. "

    ej_repr_seccion_4 = f"Importe total adeudado/precio total a plazos: {tools.formatear_decimales(importe_total_a_pagar)} €. Sistema de amortización francés."
    
    
    ejemplo_representativo = ej_repr_seccion_1 + ej_repr_seccion_2 + ej_repr_seccion_3 + ej_repr_seccion_4
    
    ''' Convertir DataFrames a str para compatibilidad con Arrow en Streamlit 1.56 '''
    cuadro_amortizacion = cuadro_amortizacion.astype(str)
    input_tae = input_tae.astype(str)
    resumen1 = resumen1.astype(str)
    resumen2 = resumen2.astype(str)
    resumen3 = resumen3.astype(str)
    
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
        
    return (resumen1,
            resumen2,
            resumen3,
            ejemplo_representativo,
            cuadro_amortizacion,
            input_tae)



def simular_masivamente(capital_2sec,
                        carencias,
                        comision_apertura_capitalizada,
                        dia_pago,
                        entrega_a_cuenta,
                        etiqueta_producto,
                        fechas_financiacion,
                        imp_max_com_apertura,
                        importes_prestado,
                        on,
                        plazo_2sec,
                        plazos,
                        seguro_titular_1,
                        seguro_titular_2,
                        tasa,
                        tasa_2sec,
                        tasa_comision_apertura):


    ''' Inicializar los acumulados de resultados de la simulación masiva '''
    acumulado_tae.clear()
    acumulado_comision_apertura.clear()
    acumulado_importe_total_a_pagar.clear()
    acumulado_coste_total.clear()
    acumulado_intereses.clear()
    acumulado_coste_seguro.clear()
    acumulado_importe_crédito.clear()
    acumulado_descuento.clear()
    acumulado_tasa.clear()
    acumulado_cuota_1sec.clear()
    acumulado_cuota_2sec.clear()
    acumulado_fecha_fin_carencia_gratuita_forzada.clear()
    acumulado_fecha_fin_carencia_diferida.clear()
    acumulado_fecha_fin_carencia.clear()
    acumulado_fecha_primer_vencimiento.clear()
    acumulado_ejemplo_representativo.clear()
    acumulado_capital_2sec.clear()
    acumulado_carencia.clear()
    acumulado_comision_apertura_capitalizada.clear()
    acumulado_dia_pago.clear()
    acumulado_etiqueta_producto.clear()
    acumulado_fecha_financiacion.clear()
    acumulado_imp_max_com_apertura.clear()
    acumulado_capital_prestado.clear()
    acumulado_on.clear()
    acumulado_plazo_2sec.clear()
    acumulado_plazos.clear()
    acumulado_seguro_titular_1.clear()
    acumulado_seguro_titular_2.clear()
    acumulado_tasa_2sec.clear()
    acumulado_tasa_comision_apertura.clear()
    
    tasa_entrada = tasa

    ''' Desplegar las listas de duraciones / importes / carencia '''
    w_capital_2sec = capital_2sec
    fechas_financiacion = tools.pd.date_range(start=fechas_financiacion[0],
                                              end=fechas_financiacion[1],
                                              freq='D')
    if len(carencias) > 1:
        carencias = [i for i in range(carencias[0], carencias[1] + 1, 1)]
    if LISTA_PRODUCTOS.index(etiqueta_producto) in (0, 1, 8, 9, 10, 11):
        importes_prestado = list(tools.np.arange(importes_prestado[0], importes_prestado[1] + 1.0, 500.0))
        plazos = [i for i in range(plazos[0], plazos[1] + 1, 12)]
    else:
        importes_prestado = list(tools.np.arange(importes_prestado[0], importes_prestado[1] + 1.0, 50.0))
        plazos = [i for i in range(plazos[0], plazos[1] + 1, 1)]
    
    ''' Función la simulación masiva de préstamos amortizables '''
    for fecha_financiacion in fechas_financiacion:
        for capital_prestado in importes_prestado:
            w_capital_prestado = capital_prestado
            capital_prestado = (capital_prestado - entrega_a_cuenta)
            if on:
                capital_2sec = tools.redondear_decimal(w_capital_prestado * w_capital_2sec / 100)
            for carencia in carencias:
                for plazo in plazos:
                    (
                        tae,
                        comision_apertura,
                        importe_total_a_pagar,
                        coste_total,
                        intereses,
                        coste_seguro,
                        importe_crédito,
                        descuento,
                        tasa_result,
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
                        tasa_entrada,
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
                    ''' Acumular los resultados de la simulación masiva '''
                    acumulado_tae.append(tools.formatear_decimales(tae))
                    acumulado_comision_apertura.append(tools.formatear_decimales(comision_apertura))
                    acumulado_importe_total_a_pagar.append(tools.formatear_decimales(importe_total_a_pagar))
                    acumulado_coste_total.append(tools.formatear_decimales(coste_total))
                    acumulado_intereses.append(tools.formatear_decimales(intereses))
                    acumulado_coste_seguro.append(tools.formatear_decimales(coste_seguro))
                    acumulado_importe_crédito.append(tools.formatear_decimales(importe_crédito))
                    acumulado_descuento.append(tools.formatear_decimales(descuento))
                    acumulado_tasa.append(tools.formatear_decimales(tasa_result))
                    acumulado_cuota_1sec.append(tools.formatear_decimales(cuota_1sec))
                    acumulado_cuota_2sec.append(tools.formatear_decimales(cuota_2sec))
                    acumulado_fecha_fin_carencia_gratuita_forzada.append(tools.mostrar_fecha(fecha_fin_carencia_gratuita_forzada))
                    acumulado_fecha_fin_carencia_diferida.append(tools.mostrar_fecha(fecha_fin_carencia_diferida))
                    acumulado_fecha_fin_carencia.append(tools.mostrar_fecha(fecha_fin_carencia))
                    acumulado_fecha_primer_vencimiento.append(tools.mostrar_fecha(fecha_primer_vencimiento))
                    acumulado_ejemplo_representativo.append(ejemplo_representativo)
                    acumulado_capital_2sec.append(tools.formatear_decimales(capital_2sec))
                    acumulado_carencia.append(tools.formatear_decimales(carencia))
                    acumulado_comision_apertura_capitalizada.append(comision_apertura_capitalizada)
                    acumulado_dia_pago.append(dia_pago)
                    acumulado_etiqueta_producto.append(etiqueta_producto)
                    acumulado_fecha_financiacion.append(tools.mostrar_fecha(fecha_financiacion))
                    acumulado_imp_max_com_apertura.append(tools.formatear_decimales(imp_max_com_apertura))
                    acumulado_capital_prestado.append(tools.formatear_decimales(float(capital_prestado)))
                    acumulado_on.append(on)
                    acumulado_plazo_2sec.append(plazo_2sec)
                    acumulado_plazos.append(plazo)
                    acumulado_seguro_titular_1.append(seguro_titular_1)
                    acumulado_seguro_titular_2.append(seguro_titular_2)
                    acumulado_tasa_2sec.append(tools.formatear_decimales(tasa_2sec))
                    acumulado_tasa_comision_apertura.append(tools.formatear_decimales(tasa_comision_apertura))    

    ''' Crear el diccionario con los datos del cuadro de amortización y de la TAE'''
    resultado_simulacion_masiva = {
        'TAE' : acumulado_tae,
        'Ejemplo Representativo' : acumulado_ejemplo_representativo,
        'Etiqueta producto': acumulado_etiqueta_producto,
        'Capital prestado': acumulado_capital_prestado,
        'Carencia': acumulado_carencia,
        'Plazos': acumulado_plazos,
        'TIN' : acumulado_tasa,
        'Cuota residual porcentual': acumulado_on,
        'Capital 2sec': acumulado_capital_2sec,
        'Tasa 2sec': acumulado_tasa_2sec,
        'Plazo 2sec': acumulado_plazo_2sec,
        'Comision apertura capitalizada': acumulado_comision_apertura_capitalizada,
        'Tasa comision apertura': acumulado_tasa_comision_apertura,
        'Imp max com apertura': acumulado_imp_max_com_apertura,
        'Dia pago': acumulado_dia_pago,
        'Fecha financiacion': acumulado_fecha_financiacion,
        'Seguro titular 1': acumulado_seguro_titular_1,
        'Seguro titular 2': acumulado_seguro_titular_2,
        'Imp. Total a Pagar' : acumulado_importe_total_a_pagar,
        'Coste Total' : acumulado_coste_total,
        'Intereses' : acumulado_intereses,
        'Imp. Com. Apert.' : acumulado_comision_apertura,
        'Coste Seguro' : acumulado_coste_seguro,
        'Imp. Crédito' : acumulado_importe_crédito,
        'Descuento Partner' : acumulado_descuento,
        'Mens. 1º Sec.' : acumulado_cuota_1sec,
        'Mens. 2ª Sec.' : acumulado_cuota_2sec,
        'F_Fin carencia forzada' : acumulado_fecha_fin_carencia_gratuita_forzada,
        'F_Fin carencia diferida' : acumulado_fecha_fin_carencia_diferida,
        'F_Fin carencia' : acumulado_fecha_fin_carencia,
        'F_1er_Vcto' : acumulado_fecha_primer_vencimiento,
        }
    '''Crear el dataframe con el cuadro de amortización a mostrar'''
    resultado_simulacion_masiva = tools.pd.DataFrame(resultado_simulacion_masiva)
    
    return resultado_simulacion_masiva
