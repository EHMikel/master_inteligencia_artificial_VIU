# Esta funcion calcula el gradiente para cualquier funcion, dada una funcion lambda y la lista de sus correspondientes variables
def gradiente(funcion_lambda, lista_variables:list):

    import numpy as np
    from sympy import diff, symbols, lambdify

    gradiente = {}                                                      # el gradiente será un diccionario donde las claves seran la funcion escrita y los valores, la funcion gradiente de cada componente
    simb_var = symbols(lista_variables)                                 # guardo los simbolos de las variables que utilizaré después

    for variable in lista_variables:                                    # para cada variable en mi lista de variables vamos a calcular su derivada parcial

        derivada_parcial = diff(funcion_lambda(*simb_var), variable)    # se crea la funcion gradiente 'escrita', es necesario desempaquetar todas las variables para darselas a la funcion lambda
        f_dev_parcial = lambdify(simb_var, derivada_parcial)            # comvierto la funcion 'escrita' en otra funcion lambda, que es la derivada parcial de la variable correspondiente
        gradiente[derivada_parcial] = f_dev_parcial                     # añado a mi diccionario tanto la derivada 'escrita' (llave), como la derivada en formato lambda (valor)

    return gradiente                                                    # devuelvo el diccionario de mis derivadas parciales, que juntas, conforman el vector gradiente


def generar_datos(f= lambda x: 0.5*x +10):
    import numpy as np

    x = np.linspace(0,5)
    ruido_varianza= 0.05
    y = f(x) + np.random.randint(low = -10, high= 10, size = x.shape[0])*ruido_varianza

    return np.array([x,y])

def batch_gradient_descent_sesgo(cost_func, variables_lst, learning_rate, max_iter, precision):
    import random
    import numpy as np

    w = random.random()
    b = random.random()

    cost_grad = gradiente(cost_func, variables_lst)         # calculo el gradiente
    lista_de_grad = list(cost_grad.keys())
    cost_grad_f = [cost_grad[lista_de_grad[0]], cost_grad[lista_de_grad[1]]]               # el primer valor del diccionario de gradientes es mi derivada respecto a w

    print(lista_de_grad[0])
    print(lista_de_grad[1])

    data = generar_datos(f= lambda x: x*200+10)                 # datos a partir de una funcion con ruido añadido; W y b COMVERGERÁN AL MULTIPLO DE X EN ESTE CASO 10
    x = data[0]
    y = data[1]

    for epoch in range(max_iter):

        error = np.sum(cost_func(w, b, x, y))

        w -= learning_rate*(np.sum(cost_grad_f[0](w, b, x, y)))
        b -= learning_rate*(np.sum(cost_grad_f[1](w, b, x, y)))

        new_error = np.sum(cost_func(w, b, x, y))

        if abs(error - new_error):
            print(epoch)
            break

    p = np.array([w, b])
    return p


if __name__ == '__main__':

