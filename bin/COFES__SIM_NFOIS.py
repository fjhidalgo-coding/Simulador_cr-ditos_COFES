#!
'''Programa para la simulación de los productos revolving'''

import bin.COFES___TAE as tools_tae
import bin.COFES___tools as tools



''' Declarar constantes'''

DIAS_BASE = 365



''' Crear las funciones necesarias para la simulación NFOIS'''

def nfois_cuadro_amortización(capital,
                              tin,
                              cuota,
                              fecha_financiacion,
                              seguro_tasa=0,
                              dia_pago=2,
                              plazo=0,
                              fecha_primer_vencimiento=None,
                              comision_apertura=0):

    '''Función para simular un crédito NFOIScon sistema de amortización francés, con precisión día a día
    en el cálculo de intereses, y teniendo en cuenta la posible existencia de un seguro asociado al crédito.
    Devuelve un cuadro de amortización detallado con la evolución del capital pendiente, los intereses,
    la amortización y el seguro a lo largo de la vida del crédito.'''
    
    saldo = capital
    cuadro_amortización = []
        
    fecha_pago = fecha_primer_vencimiento
    fecha_anterior = fecha_financiacion

    for mes in range(1, plazo + 1):

        interes_total = tools.calcular_periodo_roto(saldo,
                                                    fecha_anterior,
                                                    fecha_pago,
                                                    tin,
                                                    DIAS_BASE)
        seguro = tools.redondear_decimal(((saldo + interes_total) * seguro_tasa))

        if mes == plazo:
            amort = tools.redondear_decimal(saldo)
            saldo = tools.redondear_decimal(0.00)
            cuota_final = tools.redondear_decimal(amort + interes_total)

        else:
            amort = tools.redondear_decimal(cuota - interes_total)
            saldo = tools.redondear_decimal(saldo - amort)
            cuota_final = tools.redondear_decimal(cuota)

        comision_mes = comision_apertura if mes == 1 else tools.redondear_decimal(0.00)
        cuota_final = tools.redondear_decimal(cuota_final + comision_mes)
        
        cuadro_amortización.append({
            "Mes": mes,
            "Fecha recibo": tools.mostrar_fecha(fecha_pago),
            "Capital pendiente (€)": float(saldo + amort),
            "Cuota (€)": float(cuota_final),
            "Intereses total (€)": float(interes_total),
            "Comisión (€)": float(comision_mes),
            "Amortización (€)": float(amort),
            "Saldo (€)": float(saldo),
            "Seguro (€)": float(seguro),
            "Recibo total (€)": float(cuota_final + seguro),
            "Fecha tae": fecha_pago,
            "Tiempo": tools_tae.calcular_fraccion_entre_financiacion_y_vencimiento(fecha_financiacion,
                                                                                   fecha_pago,
                                                                                   tools.dias_año(fecha_pago))
        })

        fecha_anterior = fecha_pago
        fecha_pago = fecha_pago + tools.pd.DateOffset(months=1)
    
    return tools.pd.DataFrame(cuadro_amortización)


