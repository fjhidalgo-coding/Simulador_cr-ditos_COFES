#!
'''Programa para la simulación de los productos amortizables de COF_ES'''

import datetime as dt
from decimal import Decimal
import pandas as pd
import numpy as np
import bin.COFES___TAE as tools_tae
import bin.COFES___tools as tools



''' Declarar variables globales '''

tipo_vencimiento = []
numero_vencimiento = []
fecha_vencimiento = []
capital_inicial = []
mensualidad_vencimiento = []
comisiones_vencimiento = []
capital_financiado_periodo = []
capital_vencimiento = []
capital_pendiente = []
cuota_tae = []
año_base = []
tiempo = []
van_cuota_tae = []

acumulado_tae = []
acumulado_comision_apertura = []
acumulado_importe_total_a_pagar = []
acumulado_coste_total = []
acumulado_ejemplo_representativo = []
acumulado_fecha_financiacion = []
acumulado_capital_prestado = []
acumulado_tasa_comision_apertura = []


def alimentar_cuadro_amortizacion(w_tipo_vencimiento, 
                                  w_numero_vencimiento, 
                                  w_fecha_vencimiento, 
                                  w_capital_inicial, 
                                  w_mensualidad_vencimiento, 
                                  w_comisiones_vencimiento, 
                                  w_capital_financiado_periodo, 
                                  w_capital_vencimiento, 
                                  w_capital_pendiente, 
                                  w_cuota_tae, 
                                  w_año_base, 
                                  w_tiempo):
    '''Función para almacenar la construcción del cuadro de amortización asociado a la instrucción'''
    tipo_vencimiento.append(w_tipo_vencimiento)
    numero_vencimiento.append(w_numero_vencimiento)
    fecha_vencimiento.append(w_fecha_vencimiento)
    capital_inicial.append(w_capital_inicial)
    mensualidad_vencimiento.append(w_mensualidad_vencimiento)
    comisiones_vencimiento.append(w_comisiones_vencimiento)
    capital_financiado_periodo.append(w_capital_financiado_periodo)
    capital_vencimiento.append(w_capital_vencimiento)
    capital_pendiente.append(w_capital_pendiente)
    cuota_tae.append(w_cuota_tae)
    año_base.append(w_año_base)
    tiempo.append(w_tiempo)



