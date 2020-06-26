# -*- coding: utf-8 -*-

#Librerías a usar:
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from numpy import linspace
import pandas as pd
from scipy.optimize import curve_fit
from pylab import plot,show,title

#Primero, se ingresan los datos de los dos csv a dataframes de pandas:
xy = pd.read_csv("xy.csv",index_col = 0)
xyp = pd.read_csv("xyp.csv")

#Se convierten los datos del dataframe a numpy, por facilidad de algunos cálculos:
xy_np = xy.to_numpy(dtype=None, copy=False) 
xyp_np = xyp.to_numpy(dtype=None, copy=False) 

#Se encuentran los datos para las funciones de densidad marginales de cada variable:
datos_margin_x = np.sum(xy_np,axis=1)
datos_margin_y = np.sum(xy_np,axis=0)

#Se crean los ejes x para las gráficas que se harán:
eje_x1 = linspace(5,15,100) #Este es de 100 valores, para visualizar los modelos
eje_x2 = linspace(5,15,11) #Este tiene la cantidad de números exacta para los datos que se tienen.

eje_y1 = linspace(5,25,100)
eje_y2 = linspace(5,25,21)


#Se grafican los datos discretos para observar con qué deben modelarse las funciones de densidad marginales de X y Y:
plot(eje_x2, datos_margin_x,'g-')
plt.plot(eje_x2, datos_margin_x, 'o', color='black');
title('Datos discretos para la función de densidad marginal de "X"')
plt.xlabel('x')
plt.ylabel('fx(x)')
show()

plot(eje_y2, datos_margin_y,'g-')
plt.plot(eje_y2, datos_margin_y, 'o', color='black');
title('Datos discretos para la función de densidad marginal de "Y"')
plt.xlabel('y')
plt.ylabel('fy(y)')
show()


#Tras decidir modelar los datos con una función normal o gaussiana, se define dicha función y sus parámetros mu (media) y sigma (desviación estándar)
def normal(x,mu,sigma):
    return (1/np.sqrt(2*np.pi*sigma**2))*np.exp(-(x-mu)**2/(2*sigma**2))

#Se encuentran los parámetros que ajustan las curvas a los datos tanto de "x" como de "y" con ayuda de curve_fit:

paramx, _ = curve_fit(normal,eje_x2,datos_margin_x)
curva = normal(eje_x1,paramx[0],paramx[1])


paramy, _ = curve_fit(normal,eje_y2,datos_margin_y)
curvay = normal(eje_y1,paramy[0],paramy[1])

#Se imprimen los valores de los parámetros obtenidos, para visualizarlos e incluirlos en el trabajo escrito:
print("Mu x:",paramx[0],"\n Sigma x:",paramx[1],"\n Mu y:",paramy[0],"\n Sigma y:",paramy[1])


#Se grafican los modelos obtenidos, junto a los datos reales: 
plot(eje_x1,curva,'b-')
plot(eje_x2, datos_margin_x,'g-')
plt.plot(eje_x2, datos_margin_x, 'o', color='black');
title('Modelo gaussiano para la función marginal de "X" (azul) junto a los datos')
plt.xlabel('x')
plt.ylabel('fx(x)')
show()


plot(eje_y1, curvay,'b-')
plot(eje_y2, datos_margin_y,'g-')
plt.plot(eje_y2, datos_margin_y, 'o', color='black');
title('Modelo gaussiano para la para la función marginal de "Y" (azul) junto a los datos')
plt.xlabel('y')
plt.ylabel('fy(y)')
show()

#Se define la función de densidad conjunta, sabiendo que las variables en cuestión son independientes:
def normal_conjunta(x,mux,sigmax,y,muy,sigmay):
    return normal(x, mux,sigmax)*normal(y, muy,sigmay)

#Se grafica en 3D la función de densidad conjunta:
X, Y = np.meshgrid(eje_x1, eje_y1)
conjunta = normal_conjunta(X,paramx[0],paramx[1], Y,paramy[0],paramy[1])
ax = plt.axes(projection="3d")
ax.plot_surface(X, Y, conjunta, rstride=1, cstride=1, cmap='viridis', edgecolor='none')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('fx,y(x,y)')
ax.set_title('Función de densidad conjunta que modela los datos')
plt.show()

"""
Hallar los valores de correlación, covarianza y coeficiente de correlación (Pearson) para los datos y explicar su significado.
"""
#Encontrando el valor de la correlación a partir del los datos del archivo xyp:
#Se inicializa una variable como cero para poder realizar la sumatoria de valores en ella.
correlacion=0
for i in range(len(xyp)):
    #Como se trabaja con valores discretos, es necesario sumar la multiplicación de tres cosas:
    #1: El valor de X. 2: El valor de Y. 3: El valor de probabilidad de X,Y
    #Se realiza un recorrido por cada fila del archivo xyp, y se van sumando los valores hasta terminar de recorrer el archivo.
    correlacion+= xyp.iloc[i][0]*xyp.iloc[i][1]*xyp.iloc[i][2] 
    
    
#Visualización de la correlación, y de la multiplicación de (Mu x)*(Mu y)
print("\nCorrelación:", correlacion)    
print("\nMultiplicación de E[X] con E[Y]", paramx[0]*paramy[0])


#Nuevamente, se inicializa la variable de covarianza en 0.
covarianza = 0

for i in range(len(xyp)):
    #La covarianza se clacula con suma de la multiplicación de tres cosas:
    #1: el valor de x menos la media de X. 2: El valor de y menos la media de Y. 3: La probabilidad en ese punto.
    #Al ifual que con la correlación, se recorren todos los datos xyp que contienen los 3 datos necesarios para calcular este momento.
    covarianza += (xyp.iloc[i][0]-paramx[0])*(xyp.iloc[i][1]-paramy[0])*xyp.iloc[i][2] 

#Visualización de la covarianza obtenida
print("\nCovarianza:",covarianza,"\n")         

#Se calcula el coeficiente de correlación según la fórmula vista en clase:
coef_correlacion = covarianza/(paramy[1]*paramx[1])

#Visualización del coeficiente de correlación:
print("Coeficiente de correlación:",coef_correlacion)