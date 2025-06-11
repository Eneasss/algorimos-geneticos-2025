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


def generarTorneo(sol):
    torneo = []
    for ind in range(popul * 2):
        torneo.append(sol[random.randint(0, popul - 1)])
    return torneo


def seleccionarPadres(torneo):
    padres = []
    for ind in range(0, popul * 2, 2):
        a = torneo[ind]
        b = torneo[ind + 1]
        aVal = function(a)
        bVal = function(b)
        padres.append(a if aVal > bVal else b)
    return padres


def cruzarPadres(padres, ind, sol):
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


def elegirElites(sol, valor):
    # Guardar mejores individuos
    individuos = list(zip(sol, valor))
    individuos.sort(key=lambda x: x[1], reverse=True)  # Ordenar por fitness (valor)
    elite = [individuos[0], individuos[1]]  # Los 2 mejores (mayor valor)
    return elite


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
        elite = elegirElites(sol, valor)
        torneo = generarTorneo(sol)
        padres = seleccionarPadres(torneo)

        # Agregar los elite al final y quitar los primeros 2 normales
        sol.append(elite[0][0])
        sol.append(elite[1][0])
        valor.append(elite[0][1])
        valor.append(elite[1][1])
        sol.remove(sol[0])
        sol.remove(sol[0])
        valor.remove(valor[0])
        valor.remove(valor[0])

        for ind in range(0, popul - 2, 2):  #No se tienen en cuenta los ultimos 2 que son elite
            cruzarPadres(padres, ind, sol)
            mutarHijos(sol, ind)
            valor[ind] = function(sol[ind])
            valor[ind + 1] = function(sol[ind + 1])
        print(f'Valores Corrida: {ciclo + 2}\n')
        mostrar_resul(valor, maximos, minimos, promedios)
    graficar(maximos, minimos, promedios)


if __name__ == "__main__":
    main()
