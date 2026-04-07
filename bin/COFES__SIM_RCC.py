#!
'''Programa para la simulación de los productos amortizables de COF_ES'''

import bin.COFES___TAE as tools_tae
import bin.COFES___tools as tools



tools.getcontext().prec = 10

# ---------------------------------------------------------
# FUNCIONES AUXILIARES
# ---------------------------------------------------------

def primer_recibo(fecha_financiacion):
    if fecha_financiacion.day < 2:
        return fecha_financiacion.replace(day=2)
    if fecha_financiacion.month == 12:
        return tools.dt.date(fecha_financiacion.year + 1, 1, 2)
    return tools.dt.date(fecha_financiacion.year, fecha_financiacion.month + 1, 2)

def siguiente_recibo(fecha):
    if fecha.month == 12:
        return tools.dt.date(fecha.year + 1, 1, 2)
    return tools.dt.date(fecha.year, fecha.month + 1, 2)

def rcc_obtener_duraciones(capital, tin, fecha_financiacion):
    rcc_duraciones = []
    rcc_cuotas = {}
    for v in tools.RCC_OPCIONES_VITESSE:
        cuota_test = round(capital*v/100,2)
        cuadro_amortización = simulador(capital,tin,cuota_test,fecha_financiacion,0)
        meses = len(cuadro_amortización)
        etiqueta = f"{meses} meses"
        rcc_duraciones.append(etiqueta)
        rcc_cuotas[etiqueta] = cuota_test
    
    return rcc_duraciones, rcc_cuotas    

# ---------------------------------------------------------
# CALCULO INTERESES
# ---------------------------------------------------------

def interes_preciso(capital, tin, fecha_financiacion, fecha_fin):

    capital = tools.Decimal(str(capital))
    tin = tools.Decimal(str(tin)) / tools.Decimal("100")

    fecha_financiacion = tools.pd.to_datetime(fecha_financiacion).date()
    fecha_fin = tools.pd.to_datetime(fecha_fin).date()

    interes_diciembre = tools.Decimal("0")
    interes_enero = tools.Decimal("0")

    if fecha_fin.month == 1 and fecha_financiacion.year < fecha_fin.year:

        year_prev = fecha_financiacion.year
        year_curr = fecha_fin.year

        bisiesto_prev = tools.cl.isleap(year_prev)
        bisiesto_curr = tools.cl.isleap(year_curr)

        if bisiesto_prev != bisiesto_curr:

            dias_dic = 29
            base_dic = 366 if bisiesto_prev else 365

            interes_diciembre = (
                capital * tin * tools.Decimal(dias_dic) / tools.Decimal(base_dic)
            ).quantize(tools.Decimal("0.00001"))

            dias_ene = (fecha_fin - tools.dt.date(year_curr,1,1)).days + 1
            base_ene = 366 if bisiesto_curr else 365

            interes_enero = (
                capital * tin * tools.Decimal(dias_ene) / tools.Decimal(base_ene)
            ).quantize(tools.Decimal("0.00001"))

            interes_total = (interes_diciembre + interes_enero).quantize(tools.Decimal("0.00001"))

            return interes_total, interes_diciembre, interes_enero

    dias_tramo = (fecha_fin - fecha_financiacion).days
    base = tools.dias_año(fecha_financiacion)

    interes_total = (
        capital * tin * tools.Decimal(dias_tramo) / tools.Decimal(base)
    ).quantize(tools.Decimal("0.00001"))

    return interes_total, tools.Decimal("0"), interes_total

# ---------------------------------------------------------
# SIMULADOR
# ---------------------------------------------------------

