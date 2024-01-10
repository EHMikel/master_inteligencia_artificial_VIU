# -*- coding: utf-8 -*-
"""
Ejercicios 3:2 DataFrames
"""
import pandas as pd
""" 1. Blance de ventas y gastos
"""
Dicc = {'Mes':['Enero','Febrero','Marzo','Abril','Mayo','Junio'], \
        'Ventas':[27500, 32400, 19900, 24800, 15950, 34200], \
        'Gastos':[20000, 22500, 17400, 21600, 15500, 20200]}
indice = ['r1', 'r2', 'r3', 'r4', 'r5', 'r6']
dfB = pd.DataFrame(Dicc, index = indice)
dfB['Balance'] = dfB['Ventas']-dfB['Gastos']
print(dfB)

"""
2. Datos corporles de personas
"""
# a)
dfC = pd.read_csv('data2.csv')
dfC.index = ['id1','id2','id3','id4']
dfC['IMC'] = dfC['peso']/dfC['altura']**2  # se calcula y añade columna 'IMC'
# b)
J=dfC.loc['id3']
print(J)
# df3.name = ' Datos clínicos '
# df3.index.name ='CodPaciente'
# c)
Med=round(dfC.mean(),2)
print(Med)
# d)
EdadMax=dfC['edad'].max()
print(EdadMax)
# e)
EstDesc=round(dfC.describe(),2)
print(EstDesc)

"""
   3. Gestionar Pensionistas
"""
lst = [['1111A','Carlos',68,640,589,573, 560, 530, 234],
     ['2222D','Lucia',69,710,550,570,698,645,514],
     ['3333J','Paula',72,530,534, 678, 453, 345, 472],
     ['4444N','Luis',75,770,645,630,650,590,483]]
col=['DNI','nombre','edad','Enero','Febrero','Marzo','Abril','Mayo','Junio']
ind = ['p1', 'p2', 'p3', 'p4']
# a)
dfPens = pd.DataFrame(lst, columns = col, index = ind)
print(dfPens)
# b)
GastPro=dfPens[['Enero','Febrero','Marzo','Abril','Mayo','Junio']].mean(axis=1)
print(GastPro)
# c)
GM=GastPro.max()
print(GM)
# d)
ED=dfPens.describe()
print(ED)

"""
 4. Jugadores de futbol. Minutos jugados en últimos 8 partidos
"""
lst_equipo = [['Lionel', 33, 77, 90, 82, 75, 90, 65, 90, 80], \
              ['Ramos', 34, 88, 75, 81, 90, 74, 62], \
              ['Koke',27, 78, 89, 85, 76, 90, 65, 81, 90], \
              ['Saul', 24, 90, 90, 90, 90, 90, 90, 90], \
              ['Joao', 25, 24, 22, 45, 20, 25, 90, 60], \
              ['Odriozola', 25, 70, 45, 90, 75, 80], \
              ['Lenglet', 23, 45, 55, 50], \
              ['Pique', 33, 90, 90, 90, 90, 90, 90, 90, 90], \
              ['Araujo', 21, 28, 15, 45, 18, 25, 33], \
              ['Valverde', 22, 45, 55, 33, 40], \
              ['Rosales', 30, 75], \
              ['Piatti', 40, 80, 31, 40, 20]]
colF=['nombre','edad','P1','P2','P3','P4','P5','P6','P7','P8']
# a)
dfFut = pd.DataFrame(lst_equipo, columns = colF)
# b)
Nom = dfFut['nombre']
MJsum = dfFut[['P1','P2','P3','P4','P5','P6','P7','P8']].sum(axis=1)
MJmean = dfFut[['P1','P2','P3','P4','P5','P6','P7','P8']].mean(axis=1)
# c)
d = {'Nombre': Nom, 'Suma minutos': MJsum, 'Media minutos': MJmean}
dfRes = pd.DataFrame(d)
print(dfRes)

""" 5. Vinos. Diccionario a DataFrame
"""
dV = {'Muga': ['Rioja', 2012, 8.5],'Petit caus': ['Penedes',2014, 6.75],\
     'Viña vial': ['Rioja',2016,9.5], 'Lavia': ['Jumilla',2011,12.5], \
     'Bach': ['Penedes',2015, 4.5], 'Pazo B': ['Rias Baixas', 2016,13.0]}
lstV = []
for k, v in dV.items():
    elem = [k]
    elem.extend(v)
    lstV.append(elem)
colV = ['Nombre','Origen','Añada','Precio']
indV = ['V1','V2','V3','V4','V5','V6']
dfVinos = pd.DataFrame(lstV,columns=colV, index = indV)
dfVinos.name = 'Vinos '
print(dfVinos)
    