def nfois_simulacion_completa(capital_prestado,
                              tasa,
                              plazo,
                              fecha_financiacion,
                              seguro_tasa,
                              dia_pago,
                              tasa_comision_apertura,
                              imp_max_com_apertura):

    '''Función para simular un crédito NFOIS'''
    
    '''Asegurar la utilización de variables de tipo Decimal para los cálculos financieros'''
    capital_prestado = tools.redondear_decimal(capital_prestado)
    tasa = tools.redondear_decimal(tasa)
    seguro_tasa = tools.truncar_decimal(seguro_tasa, 4)
    tasa_comision_apertura = tools.redondear_decimal(tasa_comision_apertura)
    imp_max_com_apertura = tools.redondear_decimal(imp_max_com_apertura)
    van_cuota_tae = []
    
    '''Obtener el importe de la comisión de apertura'''
    comision_apertura, capitalizacion_comision_apertura = tools.calcular_comision_apertura(capital_prestado,
                                                                                           tasa_comision_apertura,
                                                                                           imp_max_com_apertura,
                                                                                           False)
    
    '''Obtener las fechas relevantes de la operación'''
    (fecha_fin_carencia_gratuita_forzada,
     fecha_fin_carencia_diferida,
     fecha_fin_carencia,
     fecha_primer_vencimiento) = tools.calcular_fechas("rcc",
                                                       fecha_financiacion,
                                                       dia_pago,
                                                       0)
    
    '''Obtener el importe de la mensualidad'''
    cuota_1sec, cuota_2sec = tools.calcular_mensualidad_estandar(capital_prestado,
                                                                 tasa, 
                                                                 plazo, 
                                                                 0, 
                                                                 tools.redondear_decimal(0.00), 
                                                                 tools.redondear_decimal(0.00), 
                                                                 0, 
                                                                 tasa, 
                                                                 tools.redondear_decimal(0.00), 
                                                                 fecha_financiacion, 
                                                                 fecha_fin_carencia_gratuita_forzada, 
                                                                 fecha_fin_carencia_diferida, 
                                                                 fecha_fin_carencia,
                                                                 DIAS_BASE)
    
    '''Función para realizar la simulación completa de un crédito con sistema de amortización francés (RCC),'''
    cuadro_amortización = nfois_cuadro_amortización(capital_prestado,
                                                    tasa,
                                                    cuota_1sec,
                                                    fecha_financiacion,
                                                    seguro_tasa,
                                                    dia_pago,
                                                    plazo,
                                                    fecha_primer_vencimiento,
                                                    comision_apertura)
    
    total_intereses = tools.redondear_decimal(cuadro_amortización["Intereses total (€)"].sum())
    total_capital_intereses = tools.redondear_decimal(cuadro_amortización["Cuota (€)"].sum())

    if seguro_tasa > 0:
        total_seguro = tools.redondear_decimal(cuadro_amortización["Seguro (€)"].sum())
    else:
        total_seguro = tools.redondear_decimal(0.00)

    cuotas_tae = [-capital_prestado]+list(cuadro_amortización["Cuota (€)"])
    tiempo = [0]+list(cuadro_amortización["Tiempo"])
    
    tae = tools_tae.calcular_tae(cuotas_tae,
                                 tiempo,
                                 tasa,
                                 van_cuota_tae)

    datos_tae = {
                 'Fecha' : [tools.mostrar_fecha(fecha_financiacion)]+list(cuadro_amortización["Fecha recibo"]),
                 'cuota_tae' : cuotas_tae,
                 'Tiempo': tiempo,
                 'van_cuota_tae' : van_cuota_tae
                 }    
        
    cuadro_amortización = cuadro_amortización.drop(columns=["Fecha tae",
                                                            "Tiempo"])
    
    nfois_resumen = {
        "Concepto" : [
            "Duración (meses)",
            "Mensualidad contractual (€)",
            "TAE (%)",
            "Importe total a pagar (€)",
            "Seguro (€)",
            "Coste total (€, comisión de apertura + intereses)",
            "Intereses (€)",
            "Comisión de apertura (€)"
        ],
        "Valor" : [
            len(cuadro_amortización),
            tools.formatear_decimales(cuota_1sec),
            tools.formatear_decimales(tae),
            tools.formatear_decimales(total_capital_intereses+total_seguro),
            tools.formatear_decimales(total_seguro),
            tools.formatear_decimales(comision_apertura + total_intereses),
            tools.formatear_decimales(total_intereses),
            tools.formatear_decimales(comision_apertura)
        ]
    }
    
    nfois_resumen = tools.pd.DataFrame(nfois_resumen).transpose()

    return (tools.pd.DataFrame(cuadro_amortización),
            tools.pd.DataFrame(nfois_resumen),
            tools.pd.DataFrame(datos_tae))