def simulador(capital, tin, cuota, fecha_financiacion, seguro_tasa=0):

    capital = tools.Decimal(str(capital))
    cuota = tools.Decimal(str(cuota))
    saldo = capital
    seguro_tasa = tools.Decimal(str(seguro_tasa))
    
    fecha_pago = primer_recibo(fecha_financiacion)
    fecha_anterior = fecha_financiacion

    cuadro_amortización = []
    mes = 1

    while saldo > 0:

        interes_total, interes_dic, interes_ene = interes_preciso(
            saldo, tin, fecha_anterior, fecha_pago
        )

        interes_total = interes_total.quantize(tools.Decimal("0.01"), tools.ROUND_HALF_UP)

        seguro = ((saldo + interes_total) * seguro_tasa).quantize(tools.Decimal("0.01"), tools.ROUND_HALF_UP)

        if saldo + interes_total <= cuota:

            amort = saldo.quantize(tools.Decimal("0.01"), tools.ROUND_HALF_UP)
            saldo = tools.Decimal("0")

            cuota_final = (amort + interes_total).quantize(tools.Decimal("0.01"), tools.ROUND_HALF_UP)

        else:

            amort = (cuota - interes_total).quantize(tools.Decimal("0.01"), tools.ROUND_HALF_UP)
            saldo = (saldo - amort).quantize(tools.Decimal("0.01"), tools.ROUND_HALF_UP)

            cuota_final = cuota

        cuadro_amortización.append({
            "Mes": mes,
            "Fecha recibo": fecha_pago,
            "Capital pendiente (€)": float(saldo + amort),
            "Cuota (€)": float(cuota_final),
            "Intereses diciembre (€)": float(interes_dic),
            "Intereses enero (€)": float(interes_ene),
            "Intereses total (€)": float(interes_total),
            "Amortización (€)": float(amort),
            "Saldo (€)": float(saldo),
            "Seguro (€)": float(seguro),
            "Recibo total (€)": float(cuota_final + seguro)
        })

        fecha_anterior = fecha_pago
        fecha_pago = siguiente_recibo(fecha_pago)

        mes += 1

        if mes > 600:
            break
    
    return tools.pd.DataFrame(cuadro_amortización)


def rcc_simulacion_completa(capital, tin, cuota, fecha_financiacion, seguro_tasa=0):
    cuadro_amortización = simulador(capital, tin, cuota, fecha_financiacion, seguro_tasa)
    # Quitar columna seguro si no hay seguro
    if seguro_tasa == 0 and "Seguro (€)" in cuadro_amortización.columns:
        cuadro_amortización = cuadro_amortización.drop(columns=["Seguro (€)"])

    total_intereses = round(cuadro_amortización["Intereses total (€)"].sum(),2)
    total_capital_intereses = round(cuadro_amortización["Cuota (€)"].sum(),2)

    if seguro_tasa > 0:
        total_seguro = round(cuadro_amortización["Seguro (€)"].sum(),2)

    cuotas_tae = [-capital]+list(cuadro_amortización["Cuota (€)"])
    fechas_tae = [fecha_financiacion]+list(cuadro_amortización["Fecha recibo"])

    tae = calcular_tae(cuotas_tae,fechas_tae)
    
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
        total_intereses,
        total_seguro,
        total_capital_intereses,
        round(total_capital_intereses+total_seguro,2),
        tae
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

    return tools.pd.DataFrame(cuadro_amortización), tools.pd.DataFrame(rcc_resumen)

# ---------------------------------------------------------
# CALCULO TAE
# ---------------------------------------------------------

def calcular_tae(cuotas, fechas):

    tiempos=[tools.Decimal("0.0")]

    for i in range(1,len(fechas)):
        f0=tools.pd.to_datetime(fechas[i-1]).date()
        f1=tools.pd.to_datetime(fechas[i]).date()

        fraccion=(f1-f0).days/tools.dias_año(f0)
        tiempos.append(tiempos[-1] + tools.Decimal(fraccion))

    def van(tasa):
        return sum(tools.Decimal(c)/((1+tools.Decimal(tasa))**t) for c,t in zip(cuotas,tiempos))

    minimo=-0.9999
    maximo=10

    for _ in range(1000):

        medio=(minimo+maximo)/2
        valor=van(medio)

        if abs(valor)<1e-10:
            return round(medio*100,2)

        if valor>0:
            minimo=medio
        else:
            maximo=medio

    return round(medio*100,2)

