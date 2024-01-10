def notas_al_pie(s):
    # esta función si admite strings vacíos

    if type(s) != str:
        raise ValueError('invalid input')

    cuenta_notas = 0

    for item in s:

        if item == '*':
            cuenta_notas += 1
            s = s.replace(item, f'({cuenta_notas})')

    return s

print(notas_al_pie('Esta es la primera nota*; y esta la segunda*.'))
print(notas_al_pie('*,*. *.'))
print(notas_al_pie(''))