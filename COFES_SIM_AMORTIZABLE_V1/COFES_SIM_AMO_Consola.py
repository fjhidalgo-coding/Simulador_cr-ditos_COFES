#!
'''Programa para la simulación de los productos amortizables de Cofidis España'''

''' Definir los parámetros básicos para realizar las simulaciones'''

LISTA_PRODUCTOS = ["CREDITO FUSION","Crédito Proyecto","Compra a plazos","Compra a plazos Vorwerk","Compra financiada","COMPRA FINANCIADA VORWERK","AMORTIZABLE OPTION PH IP","AMORTIZABLE OPTION PH IC","CREDITO FINANCIACION AUTO OCASION","CREDITO FINANCIACION MOTO OCASION","CREDITO FINANCIACION AUTO NUEVO","CREDITO FINANCIACION MOTO NUEVO","CREDITO FINANCIACION AUTO OCASION","CREDITO FINANCIACION MOTO OCASION"]
LISTA_SEGURO = ["Seguro ADE", "SIN SEGURO", "VIDA PLUS", "VIDA"]
DIAS_BASE = 360

capital_prestado = 0.00
comision_apertura = 0.00
tasa_comision_apertura = 0.00
imp_max_com_apertura = 0.00
comision_apertura_capitalizada = False
    

''' Crear las funciones necesarias para la simulación '''

def calcular_comision_apertura(capital_prestado, tasa_comision_apertura, imp_max_com_apertura):
    '''Calcular la comisión de apertura en base al capital prestado y el porcentaje definido'''
    comision_apertura = round(capital_prestado * tasa_comision_apertura / 100, 2)
        
    if comision_apertura > imp_max_com_apertura and imp_max_com_apertura > 0:
        '''Comprobar que la comisión calculada no supera el límite marcado; si fuese el caso, actualizamos el valor de la comisión con el límite'''
        comision_apertura = imp_max_com_apertura
    
    return comision_apertura

def calcular_mensualidad_estandar(tasa,capital_prestado, plazo, carencia, producto, comision_apertura):
    if comision_apertura_capitalizada:
        '''Incrementar el capital prestado con la comisión de apertura si el préstamo cobra de esta fornma la comisión (comision_apertura_capitalizada=True)'''
        capital_prestado += comision_apertura
    
    if carencia > 0:
        '''Incremantar el capital de la operación con el interés y seguro capitalizado al finalizar carencia'''
        capital_prestado += round((capital_prestado * tasa / 12),2) * carencia
    
    '''Calcular la mensualidad contractual del préstamo rendondeando al céntimo superior para asegurar la ventilación de todo el capital'''
    cuota_1SEC = capital_prestado
    #cuota=npf.pmt(tasa, plazo,-capital_prestado, 0)
    print(cuota_1SEC)                                                                                                              # A suprimir en versión definitiva



''' Iniciar la simulación de préstamo'''

comision_apertura= calcular_comision_apertura(capital_prestado, tasa_comision_apertura, imp_max_com_apertura)

#df=calcular_mensualidad_estandar(tasa,capital_prestado, plazo, carencia, producto, comision_apertura)
















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

