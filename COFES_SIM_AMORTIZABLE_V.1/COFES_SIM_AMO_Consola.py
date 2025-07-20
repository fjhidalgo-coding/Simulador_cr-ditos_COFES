#!
'''
Programa para la simulación de los productos amortizables de Cofidis España creado a partir de:

    Cristian Camilo Moreno Narvaez
    https://ccamilocristian.github.io/posts/liquidador-intereses/

'''

import numpy as np
import pandas as pd
import numpy_financial as npf
import matplotlib.pyplot as plt


tasa=0.0109
importe_a_financiar=500000
plazo=18
cuota_inicial=0

# Función cuota_fija para realizar la simulación de crédito

def cuota_fija(tasa,importe_a_financiar, plazo, cuota_inicial ):
    '''
    La función cuota_fija permite generar la simulación de un cuadro de amortización a partir de las variables de entrada:
    tasa                : Contiene el tipo de interés solicitado al usuario
    importe_a_financiar : Contiene el capital inicial del préstamos solicitado al cliente
    plazo               : Contiene la duración inicial del crédito 
    cuota_inicial       : Contiene la mensualidad al inicio de la simulación
    '''
    
    base_liquidador=pd.DataFrame([])
    cuota=npf.pmt(tasa, plazo,-importe_a_financiar, 0)
    cuotas_iniciales=int(input("Ingrese el valor: "))
    if cuotas_iniciales==1:
        base_liquidador=pd.DataFrame([])
        base_liquidador['Mes_cuota']=["Mes_%s"%(i+1) for i in range(plazo+1)]
        base_liquidador['Saldo']=0
        base_liquidador['Intereses']=0
        base_liquidador['Saldo'][0]=importe_a_financiar
        base_liquidador['Saldo'][1]=importe_a_financiar-cuota_inicial 
        
        base_liquidador['pago_mes']=int(cuota)
        base_liquidador['pago_mes'][0]=cuota_inicial
        base_liquidador['amortización']=0
        base_liquidador['amortización'][0]=cuota_inicial
        base_liquidador['tasa_interes']=tasa
        base_liquidador['Saldo_final']=0

        for i in range(0, len(base_liquidador)):
            base_liquidador['Intereses'][i+1]=(base_liquidador['Saldo'][i]*base_liquidador['tasa_interes'][i])
            base_liquidador['amortización'][i]=np.where(base_liquidador['Saldo'][i]>base_liquidador['Intereses'][i],(base_liquidador['pago_mes'][i]-base_liquidador['Intereses'][i]),base_liquidador['Saldo'][i] )
            base_liquidador['Saldo'][i+1]=base_liquidador['Saldo'][i]-base_liquidador['amortización'][i]
            base_liquidador['pago_mes'][i]=np.where(base_liquidador['Saldo'][i]>base_liquidador['amortización'][i], base_liquidador['pago_mes'][i], base_liquidador['Saldo'][i])
            base_liquidador['Saldo_final'][i]=base_liquidador['Saldo'][i]-base_liquidador['amortización'][i] 

    elif cuotas_iniciales==0:
        base_liquidador=pd.DataFrame([])
        base_liquidador['Mes_cuota']=["Mes_%s"%(i+1) for i in range(plazo)]
        base_liquidador['Saldo']=0
        base_liquidador['Saldo'][0]=importe_a_financiar
        base_liquidador['Intereses']=0
        base_liquidador['pago_mes']=int(cuota)
        base_liquidador['amortización']=0
        base_liquidador['tasa_interes']=tasa
        base_liquidador['Saldo_final']=0
        
        for i in range(0, len(base_liquidador)):
            base_liquidador['Intereses'][i]=(base_liquidador['Saldo'][i]*base_liquidador['tasa_interes'][i])
            base_liquidador['amortización'][i]=np.where(base_liquidador['Saldo'][i]>base_liquidador['Intereses'][i],(base_liquidador['pago_mes'][i]-base_liquidador['Intereses'][i]),base_liquidador['Saldo'][i] )
            base_liquidador['Saldo'][i+1]=base_liquidador['Saldo'][i]-base_liquidador['amortización'][i]
            base_liquidador['Saldo_final'][i]=base_liquidador['Saldo'][i]-base_liquidador['amortización'][i]    
    else: 
        print("Oops!  Este es un valor incorrecto.  Pruebe de nuevo...")    
    return base_liquidador


# Generación del Cuadro de amortización - TAMO - a partir de la salida de la función cuota_fija 

df=cuota_fija(tasa,importe_a_financiar, plazo, cuota_inicial )
print(df)


# Generación del gráfico con la caída de capital e intereses 

plt.figure(figsize=(15,8))
plt.plot(df.Mes_cuota,df.Saldo,label='Saldo')
plt.xlabel('Meses')
plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
plt.title('Saldo de la deuda')
for a,b in zip(df.Mes_cuota,df.Saldo): 
    plt.text(a, b, str(b))
plt.legend()
plt.show()