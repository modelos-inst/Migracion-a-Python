#Script donde se llevaran a cabo todas las funciones

#Librerías que vamos a utilizar
## Recuerde hacer pip install en el cmd si no ha instalado alguna de ellas
import pandas as pd
import numpy as np

from scipy.stats import poisson
from jmarkov.dtmc import dtmc

#Crear la función que realice los procedimientos necesarios.
#En este caso se busca crear los objetos cadenas de markov para ambas políticas, realizar el análisis transitorio para las 10 semanas y obtener los respectivos costos
def Shiny_function(tasa):
    
    #Crear los estados
    estados = range(23)

    #*****Crear y llenar la matriz P de la política actual*****
    matrizP = np.zeros((len(estados), len(estados)), dtype = float)

    #Para la Política Actual -> si i<=10 solicita 12 resmas
    for i in estados:
        for j in estados:
            if i<=10 and j>0:
                matrizP[i,j] = poisson.pmf(12+i-j, tasa) #poisson.pmf calcula P(D=k)
            elif i<=10 and j==0:
                matrizP[i,j] = poisson.sf(12+i-1, tasa) #poisson.smf calcula P(D>k). Por esto es necesario restar 1 unidad.
            elif i>10 and j>0:
                matrizP[i,j] = poisson.pmf(i-j, tasa)
            elif i>10 and j==0:
                matrizP[i,j] = poisson.sf(i-1, tasa)

    
    #*****Crear y llenar la matriz P para el caso de la Política Nueva*****
    matrizPNueva = np.zeros((len(estados), len(estados)), dtype = float)
    
    #Para la nueva Política  -> solicitar hasta la capacidad máxima
    for i in estados:
        for j in estados:
            if j>0:
               matrizPNueva[i,j] = poisson.pmf(22-j, tasa)
            elif j==0:
                matrizPNueva[i,j]=poisson.sf(21, tasa)

    #*****Crear las dos cadenas usando el paquete jmarkov*****
    #Política Actual
    politica_Actual = dtmc(matrizP)
    #Política Nueva
    politica_Nueva = dtmc(matrizPNueva)

    #Valor de los costos de inventario y de ordenar
    cInventario = 6200
    cOrdenar = 38000

    #******Estimar los costos para las próximas 10 semanas
    #Definir vector de estado inicial dado que al final de esta semana quedaron cero unidades en inventario
    alfa = np.zeros(len(estados))
    alfa[0] = 1

    #calcula el vector de costos de la política actual 
    cost_Sem_Pactual = []
    #Calcula el costo de inventario y el costo de ordenar promedio de la política actual
    cost_inv_Pactual = []
    cost_ord_Pactual = []

    for i in range(1,11):
        probs = politica_Actual.transient_probabilities(n = i, alpha=alfa)

        print(cInventario * np.dot(probs, estados))
        cost_inv_Pactual.append(cInventario * np.dot(probs, estados))
        cost_ord_Pactual.append(cOrdenar*sum(probs[0:10]))

    print(cost_inv_Pactual)
    print(cost_ord_Pactual)
    cost_Sem_Pactual = np.add(cost_inv_Pactual, cost_ord_Pactual)

    #calcula el vector de costos de la política nueva
    cost_Sem_Pnueva = []
    #Calcula el costo de inventario y el costo de ordenar promedio de la política nueva
    cost_inv_Pnueva = []
    cost_ord_Pnueva = [] 
    for i in range(1,11):
        probs = politica_Nueva.transient_probabilities(n = i, alpha=alfa)
        
        cost_inv_Pnueva.append(cInventario * np.dot(probs, estados))
        cost_ord_Pnueva.append(cOrdenar*sum(probs[0:21]))
    
    cost_Sem_Pnueva = np.add(cost_inv_Pnueva, cost_ord_Pnueva)

    #vector de numero de semana
    num_sem = range(1,11)
    data = pd.DataFrame({
        'numero_semana': num_sem,
        'costo_semanal_PolActual': cost_Sem_Pactual,
        'costo_semanal_PolNueva': cost_Sem_Pnueva
    })

    return data