def simular_prestamo_4CB(capital_prestado_4CB,
                         tasa_comision_apertura_4CB,
                         fecha_financiacion_4CB):
    
    '''Función principal para la simulación de los productos amortizables de COF_ES'''
    
    # Convertir entradas a Decimal para cálculos en base 10 exacta
    capital_prestado_4CB = Decimal(str(capital_prestado_4CB))
    tasa_comision_apertura_4CB = Decimal(str(tasa_comision_apertura_4CB))

    '''Limpiar variables del cuadro de amortización de la operación simulada con anterioridad'''
    tipo_vencimiento.clear()
    numero_vencimiento.clear()
    fecha_vencimiento.clear()
    capital_inicial.clear()
    mensualidad_vencimiento.clear()
    comisiones_vencimiento.clear()
    capital_financiado_periodo.clear()
    capital_vencimiento.clear()
    capital_pendiente.clear()
    cuota_tae.clear()
    año_base.clear()
    tiempo.clear()
    van_cuota_tae.clear()
    
    '''Calcular la comisión de apertura'''
    comision_apertura = tools.truncar_decimal(capital_prestado_4CB * tasa_comision_apertura_4CB / 100, 2)
    
    '''Calcular cuota de la facilidad de pago 4CB'''
    cuota_4CB = tools.truncar_decimal((capital_prestado_4CB + comision_apertura) / 4, 2)
    
    '''Calcular capital de los vencimientos de la facilidad de pago 4CB'''
    capital_4CB = tools.truncar_decimal(capital_prestado_4CB / 4, 2)
    
    '''Calcular capital del primer vencimiento de la facilidad de pago 4CB0'''
    ajuste_1er_vencimiento = capital_prestado_4CB - (capital_4CB * 4)
    
    
    '''Crear el cuadro de amortización'''
    cuadro_amortizacion = pd.DataFrame()
    
    '''Alimentar cuadro de amortización'''
    dias_vencimiento = [0, 1, 32, 63, 90]
    w_capital_inicial = Decimal('0.00')
    
    for i in range(5):
        w_fecha_vencimiento = fecha_financiacion_4CB + dt.timedelta(days=dias_vencimiento[i])
        w_mensualidad_vencimiento = Decimal(cuota_4CB + ajuste_1er_vencimiento) if i == 1 and tasa_comision_apertura_4CB == 0.00 else Decimal(str(cuota_4CB)) if i > 0 else Decimal('0.00')
        w_capital_financiado_periodo = capital_prestado_4CB if i == 0 else Decimal('0.00')
        w_capital_vencimiento = Decimal(str(tools.redondear_decimal(capital_4CB + ajuste_1er_vencimiento))) if i == 1 else Decimal(str(capital_4CB)) if i > 1 else -capital_prestado_4CB
        w_capital_pendiente = Decimal(str(tools.redondear_decimal(w_capital_inicial - w_capital_vencimiento)))
        w_comisiones_vencimiento = Decimal(str(tools.redondear_decimal(w_mensualidad_vencimiento - w_capital_vencimiento))) if i > 0 and tasa_comision_apertura_4CB > 0.00 else Decimal('0.00')
        w_dia_año = tools.dias_año(w_fecha_vencimiento)
        
        alimentar_cuadro_amortizacion("Amortización" if i > 0 else "Financiación",
                                      i, 
                                      tools.mostrar_fecha(w_fecha_vencimiento),
                                      w_capital_inicial, 
                                      w_mensualidad_vencimiento, 
                                      w_comisiones_vencimiento, 
                                      w_capital_financiado_periodo, 
                                      w_capital_vencimiento, 
                                      w_capital_pendiente, 
                                      w_capital_vencimiento + w_comisiones_vencimiento, 
                                      w_dia_año, 
                                      tools_tae.calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion_4CB, w_fecha_vencimiento,w_dia_año))
        w_capital_inicial = w_capital_pendiente

    ''' Calcular la TAE de la operación con el listado de "cuota_tae", la fracción temporal entre la financiación y el vencimiento y el TIN'''
    tae = tools_tae.calcular_tae(cuota_tae, tiempo, tasa_comision_apertura_4CB * 10, van_cuota_tae)
    
    ''' Crear el diccionario con los datos del cuadro de amortización y de la TAE'''
    datos_amortizacion = {
    'Tipo vcto' : tipo_vencimiento,
    'Nº Vcto' : numero_vencimiento,
    'F_Vcto' : fecha_vencimiento,
    'Cap. finan.' : capital_financiado_periodo,
    'Cap. inicial' : capital_inicial,
    'Mens. vcto' : mensualidad_vencimiento,
    'Com. vcto' : comisiones_vencimiento,
    'Cap. vcto' : capital_vencimiento,
    'Cap. PDTE' : capital_pendiente,
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
    comision_apertura = sum(comisiones_vencimiento)
    coste_total = comision_apertura
    importe_total_a_pagar = sum(mensualidad_vencimiento)
    
    resumen1 = pd.DataFrame(
        {
            "TAE": [tools.formatear_decimales(tae)],
        },
    index=["%"],
    )

    resumen2 = pd.DataFrame(
        {
            "Importe total a pagar": [tools.formatear_decimales(importe_total_a_pagar)],
            "Capital": [tools.formatear_decimales(capital_prestado_4CB)],
            "Coste total": [tools.formatear_decimales(coste_total)],
            "Comisión de apertura": [tools.formatear_decimales(comision_apertura)],
        },
    index=["EUR"],
    )

    ''' Crear el ejemplo representativo de la operación simulada '''
    if tasa_comision_apertura_4CB == 0.00 and mensualidad_vencimiento[1] != mensualidad_vencimiento[2]:
        ej_repr_seccion_1 = f"Ejemplo de financiación con promoción para importe PVP {tools.formatear_decimales(capital_prestado_4CB)} €: 4 cuotas, la primera de {tools.formatear_decimales(mensualidad_vencimiento[1])} € y el resto de {tools.formatear_decimales(mensualidad_vencimiento[2])} €. Importe total adeudado/precio total a plazos: {tools.formatear_decimales(importe_total_a_pagar)} €. Comisión de apertura financiada (0 %) / coste total del préstamo: 0 € . TIN 0 %. TAE 0 %."
    elif tasa_comision_apertura_4CB == 0.00:
        ej_repr_seccion_1 = f"Ejemplo de financiación con promoción para importe PVP {tools.formatear_decimales(capital_prestado_4CB)} €: 4 cuotas de {tools.formatear_decimales(mensualidad_vencimiento[1])} €. Importe total adeudado/precio total a plazos: {tools.formatear_decimales(importe_total_a_pagar)} €. Comisión de apertura financiada (0 %) / coste total del préstamo: 0 € . TIN 0 %. TAE 0 %."
    else:
        ej_repr_seccion_1 = f"Ejemplo de financiación sin promoción para importe PVP {tools.formatear_decimales(capital_prestado_4CB)} €: 4 cuotas de {tools.formatear_decimales(mensualidad_vencimiento[1])} €. Importe total adeudado/precio total a plazos: {tools.formatear_decimales(importe_total_a_pagar)} €. Comisión de apertura financiada / coste total del préstamo: {tools.formatear_decimales(comision_apertura)} € ({tools.formatear_decimales(tasa_comision_apertura_4CB)} %). TIN 0 %. TAE {tools.formatear_decimales(tae)} %."
    
    ej_repr_seccion_2 = f"\nFecha de financiación del ejemplo representativo {tools.mostrar_fecha(fecha_vencimiento[0])} y primera amortización el {tools.mostrar_fecha(fecha_vencimiento[1])}, segunda el {tools.mostrar_fecha(fecha_vencimiento[2])}, tercera el {tools.mostrar_fecha(fecha_vencimiento[3])} y cuarta el {tools.mostrar_fecha(fecha_vencimiento[4])}."
    ej_repr_seccion_3 = f"Sistema de amortización francés. Para otros importes y/o plazos, consulte condiciones de financiación."
    
    ejemplo_representativo = ej_repr_seccion_1 + ej_repr_seccion_2 + ej_repr_seccion_3

    
    return (tae,
            comision_apertura,
            importe_total_a_pagar,
            coste_total, 
            cuadro_amortizacion, 
            input_tae, 
            resumen1, 
            resumen2, 
            ejemplo_representativo)

def visualizar_simulacion_unitaria(capital_prestado_4CB,
                                   tasa_comision_apertura_4CB,
                                   fecha_financiacion_4CB):
    ''' Función para simplificar el retorno de la simulación completa que es utilizada para mostrar las simulaciones unitarias '''
    (
        tae,
        comision_apertura,
        importe_total_a_pagar,
        coste_total, 
        cuadro_amortizacion, 
        input_tae, 
        resumen1, 
        resumen2, 
        ejemplo_representativo
    ) = simular_prestamo_4CB(
        capital_prestado_4CB,
        tasa_comision_apertura_4CB,
        fecha_financiacion_4CB
    )
        
    return (resumen1,
            resumen2,
            ejemplo_representativo,
            cuadro_amortizacion,
            input_tae)

def simular_masivamente(importes_prestado_4CB,
                        tasas_comision_apertura_4CB,
                        fechas_financiacion_4CB):


    ''' Inicializar los acumulados de resultados de la simulación masiva '''
    acumulado_tae.clear()
    acumulado_comision_apertura.clear()
    acumulado_importe_total_a_pagar.clear()
    acumulado_coste_total.clear()
    acumulado_ejemplo_representativo.clear()
    acumulado_fecha_financiacion.clear()
    acumulado_capital_prestado.clear()
    acumulado_tasa_comision_apertura.clear()

    ''' Desplegar las listas de duraciones / importes / carencia '''
    importes_prestado_4CB = list(np.round(np.arange(importes_prestado_4CB[0], importes_prestado_4CB[1] + 0.01, 0.01), 2))
    tasas_comision_apertura_4CB = list(np.round(np.arange(tasas_comision_apertura_4CB[0], tasas_comision_apertura_4CB[1] + 0.01, 0.10), 2))
    
    ''' Función la simulación masiva de préstamos amortizables '''
    for capital_prestado_4CB in importes_prestado_4CB:
        for tasa_comision_apertura_4CB in tasas_comision_apertura_4CB:
            (
                tae,
                comision_apertura,
                importe_total_a_pagar,
                coste_total, 
                cuadro_amortizacion, 
                input_tae, 
                resumen1, 
                resumen2, 
                ejemplo_representativo
            ) = simular_prestamo_4CB(
                capital_prestado_4CB,
                tasa_comision_apertura_4CB,
                fechas_financiacion_4CB
            )
            ''' Acumular los resultados de la simulación masiva '''
            acumulado_tae.append(tools.formatear_decimales(tae))
            acumulado_comision_apertura.append(tools.formatear_decimales(comision_apertura))
            acumulado_importe_total_a_pagar.append(tools.formatear_decimales(importe_total_a_pagar))
            acumulado_coste_total.append(tools.formatear_decimales(coste_total))
            acumulado_ejemplo_representativo.append(ejemplo_representativo)
            acumulado_fecha_financiacion.append(tools.mostrar_fecha(fechas_financiacion_4CB))
            acumulado_capital_prestado.append(tools.formatear_decimales(float(capital_prestado_4CB)))
            acumulado_tasa_comision_apertura.append(tools.formatear_decimales(tasa_comision_apertura_4CB))

    ''' Crear el diccionario con los datos del cuadro de amortización y de la TAE'''
    resultado_simulacion_masiva = {
        'TAE' : acumulado_tae,
        'Ejemplo Representativo' : acumulado_ejemplo_representativo,
        'Capital prestado': acumulado_capital_prestado,
        'Tasa comision apertura': acumulado_tasa_comision_apertura,
        'Fecha financiacion': acumulado_fecha_financiacion,
        'Imp. Total a Pagar' : acumulado_importe_total_a_pagar,
        'Coste Total' : acumulado_coste_total,
        'Imp. Com. Apert.' : acumulado_comision_apertura,
        }
    '''Crear el dataframe con el cuadro de amortización a mostrar'''
    resultado_simulacion_masiva = pd.DataFrame(resultado_simulacion_masiva)
    
    return resultado_simulacion_masiva
