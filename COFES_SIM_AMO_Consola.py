#!
'''
Programa para la simulación de los productos amortizables de Cofidis España creado a partir de:

    Cristian Camilo Moreno Narvaez
    https://ccamilocristian.github.io/posts/liquidador-intereses/

'''

import datetime as dt

#import numpy as np
#import pandas as pd
#import numpy_financial as npf
#import matplotlib.pyplot as plt



''' Definir las características de los productos ''' 

PRODUCTOS = [
{"id":  1, "Producto POPS": "B 2141650000", "Familia de producto": "Directo Rachat","Interés cliente": True,  "Producto con dos secuencias": False,"Carencia forzada": False, "Carencia gratuita": False, "Mínimo entre financiación y vencimiento": 14, "Asegurable": 1, "Tipo de seguro": [{id:1, "Etiqueta": "Seguro ADE"}],"Etiqueta": "CREDITO FUSION"},
{"id":  2, "Producto POPS": "B 2150850001", "Familia de producto": "Directo","Interés cliente": True,  "Producto con dos secuencias": False,"Carencia forzada": False, "Carencia gratuita": True , "Mínimo entre financiación y vencimiento": 14, "Asegurable": 1, "Tipo de seguro": [{id:1, "Etiqueta": "Seguro ADE"}],"Etiqueta": "Crédito Proyecto"},
{"id":  3, "Producto POPS": "B 2460050000", "Familia de producto": "PdV","Interés cliente": True,  "Producto con dos secuencias": False,"Carencia forzada": False, "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 0, "Tipo de seguro": None, "Etiqueta": "Compra a plazos"},
{"id":  4, "Producto POPS": "B 2460050001", "Familia de producto": "PdV","Interés cliente": True,  "Producto con dos secuencias": False,"Carencia forzada": True,  "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 0, "Tipo de seguro": None, "Etiqueta": "Compra a plazos Vorwerk"},
{"id":  5, "Producto POPS": "B 2460050002", "Familia de producto": "PdV sin interés cliente","Interés cliente": False, "Producto con dos secuencias": False,"Carencia forzada": False, "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 0, "Tipo de seguro": None, "Etiqueta": "Compra financiada"},
{"id":  6, "Producto POPS": "B 2460050003", "Familia de producto": "PdV sin interés cliente","Interés cliente": False, "Producto con dos secuencias": False,"Carencia forzada": True,  "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 0, "Tipo de seguro": None, "Etiqueta": "COMPRA FINANCIADA VORWERK"},
{"id":  7, "Producto POPS": "B 2460050004", "Familia de producto": "OPTION+","Interés cliente": False, "Producto con dos secuencias": True, "Carencia forzada": False, "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 0, "Tipo de seguro": None, "Etiqueta": "AMORTIZABLE OPTION PH IP"},
{"id":  8, "Producto POPS": "B 2460050005", "Familia de producto": "OPTION+","Interés cliente": True,  "Producto con dos secuencias": True, "Carencia forzada": False, "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 0, "Tipo de seguro": None, "Etiqueta": "AMORTIZABLE OPTION PH IC"},
{"id":  9, "Producto POPS": "B 2460050006", "Familia de producto": "AUTO","Interés cliente": True,  "Producto con dos secuencias": False,"Carencia forzada": False, "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 1, "Tipo de seguro": [{id:2, "Etiqueta": "VIDA PLUS"},{id:3, "Etiqueta": "VIDA"}], "Etiqueta": "CREDITO FINANCIACION AUTO OCASION"},
{"id": 10, "Producto POPS": "B 2460050007", "Familia de producto": "AUTO","Interés cliente": True,  "Producto con dos secuencias": False,"Carencia forzada": False, "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 1, "Tipo de seguro": [{id:2, "Etiqueta": "VIDA PLUS"},{id:3, "Etiqueta": "VIDA"}], "Etiqueta": "CREDITO FINANCIACION MOTO OCASION"},
{"id": 11, "Producto POPS": "B 2460050008", "Familia de producto": "AUTO","Interés cliente": True,  "Producto con dos secuencias": False,"Carencia forzada": False, "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 1, "Tipo de seguro": [{id:2, "Etiqueta": "VIDA PLUS"},{id:3, "Etiqueta": "VIDA"}], "Etiqueta": "CREDITO FINANCIACION AUTO NUEVO"},
{"id": 12, "Producto POPS": "B 2460050009", "Familia de producto": "AUTO","Interés cliente": True,  "Producto con dos secuencias": False,"Carencia forzada": False, "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 1, "Tipo de seguro": [{id:2, "Etiqueta": "VIDA PLUS"},{id:3, "Etiqueta": "VIDA"}], "Etiqueta": "CREDITO FINANCIACION MOTO NUEVO"},
{"id": 13, "Producto POPS": "B 2460050066", "Familia de producto": "AUTO","Interés cliente": True,  "Producto con dos secuencias": False,"Carencia forzada": False, "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 1, "Tipo de seguro": [{id:2, "Etiqueta": "VIDA PLUS"},{id:3, "Etiqueta": "VIDA"}], "Etiqueta": "CREDITO FINANCIACION AUTO OCASION"},
{"id": 14, "Producto POPS": "B 2460050067", "Familia de producto": "AUTO","Interés cliente": True,  "Producto con dos secuencias": False,"Carencia forzada": False, "Carencia gratuita": False, "Mínimo entre financiación y vencimiento":  0, "Asegurable": 1, "Tipo de seguro": [{id:2, "Etiqueta": "VIDA PLUS"},{id:3, "Etiqueta": "VIDA"}], "Etiqueta": "CREDITO FINANCIACION MOTO OCASION"}
]



''' Definir los parámetros básicos para realizar las simulaciones'''

DIAS_BASE = 360
D_PAGO_DEFECTO = 2
DIAS_VENCIMIENTO = list(range(1,13))
CURRENT_DATE = dt.date.today()




''' Definir la variables de trabajo de la simulación '''

producto = PRODUCTOS[0]                          # Pendiente buscar cómo recuperar los productos con un desplegable o similar en Streamlit                  
capital_prestado= int(50000)
carencia=2
plazo=18
tasa=0.133
tasa_comision_apertura=0.03
imp_max_com_apertura= int(950)
comision_apertura_capitalizada=True
seguro_titular_1 = 1
seguro_titular_2 = 1
fecha_financiacion = CURRENT_DATE
#cuota_inicial=0

print(fecha_financiacion)

''' Creamos las funciones necesarias para la simulación '''

def calcular_comision_apertura(capital_prestado, tasa_comision_apertura, imp_max_com_apertura):
    '''Calculamos la comisión de apertura en base al capital prestado y el porcentaje definido'''
    comision_apertura = round(capital_prestado * tasa_comision_apertura,2)
        
    if comision_apertura > imp_max_com_apertura and imp_max_com_apertura > 0:
        '''Comprobamos que la comisión calculada no supera el límite marcado; si fuese el caso, actualizamos el valor de la comisión con el límite'''
        comision_apertura = imp_max_com_apertura
    
    return comision_apertura

def calcular_mensualidad_estandar(tasa,capital_prestado, plazo, carencia, producto, comision_apertura):
    if comision_apertura_capitalizada:
        '''Incrementamos el capital prestado con la comisión de apertura si el préstamo cobra de esta fornma la comisión (comision_apertura_capitalizada=True)'''
        capital_prestado += comision_apertura
    
    if carencia > 0:
        '''Incremantamos el capital de la operación con el interés y seguro capitalizado al finalizar carencia'''
        capital_prestado += round((capital_prestado * tasa / 12),2) * carencia
    
    '''Calculamos la mensualidad contractual del préstamo rendondeando al céntimo superior para asegurar la ventilación de todo el capital'''
    cuota_1SEC = capital_prestado
    #cuota=npf.pmt(tasa, plazo,-capital_prestado, 0)
    print(cuota_1SEC)                                                                                                              # A suprimir en versión definitiva



''' Iniciar la simulación de préstamo'''

comision_apertura= calcular_comision_apertura(capital_prestado, tasa_comision_apertura, imp_max_com_apertura)

df=calcular_mensualidad_estandar(tasa,capital_prestado, plazo, carencia, producto, comision_apertura)

















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

