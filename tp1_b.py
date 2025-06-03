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
    plt.ylabel('Fitness')
    plt.title('Evolución de fitness')
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    sol = []
    valor = []

    # Para graficas
    maximos = []
    minimos = []
    promedios = []

    for ind in range(popul):
        sol.append(random.randint(0, coef))
        valor.append(function(sol[ind]))
    print('Valores Corrida: 1\n')
    mostrar_resul(valor, maximos, minimos, promedios)
    for ciclo in range(ciclos - 1):
        torneo = []
        valoresTorneo = []
        for ind in range(popul * 2):
            torneo.append(sol[random.randint(0, popul - 1)])
        for ind in range(0, popul * 2, 2):
            a = torneo[ind]
            b = torneo[ind + 1]
            aVal = function(a)
            bVal = function(b)
            valoresTorneo.append(a if aVal > bVal else b)
        for ind in range(0, popul, 2):
            if random.random() < cross:
                corte = random.randint(1, 29)
                a = format(valoresTorneo[ind], 'b').zfill(30)
                b = format(valoresTorneo[ind + 1], 'b').zfill(30)

                a_head, a_tail = a[:corte], a[corte:]
                b_head, b_tail = b[:corte], b[corte:]

                sol[ind] = int(a_head + b_tail, 2)
                sol[ind + 1] = int(b_head + a_tail, 2)
            else:
                sol[ind] = valoresTorneo[ind]
                sol[ind + 1] = valoresTorneo[ind + 1]
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
        mostrar_resul(valor, maximos, minimos, promedios)
    graficar(maximos, minimos, promedios)


if __name__ == "__main__":
    main()
