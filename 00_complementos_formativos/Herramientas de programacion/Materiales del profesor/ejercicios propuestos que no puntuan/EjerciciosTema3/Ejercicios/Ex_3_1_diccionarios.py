# -*- coding: utf-8 -*-
# Ex 1 Frecuencia de números, 
lista = [1, 3, 2, 4, 2, 2, 3, 2, 4, 1, 2, 1, 2, 3, 1, 3, 1]
def frecuencias(lst):
    """
    >>> D=frecuencias([1, 3, 2, 4, 2, 2, 3, 2, 4, 1, 2, 1, 2, 3, 1, 3, 1])
    >>> D == {1: 5, 2: 6, 3: 4, 4: 2}
    True
    """
    d = {}
    for item in lst:
        if item not in d:
            d[item] = 1
        else:
            d[item] += 1
    return d
# método mas simple usando librería collections
from collections import Counter
d = dict(Counter(lista))
def frecuencias2(frase):
    """Retorna un diccionario con el número
    de veces que aparece cada palabra contenida
    en un string. Ejemplos:
    Retorna un diccionario con el número de veces que aparece cada 
    palabra contenida en un string. Ejemplos:
    >>> d = frecuencias2('la silla de metal y la mesa de abajo de madera')
    >>> d == {'la': 2, 'silla': 1, 'de': 3, 'metal': 1, 'y': 1, \
    'mesa': 1, 'abajo': 1, 'madera': 1}
    True
    >>> d = frecuencias2("a a b b b c c c c d e e")
    >>> d == {'c': 4, 'a': 2, 'b': 3, 'e': 2, 'd': 1}
    True
    """
    res = {}
    for item in frase.split():
        if item not in res:
            res[item] = 1
        else:
            res[item] += 1
    return res
# Ex 2 Moda (estadística)
def moda(lst):
    """
    >>> moda([1, 3, 2, 4, 2, 2, 3, 2, 4, 1, 2, 1, 2, 3, 1, 3, 1])
    2
    """
    d = frecuencias(lst)
    M = 0
    res = float('NaN')  # NaN: Not a Number (corrige el error para lst = [])
    for k in d:         # k: key o clave
        if d[k] > M:
            M = d[k]
            res = k
    return res

# Ex 3 Histograma
def histograma(lst):        # Histograma vertical
    """
    >>> histograma([1, 3, 2, 4, 2, 2, 3, 2, 4, 1, 2, 1, 2, 3, 1, 3, 1])
    1 *****
    2 ******
    3 ****
    4 **
    """
    d = frecuencias(lst)
    L = list(d.keys())
    L.sort()
    for k in L:
        print(k,d[k]*'*')
def histograma_h(lst):      # Histograma horizontal (NO pedido)
    """
    >>> histograma_h(lista)
      *    
    * *    
    * * *  
    * * *  
    * * * *
    * * * *
    1 2 3 4
    """
    d = frecuencias(lst)
    altura = max(d.values())
    k = list(d.keys())
    k.sort()
    for fila in range(altura,0,-1):
        f=[]
        for clave in k:
            if fila <= d[clave]:
                f.append('*')
            else:
                f.append(' ')
        print(*f, sep=' ')    #* expande la lista en sus elementos
    print(*k, sep=' ')   #  para poderla imprimir sin llaves ni comas
# Ex 4 Agenda (sin repetidos): Lista - Diccionario  
def Agenda1(lst):
    """
    >>> lista1 = [["Luisa", "931111111"], ["José", "912222222"], \
                  ["Judith", "96919391"]]
    >>> L = Agenda1(lista1)
    >>> L == {"Luisa": "931111111", "José": "912222222", "Judith": "96919391"}
    True
    """
    d = {}
    for item in lst:
        d[item[0]] = item[1]
    return d
# versión simplificada tipo list comprenhension (dict comprenhension)
def Agenda11(lst):
     d = {item[0]:item[1] for item in lst}
     return d
# version simple
def Agenda13(lst):
    """
    >>> lista1 = [["Luisa", "931111111"], ["José", "912222222"], \
                  ["Judith", "96919391"]]
    >>> L = Agenda1(lista1)
    >>> L == {"Luisa": "931111111", "José": "912222222", "Judith": "96919391"}
    True
    """
    return dict(lst)
