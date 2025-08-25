#!
'''Programa para la simulación de los productos amortizables de Cofidis España'''

import math
import pandas as pd 



''' Definir los parámetros básicos para realizar las simulaciones'''

LISTA_PRODUCTOS = ["CREDITO FUSION","Crédito Proyecto","Compra a plazos","Compra a plazos Vorwerk","Compra financiada","COMPRA FINANCIADA VORWERK","AMORTIZABLE OPTION PH IP","AMORTIZABLE OPTION PH IC","CREDITO FINANCIACION AUTO OCASION","CREDITO FINANCIACION MOTO OCASION","CREDITO FINANCIACION AUTO NUEVO","CREDITO FINANCIACION MOTO NUEVO","CREDITO FINANCIACION AUTO OCASION","CREDITO FINANCIACION MOTO OCASION"]
LISTA_SEGURO = ["Seguro ADE", "SIN SEGURO", "VIDA PLUS", "VIDA"]
DIAS_BASE = 360

capital_prestado = 0.00
comision_apertura = 0.00
tasa_comision_apertura = 0.00
imp_max_com_apertura = 0.00
comision_apertura_capitalizada = False
etiqueta_producto = ""
fechas_bloqueo = pd.read_csv('COFES_Date_Blocage.csv', sep=';', parse_dates=['Fecha_BLOQUEO'], dayfirst=True)

    

''' Crear las funciones necesarias para la simulación '''

def calcular_comision_apertura(capital_prestado, tasa_comision_apertura, imp_max_com_apertura):
    '''Calcular la comisión de apertura en base al capital prestado y el porcentaje definido'''
    comision_apertura = round(capital_prestado * tasa_comision_apertura / 100, 2)
    if comision_apertura > imp_max_com_apertura and imp_max_com_apertura > 0:
        '''Comprobar que la comisión calculada no supera el límite marcado; si fuese el caso, actualizamos el valor de la comisión con el límite'''
        comision_apertura = imp_max_com_apertura
    return comision_apertura

def obtener_tasa_seguro_ADE(seguro_titular_1, seguro_titular_2):
    if seguro_titular_1 == "Seguro ADE" and seguro_titular_2 == "Seguro ADE":
        tasa_ADE = 7.68
    elif seguro_titular_1 == "Seguro ADE" or seguro_titular_2 == "Seguro ADE":
        tasa_ADE = 4.44
    else:
        tasa_ADE = 0.00
    return tasa_ADE

def obtener_tasa_seguro_AUTO(plazo, tipo_seguro):
    # Cada tupla: (plazo_máximo, tasa_vida_plus, tasa_otro)
    rangos = [
        (24, 0.04760, 0.01410),
        (36, 0.05550, 0.02200),
        (48, 0.06350, 0.03000),
        (60, 0.06910, 0.03560),
        (72, 0.07820, 0.04470),
        (84, 0.08820, 0.05470),
        (96, 0.09920, 0.06570),
        (108, 0.11100, 0.07750),
        (float('inf'), 0.12410, 0.09060)
    ]
    for max_plazo, tasa_plus, tasa_otro in rangos:
        if plazo < max_plazo + 1:
            return tasa_plus if tipo_seguro == "VIDA PLUS" else tasa_otro
    return 0.0

def calcular_seguro_capitalizado(etiqueta_producto, capital_prestado, plazo, seguro_titular_1, seguro_titular_2, comision):
    '''Calcular el seguro de vida en base al capital prestado, el tipo de seguro, el número de personas aseguradas y la duración del préstamo'''
    capital_prestado += comision #Incrementar la base de cálculo del seguro con la comisión de apertura capitalizada
    if LISTA_PRODUCTOS.index(etiqueta_producto) > 7 and (seguro_titular_1 != "SIN SEGURO" or seguro_titular_2 != "SIN SEGURO"):
        if seguro_titular_1 != "SIN SEGURO":
            tasa_titular_1 = obtener_tasa_seguro_AUTO(plazo, seguro_titular_1)
        else:
            tasa_titular_1 = 0.00
        if seguro_titular_2 != "SIN SEGURO":
            tasa_titular_2 = obtener_tasa_seguro_AUTO(plazo, seguro_titular_2)
        else:
            tasa_titular_2 = 0.00
        seguro_capitalizado = round(capital_prestado * tasa_titular_1, 2) + round(capital_prestado * tasa_titular_2, 2)
    else:
        seguro_capitalizado = 0.00
    return seguro_capitalizado

def calcular_mensualidad_estandar(etiqueta_producto, capital_prestado, plazo, carencia, tasa, comision_apertura, comision_apertura_capitalizada, seguro_capitalizado, seguro_titular_1, seguro_titular_2, tasa_2SEC, capital_2SEC, plazo_2SEC):
    if 3 < LISTA_PRODUCTOS.index(etiqueta_producto) < 7:
        tasa = 0.00
    tasa += obtener_tasa_seguro_ADE(seguro_titular_1, seguro_titular_2)
    
    if comision_apertura_capitalizada:
        '''Incrementar el capital prestado con la comisión de apertura si el préstamo cobra de esta fornma la comisión (comision_apertura_capitalizada=True)'''
        capital_prestado += comision_apertura + seguro_capitalizado
    else:
        capital_prestado += seguro_capitalizado
    
    if carencia > 0:
        '''Incremantar el capital de la operación con el interés y seguro capitalizado al finalizar carencia'''
        capital_prestado += round((capital_prestado * tasa / 1200),2) * carencia
    
    '''Calcular la mensualidad contractual del préstamo rendondeando al céntimo superior para asegurar la ventilación de todo el capital'''
    if tasa == 0.00:
        cuota_1SEC = math.ceil((capital_prestado - capital_2SEC) / plazo * 100) / 100
    else:
        cuota_1SEC = math.ceil(capital_2SEC * tasa / 1200 * 100) / 100 + math.ceil((capital_prestado - capital_2SEC) * tasa / 1200 * ((1 + (tasa / 1200)) ** plazo) / (((1 + (tasa / 1200)) ** plazo) - 1) * 100 ) / 100
    if capital_2SEC != 0.00:
        if tasa_2SEC == 0.00:
            cuota_2SEC = math.ceil(capital_2SEC / plazo_2SEC * 100) / 100
        else:
            cuota_2SEC = math.ceil(capital_2SEC * tasa_2SEC / 1200 * ((1 + (tasa_2SEC / 1200)) ** plazo_2SEC) / (((1 + (tasa_2SEC / 1200)) ** plazo_2SEC) - 1) * 100 ) / 100
    else:
        cuota_2SEC = 0.00
    return cuota_1SEC, cuota_2SEC











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

