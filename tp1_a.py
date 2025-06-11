import matplotlib.pyplot as plt
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


def mostrar_resul(valor, maximos, minimos, promedios):
    maxim = max(valor)
    minim = min(valor)
    prom = np.average(valor)
    maximos.append(maxim)
    minimos.append(minim)
    promedios.append(prom)
    print(f'Maximo: {maxim}, Minimo: {minim}, Promedio: {prom}\n')


def fitness(valor, ind):
    return valor[ind] / np.sum(valor)


def graficar(maximos, minimos, promedios):
    plt.plot(maximos, label='Máximo', color='red')
    plt.plot(minimos, label='Mínimo', color='blue')
    plt.plot(promedios, label='Promedio', color='green')
    plt.xlabel('Corrida')
    plt.ylabel('Valor func objetivo')
    plt.title('Evolución de func objetivo')
    plt.legend()
    plt.grid(True)
    plt.show()


def inicializar(sol, valor):
    for ind in range(popul):
        sol.append(random.randint(0, coef))
        valor.append(function(sol[ind]))


def generarRuleta(sol, valor):
    ruleta = []
    ruletaSize = 0
    for ind in range(popul):
        for p in range(round(fitness(valor, ind) * 100)):
            ruleta.append(sol[ind])
            ruletaSize += 1
    return ruleta, ruletaSize


def seleccionarPadres(ruleta, ruletaSize):
    padres = []
    for ind in range(popul):
        padres.append(ruleta[random.randint(0, ruletaSize - 1)])
    return padres


def cruzarPadres(padres, ind, sol):
    #ind (individuo), sol (solucion)
    if random.random() < cross:
        corte = random.randint(1, 29)
        a = format(padres[ind], 'b').zfill(30)
        b = format(padres[ind + 1], 'b').zfill(30)

        a_head, a_tail = a[:corte], a[corte:]
        b_head, b_tail = b[:corte], b[corte:]

        sol[ind] = int(a_head + b_tail, 2)
        sol[ind + 1] = int(b_head + a_tail, 2)
    else:
        sol[ind] = padres[ind]
        sol[ind + 1] = padres[ind + 1]


def mutarHijos(sol, ind):
    if random.random() < mut:  # De la pareja el primer cromosoma
        bit = random.randint(0, 29)
        a = format(sol[ind], 'b').zfill(30)
        bit_cambiado = '1' if a[bit] == '0' else '0'
        sol[ind] = int(a[:bit] + bit_cambiado + a[bit + 1:], 2)
    if random.random() < mut:  # De la pareja el segundo cromosoma
        bit = random.randint(0, 29)
        b = format(sol[ind + 1], 'b').zfill(30)
        bit_cambiado = '1' if b[bit] == '0' else '0'
        sol[ind + 1] = int(b[:bit] + bit_cambiado + b[bit + 1:], 2)


def main():
    sol = []
    valor = []

    # Para graficas
    maximos = []
    minimos = []
    promedios = []

    inicializar(sol, valor)  #Genera poblacion inicial aleatoria
    print('Valores Corrida: 1\n')
    mostrar_resul(valor, maximos, minimos, promedios)

    for ciclo in range(ciclos - 1):
        ruleta, ruletaSize = generarRuleta(sol, valor)
        padres = seleccionarPadres(ruleta, ruletaSize)
        for ind in range(0, popul, 2):
            cruzarPadres(padres, ind, sol)
            mutarHijos(sol, ind)
            valor[ind] = function(sol[ind])
            valor[ind + 1] = function(sol[ind + 1])
        print(f'Valores Corrida: {ciclo + 2}\n')
        mostrar_resul(valor, maximos, minimos, promedios)
    graficar(maximos, minimos, promedios)


if __name__ == "__main__":
    main()