# Ex 5 Agenda2: Lista a diccionario con nombres repetidos con + teléfonos,
def Agenda2(lst):
    """
    >>> lst2 = [["Luisa", "931111111"], ["José", "912222222"], \
        ["Judith", "96919391"], ["Luisa", "65555555"], ["José", "61133333"]]
    >>> L2 = Agenda2(lst2)
    >>> L2 == {'José': ['912222222', '61133333'], \
               'Luisa': ['931111111', '65555555'], 'Judith': ['96919391']}
    True
    """
    d = {}
    for item in lst:
        if item[0] not in d:
            d[item[0]] = [item[1]]
        else:
            d[item[0]].append(item[1])
    return d

# Ex 6 Temp Ciudades
"""Temperaturas de ciudades. Un diccionario guarda las temperaturas mínimas 
de los 3 primeros meses del año de distintas ciudades, de la forma 
"""
dicE = {'Londres': [3.4, 6.3, 10.5], 'Oslo': [-3.8, -5.0, 4.2], \
       'Rennes': [2.5, 3.1, 12.3]}
# a)
def mediaTemp(dic):
    """
    >>> dd = mediaTemp(dicE)
    >>> dd == {'Londres': 6.73, 'Rennes': 5.97, 'Oslo': -1.53}
    True
    """
#    d = {}
#    for k in dic:
#        m = sum(dic[k])/len(dic[k])
#        d[k] = round(m, 2)
#    return d
    d = {}
    for k, v in dic.items():
        m = sum(v)/len(v)
        d[k] = round(m, 2)
    return d
        
# b)
"""
minimasTemp(dict), en que dado un diccionario como el del ejemplo nos 
devuelva un diccionario con el valor mínimo de las temperaturas de cada ciudad
"""
def minimasTemp(dic):
    """
    >>> D = minimasTemp(dicE)
    >>> D == {'Londres': 3.4, 'Rennes': 2.5, 'Oslo': -5.0}
    True
    """
    d = {}
    for i in dic:
        d[i] = min(dic[i])
    return d
# c) 
"""minTemp(dict), en que dado un diccionario como el del ejemplo nos 
devuelva una lista con la ciudad con la temperatura más baja y su valor. 
"""
def minTemp(dic):
    """
    >>> minTemp(dicE)
    ['Oslo', -5.0]
    """
    d = minimasTemp(dic)
    m = min(d.values())
    for k in d.keys():
        if d[k]==m:
            return [k,m]
def minTemp2(dic):
    """
    >>> minTemp(dicE)
    ['Oslo', -5.0]
    """
    d =  minimasTemp(dic)
    V = list(d.values())
    K = list(d.keys())
    m = min(V)
    ind = V.index(m)
    return [K[ind],m]

""" Ex 7
    Diccionario de vinos. Se dispone de un diccionario de vinos donde las 
    claves son nombres vinos y los valores para cada vino son una lista con
    la información de su denominación de origen, la añada y su precio.
    Diseñar una función en que, dado un diccionario de vinos como el descrito y 
    una lista con un rango de precios [menorPrecio, mayorPrecio], nos devuelva
    una lista de los nombres (ordenados alfabéticamente de los vinos que estén 
    en este rango de precios.
  
"""
d = {'Muga': ['Rioja',2012,8.5],'Petit caus': ['Penedes',2014, 6.75], \
     'Viña vial': ['Rioja',2016,9.5], 'Lavia': ['Jumilla',2011,12.5], \
     'Bach': ['Penedes',2015, 4.5], 'Pazo B': ['Rias Baixas', 2016, 13.0]}

def lista_vinos(d,rango):
    """ Lista de vinos en un rango de precios
    d = {'Muga': ['Rioja',2012,8.5],'Petit caus': ['Penedes',2014, 6.75], \
         'Viña vial': ['Rioja',2016,9.5], 'Lavia': ['Jumilla',2011,12.5], \
         'Bach': ['Penedes',2015, 4.5], 'Pazo B': ['Rias Baixas', 2016, 13.0]}
    >>> lista_vinos(d,[10, 15])
    ['Lavia', 'Pazo B']
    """
#    lst = []
#    for vino in d:
##        if d[vino][2] >= rango[0] and d[vino][2] <= rango[1]:
#        if rango[0] <= d[vino][2] <= rango[1]:
#            lst.append(vino)
#    lst.sort()
#    return lst
#   return sorted(lst)
    lst = []
    for vino, datos in d.items():
#        if d[vino][2] >= rango[0] and d[vino][2] <= rango[1]:
        if rango[0] <= datos[2] <= rango[1]:
            lst.append(vino)
    lst.sort()
    return lst
