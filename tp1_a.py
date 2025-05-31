import matplotlib
import random
import numpy as np

coef = 2 ** 30 - 1
cross = .75
mut = .05
popul = 10
ciclos = 20


def function(x):
    n = (x / coef) ** 2
    return n


def mostrar_resul(valor):
    maxim = max(valor)
    minim = min(valor)
    prom = np.average(valor)
    print(f'Maximo: {maxim}, Minimo: {minim}, Promedio: {prom}\n')


def fitness(valor, ind):
    return valor[ind] / np.sum(valor)


def main():
    sol = []
    valor = []
    for ind in range(popul):
        sol.append(random.randint(0, coef))
        valor.append(function(sol[ind]))
    print('Valores Corrida: 1\n')
    mostrar_resul(valor)
    for ciclo in range(ciclos - 1):
        ruleta = []
        for ind in range(popul):
            for p in range(round(fitness(valor, ind) * 100)):
                ruleta.append(sol[ind])
        valoresRuleta = []
        ruletaSize = ruleta.__len__()
        for ind in range(popul):
            valoresRuleta.append(ruleta[random.randint(0, ruletaSize - 1)])
        for ind in range(0, popul, 2):
            if random.random() < cross:
                corte = random.randint(1, 29)
                a = format(valoresRuleta[ind], 'b').zfill(30)
                b = format(valoresRuleta[ind + 1], 'b').zfill(30)

                a_head, a_tail = a[:corte], a[corte:]
                b_head, b_tail = b[:corte], b[corte:]

                sol[ind] = int(a_head + b_tail, 2)
                sol[ind + 1] = int(b_head + a_tail, 2)
            else:
                sol[ind] = valoresRuleta[ind]
                sol[ind + 1] = valoresRuleta[ind + 1]
            if random.random() < mut: # De la pareja el primer cromosoma
                bit = random.randint(0, 29)
                a = format(sol[ind], 'b').zfill(30)
                bit_cambiado = '1' if a[bit] == '0' else '0'
                sol[ind] = int(a[:bit] + bit_cambiado + a[bit + 1:], 2)
            if random.random() < mut: # De la pareja el segundo cromosoma
                bit = random.randint(0, 29)
                b = format(sol[ind + 1], 'b').zfill(30)
                bit_cambiado = '1' if b[bit] == '0' else '0'
                sol[ind + 1] = int(b[:bit] + bit_cambiado + b[bit + 1:], 2)
            valor[ind] = function(sol[ind])
            valor[ind + 1] = function(sol[ind + 1])
        print(f'Valores Corrida: {ciclo + 2}\n')
        mostrar_resul(valor)


if __name__ == "__main__":
    main()
