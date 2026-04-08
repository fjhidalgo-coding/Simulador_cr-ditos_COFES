#!
'''Programa para la simulación de los productos revolving'''

import bin.COFES___TAE as tools_tae
import bin.COFES___tools as tools



''' Declarar constantes'''

DIAS_BASE = 365



''' Crear las funciones necesarias para la simulación amortizable'''

def rcc_cuadro_amortización(capital,
                            tin,
                            cuota,
                            fecha_financiacion,
                            seguro_tasa=0,
                            dia_pago=2):

    '''Función para simular un crédito con sistema de amortización francés (RCC), con precisión día a día
    en el cálculo de intereses, y teniendo en cuenta la posible existencia de un seguro asociado al crédito.
    Devuelve un cuadro de amortización detallado con la evolución del capital pendiente, los intereses,
    la amortización y el seguro a lo largo de la vida del crédito.'''
    capital = tools.redondear_decimal(capital)
    cuota = tools.redondear_decimal(cuota)
    tin = tools.redondear_decimal(tin)
    seguro_tasa = tools.redondear_decimal(seguro_tasa)
    saldo = capital
    mes = 1
    cuadro_amortización = []
    
    (fecha_fin_carencia_gratuita_forzada, 
            fecha_fin_carencia_diferida,
            fecha_fin_carencia,
            fecha_primer_vencimiento) = tools.calcular_fechas("rcc",
                                                              fecha_financiacion,
                                                              dia_pago,
                                                              0)
    
    fecha_pago = fecha_primer_vencimiento
    fecha_anterior = fecha_financiacion

    while saldo > 0:

        interes_total = tools.calcular_periodo_roto(saldo,
                                                    fecha_anterior,
                                                    fecha_pago,
                                                    tin,
                                                    DIAS_BASE)
        seguro = tools.redondear_decimal(((saldo + interes_total) * seguro_tasa))

        if saldo + interes_total <= cuota:
            amort = tools.redondear_decimal(saldo)
            saldo = tools.redondear_decimal(0.00)
            cuota_final = tools.redondear_decimal(amort + interes_total)

        else:
            amort = tools.redondear_decimal(cuota - interes_total)
            saldo = tools.redondear_decimal(saldo - amort)
            cuota_final = tools.redondear_decimal(cuota)

        cuadro_amortización.append({
            "Mes": mes,
            "Fecha recibo": tools.mostrar_fecha(fecha_pago),
            "Capital pendiente (€)": float(saldo + amort),
            "Cuota (€)": float(cuota_final),
            "Intereses total (€)": float(interes_total),
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
        mes += 1

        if mes > 600:
            break
    
    return tools.pd.DataFrame(cuadro_amortización)


def rcc_obtener_duraciones(capital,
                           tin,
                           fecha_financiacion):
    
    '''Función para obtener las duraciones disponibles para un capital y TIN determinados en el producto RCC.
    Devuelve una lista de duraciones en meses y un diccionario con la cuota correspondiente a cada duración.'''
    rcc_duraciones = []
    rcc_cuotas = {}
    for v in tools.RCC_OPCIONES_VITESSE:
        cuota_test = tools.redondear_decimal(capital * v / 100)
        cuadro_amortización = rcc_cuadro_amortización(capital,
                                                      tin,
                                                      cuota_test,
                                                      fecha_financiacion,
                                                      0)
        meses = len(cuadro_amortización)
        etiqueta = f"{meses} meses"
        rcc_duraciones.append(etiqueta)
        rcc_cuotas[etiqueta] = cuota_test
    
    return rcc_duraciones, rcc_cuotas    



def rcc_simulacion_completa(capital,
                            tin,
                            cuota,
                            fecha_financiacion,
                            seguro_tasa=0,
                            dia_pago=2):
    
    '''Función para realizar la simulación completa de un crédito con sistema de amortización francés (RCC),'''
    cuadro_amortización = rcc_cuadro_amortización(capital,
                                                  tin,
                                                  cuota,
                                                  fecha_financiacion,
                                                  seguro_tasa,
                                                  dia_pago)
    
    total_intereses = tools.redondear_decimal(cuadro_amortización["Intereses total (€)"].sum())
    total_capital_intereses = tools.redondear_decimal(cuadro_amortización["Cuota (€)"].sum())

    if seguro_tasa > 0:
        total_seguro = tools.redondear_decimal(cuadro_amortización["Seguro (€)"].sum())
    else:
        total_seguro = tools.redondear_decimal(0.00)

    cuotas_tae = [-capital]+list(cuadro_amortización["Cuota (€)"])
    tiempo = [0]+list(cuadro_amortización["Tiempo"])
    
    tae = tools_tae.calcular_tae(cuotas_tae,
                                 tiempo,
                                 tin,
                                 van_cuota_tae=[])
    
    cuadro_amortización = cuadro_amortización.drop(columns=["Fecha tae",
                                                            "Tiempo"])
    
    if seguro_tasa > 0:
        rcc_resumen = {
        "Concepto" : [
        "Duración (meses)",
        "Intereses (€)",
        "Seguro (€) total",
        "Coste total (capital+intereses)",
        "Coste total (capital+intereses+seguro)",
        "TAE (%)"
        ],
        "Valor" : [
        len(cuadro_amortización),
        tools.formatear_decimales(total_intereses),
        tools.formatear_decimales(total_seguro),
        tools.formatear_decimales(total_capital_intereses),
        tools.formatear_decimales(total_capital_intereses+total_seguro),
        tools.formatear_decimales(tae)
        ]
        }
    else:
        rcc_resumen = {
        "Concepto" : [
        "Duración (meses)",
        "Intereses (€)",
        "Importe total a pagar (capital+intereses)",
        "TAE (%)"
        ],
        "Valor" : [
        len(cuadro_amortización),
        tools.formatear_decimales(total_intereses),
        tools.formatear_decimales(total_capital_intereses),
        tools.formatear_decimales(tae)
        ]
        }
    rcc_resumen = tools.pd.DataFrame(rcc_resumen).transpose()

    return (tools.pd.DataFrame(cuadro_amortización),
            tools.pd.DataFrame(rcc_resumen))