# 8 Lego
def contar_piezas(d_caja,d_model):
    """
    >>> d_caja = {'roja':20, 'azul':15, 'amarilla':25, 'verde': 10, 'negra':10}
    >>> d_model = {'gris': 9, 'roja':10, 'azul':20, 'amarilla':6, 'naranja': 3}
    >>> d_falta = {'azul':5, 'gris': 9, 'naranja': 3}
    >>> d_falta == contar_piezas(d_caja,d_model)
    True
    """
    d = {}
    for k, v in d_model.items():
        if k in d_caja:
            if d_caja[k] < v:
                d[k] = v - d_caja[k]
        else:
            d[k] = v
    return d

# 9. La cuenta por favor
def la_cuenta(carta, consumicion):
    """
    >>> carta = {'arroz a banda': 6.5, 'pollo al horno': 5, \
                 'conejo a la brasa': 7.5, 'judias verdes': 4.0, \
                 'paella': 7.5, 'pimientos rellenos': 5.2, \
                 'gazpacho': 4,'potaje de garbanzos': 4.5, \
                 'calamares a la romana': 7, 'lubina a la sal': 8, \
                 'bacalao con patatas': 9, 'espinacas': 4, \
                 'ensalada de atun': 5}
    >>> consumicion = {'conejo a la brasa': 2, 'paella': 1}
    >>> la_cuenta(carta, consumicion)
    22.5
    >>> consumicion = {'arroz a banda': 1, 'pollo al horno': 2, \
                       'ensalada de atun': 3, 'calamares a la romana': 2, \
                       'espinacas': 1}
    >>> la_cuenta(carta, consumicion)
    49.5
    """
    suma = 0
    for k, v in consumicion.items():
        suma += carta[k]*v
    return round(suma, 2)

""" 10.
Queremos traducir a código Morse un mensaje escrito utilizando sólo vocales 
mayúsculas que está escondido en una cadena (string) s.
Por ejemplo, si s = "LALALAlalala" el mensaje es "AAA" y la letra "A" en Morse
es: ".-" su traducción a código Morse es:  ".- .- .-" (notar que hay un espacio
en blanco entre cada letra en código Morse)

Implemente la función morse_vowel_translator(dic_morse_vow, s) que, dado el 
diccionario dic_morse_vow donde las claves son las vocales mayúsculas y los 
valores sus respectivos códigos Morse, devuelva la traducción del mensaje 
escondido en s. Para encontrar este mensaje se deben extraer de s las vocales 
mayúsculas que contenga, preservando el orden en que aparecen. La traducción 
del mensaje es simplemente el código Morse de cada vocal mayúscula, separado 
por un espacio en blanco. En caso de que el mensaje sea vacío, se debe 
devolver un string vacío.
Observación:
El diccionario dic_morse_vow = {"A":".-","E":".","I":"..","O":"---", "U":"..-"}
será dado como argumento de entrada de la función.
"""

def morse_vowel_translator(dic_morse_vow, s):
    """
    >>> dic_morse_vow = {"A":".-","E":".","I":"..","O":"---", "U":"..-"}
    >>> morse_vowel_translator(dic_morse_vow,"LALALAlalala")
    '.- .- .-'
    >>> morse_vowel_translator(dic_morse_vow,"AaEeIiOoUu")
    '.- . .. --- ..-'
    >>> morse_vowel_translator(dic_morse_vow,"aeiou")
    ''
    >>> morse_vowel_translator(dic_morse_vow,"UOIAE")
    '..- --- .. .- .'
    >>> morse_vowel_translator(dic_morse_vow,"AIAIAIAI")
    '.- .. .- .. .- .. .- ..'
    >>> morse_vowel_translator(dic_morse_vow,"A")
    '.-'
    >>> morse_vowel_translator(dic_morse_vow,"E")
    '.'
    >>> morse_vowel_translator(dic_morse_vow,"I")
    '..'
    >>> morse_vowel_translator(dic_morse_vow,"O")
    '---'
    >>> morse_vowel_translator(dic_morse_vow,"U")
    '..-'
    """
    msg = ""
    for c in s:
        if c in "AEIOU": 
            if msg != "":      # este if se usa para agregar un espacio 
                msg += " "     # a partir de la 1ra letra en Morse
            msg += dic_morse_vow[c]
    return msg
            

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
