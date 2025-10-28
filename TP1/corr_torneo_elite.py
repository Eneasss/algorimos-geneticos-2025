"""
ALGORITMO GENÉTICO CON SELECCIÓN POR TORNEO Y ELITISMO

Este programa implementa un algoritmo genético para maximizar la función f(x) = (x/(2^30-1))^2.
Utiliza una población de 10 individuos, cada uno representado por un cromosoma de 30 bits.
El método de selección implementado es el TORNEO con ELITISMO, donde:
1. Los dos mejores individuos pasan directamente a la siguiente generación (elitismo)
2. El resto de individuos se seleccionan mediante torneos de 4 participantes

También implementa operadores de cruce (crossover) de un punto y mutación con probabilidades
del 75% y 5% respectivamente. El algoritmo ejecuta 100 ciclos (generaciones).
"""

import random


def mostrar_pantalla(poblacion, decimales, objetivo, fitness, pob, total, min_val, max_val, prom):
    """
    Muestra en pantalla el estado actual de la población.
    
    Parámetros:
    - poblacion: Matriz de cromosomas (30 bits x 10 individuos)
    - decimales: Valores decimales de cada cromosoma
    - objetivo: Valores de la función objetivo para cada individuo
    - fitness: Valores de aptitud (fitness) de cada individuo
    - pob: Número de generación actual
    - total, min_val, max_val, prom: Estadísticas de la población
    """
    if pob != 0:
        print(f"Poblacion {pob}")
    else:
        print("Poblacion Inicial\n")

    print(" =============================================================================")

    for c in range(10):
        print(f"{c:2d}: ", end="")

        # Muestra la fila de población (binarios)
        for i in range(30):
            print(f"{poblacion[i][c]}", end="")
        print(" ", end="")

        # Muestra los valores decimales, objetivo y fitness
        print(f"{decimales[c]:10.4f} {objetivo[c]:10.4f} {fitness[c]:10.4f}")

    # Muestra totales, mínimos, máximos y promedios
    print("\nResumen:")
    print(f"{'Total:':<10} {total[0]:10.4f} {total[1]:10.4f}")
    print(f"{'Minimo:':<10} {min_val[0]:10.4f} {min_val[1]:10.4f}")
    print(f"{'Maximo:':<10} {max_val[0]:10.4f} {max_val[1]:10.4f}")
    print(f"{'Promedio:':<10} {prom[0]:10.4f} {prom[1]:10.4f}")


def PoblacionInicial(poblacion):
    """
    Genera una población inicial aleatoria.
    
    Parámetros:
    - poblacion: Matriz donde se almacenarán los cromosomas generados (30 bits x 10 individuos)
    """
    for c in range(10):
        for i in range(30):
            poblacion[i][c] = random.randint(0, 1)


def BinDec(poblacion, decimales):
    """
    Convierte cada cromosoma binario a su valor decimal equivalente.
    
    Parámetros:
    - poblacion: Matriz de cromosomas binarios
    - decimales: Lista donde se almacenarán los valores decimales calculados
    """
    for i in range(10):
        dec = 0
        exp = 29  # Comienza en 29 porque el cromosoma tiene 30 bits (0-29)
        for c in range(30):
            if poblacion[c][i] == 1:
                dec += 2 ** exp  # Suma la potencia de 2 correspondiente si el bit es 1
            exp -= 1
        decimales[i] = dec


def FunObj(decimales, objetivo, total, min_val, max_val, prom):
    """
    Calcula el valor de la función objetivo para cada individuo.
    La función a maximizar es f(x) = (x/(2^30-1))^2
    
    Parámetros:
    - decimales: Valores decimales de cada cromosoma
    - objetivo: Lista donde se almacenarán los valores de la función objetivo
    - total, min_val, max_val, prom: Estadísticas a calcular
    
    Retorna:
    - binario: Representación binaria del mejor individuo (mayor valor decimal)
    """
    coef = (2 ** 30) - 1  # Máximo valor posible con 30 bits
    m = 0
    for c in range(10):
        aux = round((decimales[c] / coef) ** 2, 4)  # Normaliza y eleva al cuadrado
        objetivo[c] = float(aux)
        if decimales[c] > m:
            m = int(decimales[c])  # Guarda el mayor valor decimal

    binario = bin(m)[2:]  # Convierte a binario y elimina el prefijo '0b'

    # Calcula estadísticas para la función objetivo
    total[0] = min_val[0] = max_val[0] = prom[0] = objetivo[0]
    for c in range(1, 10):
        total[0] += objetivo[c]
        if objetivo[c] < min_val[0]:
            min_val[0] = objetivo[c]
        if objetivo[c] > max_val[0]:
            max_val[0] = objetivo[c]
    prom[0] = total[0] / 10

    return binario


def FunFit(objetivo, fitness, total, min_val, max_val, prom):
    """
    Calcula el fitness (aptitud) de cada individuo como la proporción
    de su valor objetivo respecto al total.
    
    Parámetros:
    - objetivo: Valores de la función objetivo
    - fitness: Lista donde se almacenarán los valores de fitness
    - total, min_val, max_val, prom: Estadísticas a actualizar
    """
    total[1] = 0
    for c in range(10):
        fitness[c] = objetivo[c] / total[0]  # Fitness proporcional al valor objetivo
        total[1] += fitness[c]

    # Actualiza estadísticas para los valores de fitness
    min_val[1] = min_val[0] / total[0]
    max_val[1] = max_val[0] / total[0]
    prom[1] = prom[0] / total[0]


def Torneo(seleccion, fitness, poblacion, pob_siguiente):
    """
    Implementa el método de selección por torneo con elitismo.
    Los dos mejores individuos pasan directamente a la siguiente generación,
    y el resto se selecciona mediante torneos de 4 participantes.
    
    Parámetros:
    - seleccion: Lista donde se almacenarán los índices de los individuos seleccionados
    - fitness: Valores de fitness de cada individuo
    - poblacion: Población actual
    - pob_siguiente: Matriz donde se almacenarán los nuevos individuos
    """
    max1 = max2 = m1 = m2 = 0

    # Elitismo: identifica los dos individuos con mayor fitness
    for c in range(10):
        if fitness[c] >= max1:
            max2 = max1
            m2 = m1
            max1 = fitness[c]
            m1 = c
        elif fitness[c] > max2:
            max2 = fitness[c]
            m2 = c

    # Copia los dos mejores individuos directamente a la siguiente generación
    for i in range(30):
        pob_siguiente[i][0] = poblacion[i][m1]
        pob_siguiente[i][1] = poblacion[i][m2]

    # Selección por torneo para el resto de la población (posiciones 2-9)
    for j in range(2, 10):
        torneo = []    # Almacena fitness de los participantes del torneo
        postorneo = [] # Almacena posiciones de los participantes del torneo
        
        # Selecciona 4 individuos aleatorios para el torneo
        for ind in range(4):
            pos = random.randint(0, 9)
            torneo.append(fitness[pos])
            postorneo.append(pos)
            
        # Encuentra el ganador del torneo (el de mayor fitness)
        ganador = torneo[0]
        posganador = postorneo[0]
        for i in range(1, 4):
            if ganador < torneo[i]:
                ganador = torneo[i]
                posganador = postorneo[i]
                
        # El ganador es seleccionado para reproducción
        seleccion[j] = posganador


def CrossOver(poblacion, pob_siguiente, seleccion):
    """
    Realiza el cruce (crossover) entre pares de individuos seleccionados.
    Utiliza el método de cruce de un punto con probabilidad del 75%.
    
    Parámetros:
    - poblacion: Población actual
    - pob_siguiente: Matriz donde se almacenarán los nuevos individuos
    - seleccion: Índices de los individuos seleccionados para reproducción
    """
    PC = 75  # Probabilidad de crossover = 0.75

    for c in range(2, 10, 2):  # Comienza en 2 porque las posiciones 0 y 1 ya tienen los élites
        pad1 = seleccion[c]
        pad2 = seleccion[c + 1]
        prob = random.randint(0, 100)

        if prob < PC:  # Si se cumple la probabilidad de cruce
            pto = random.randint(1, 29)  # Selecciona un punto de cruce aleatorio
            # Primera parte: genes del padre 1 al hijo 1, genes del padre 2 al hijo 2
            for i in range(pto):
                pob_siguiente[i][c] = poblacion[i][pad1]
                pob_siguiente[i][c + 1] = poblacion[i][pad2]
            # Segunda parte: genes del padre 2 al hijo 1, genes del padre 1 al hijo 2
            for i in range(pto, 30):
                pob_siguiente[i][c] = poblacion[i][pad2]
                pob_siguiente[i][c + 1] = poblacion[i][pad1]
        else:  # Si no hay cruce, los hijos son copias exactas de los padres
            for i in range(30):
                pob_siguiente[i][c] = poblacion[i][pad1]
                pob_siguiente[i][c + 1] = poblacion[i][pad2]


def Mutacion(pob_siguiente):
    """
    Aplica el operador de mutación a la nueva población.
    Con una probabilidad del 5%, invierte un bit aleatorio de cada individuo.
    
    Parámetros:
    - pob_siguiente: Matriz de la nueva población a mutar
    """
    PM = 5  # Probabilidad de mutación = 5%

    for c in range(10):
        prob = random.randint(0, 100)
        if prob < PM:  # Si se cumple la probabilidad de mutación
            pto = random.randint(0, 29)  # Selecciona un gen (bit) aleatorio
            pob_siguiente[pto][c] = 1 - pob_siguiente[pto][c]  # Invierte el valor del bit


def ActualizarPob(poblacion, pob_siguiente):
    """
    Actualiza la población actual con la nueva generación.
    
    Parámetros:
    - poblacion: Matriz de la población actual
    - pob_siguiente: Matriz de la nueva población
    """
    for c in range(10):
        for i in range(30):
            poblacion[i][c] = pob_siguiente[i][c]


def GuardarDatos(cromosoma, max_val, min_val, prom, pob):
    """
    Guarda los datos de la generación actual en un archivo CSV.
    
    Parámetros:
    - cromosoma: Representación binaria del mejor individuo
    - max_val, min_val, prom: Estadísticas de la población
    - pob: Número de generación
    """
    with open("Algoritmos.csv", "a", encoding="utf-8") as file:
        if pob != 0:
            file.write(f'"{cromosoma}";{max_val[0]};{min_val[0]};{prom[0]}\n')
        else:
            file.write("Cromosoma;Maximo;Minimo;Promedio\n")


def main():
    """
    Función principal que ejecuta el algoritmo genético.
    """
    # Inicialización de estructuras de datos
    poblacion = [[0 for _ in range(10)] for _ in range(30)]  # 30 genes x 10 individuos
    pob_siguiente = [[0 for _ in range(10)] for _ in range(30)]
    decimales = [0.0] * 10  # Valores decimales de cada cromosoma
    objetivo = [0.0] * 10   # Valores de la función objetivo
    fitness = [0.0] * 10    # Valores de fitness
    total = [0.0] * 2       # Total para objetivo[0] y fitness[1]
    min_val = [0.0] * 2     # Mínimos para objetivo[0] y fitness[1]
    max_val = [0.0] * 2     # Máximos para objetivo[0] y fitness[1]
    prom = [0.0] * 2        # Promedios para objetivo[0] y fitness[1]
    seleccion = [0] * 10    # Índices de individuos seleccionados
    ciclos = 100            # Número de generaciones a ejecutar

    pob = 0  # Contador de generaciones, 0 = población inicial

    # Generación y evaluación de la población inicial
    PoblacionInicial(poblacion)
    BinDec(poblacion, decimales)
    cromosoma = FunObj(decimales, objetivo, total, min_val, max_val, prom)
    FunFit(objetivo, fitness, total, min_val, max_val, prom)
    mostrar_pantalla(poblacion, decimales, objetivo, fitness, pob, total, min_val, max_val, prom)
    GuardarDatos(cromosoma, max_val, min_val, prom, pob)
    input("Presione una tecla para continuar...")

    # Ciclo principal del algoritmo genético
    for c in range(1, ciclos + 1):
        pob = c
        # 1. Selección por torneo con elitismo
        Torneo(seleccion, fitness, poblacion, pob_siguiente)
        # 2. Cruce (crossover)
        CrossOver(poblacion, pob_siguiente, seleccion)
        # 3. Mutación
        Mutacion(pob_siguiente)
        # 4. Actualización de la población
        ActualizarPob(poblacion, pob_siguiente)
        # 5. Evaluación de la nueva población
        BinDec(poblacion, decimales)
        cromosoma = FunObj(decimales, objetivo, total, min_val, max_val, prom)
        FunFit(objetivo, fitness, total, min_val, max_val, prom)
        # 6. Mostrar y guardar resultados
        mostrar_pantalla(poblacion, decimales, objetivo, fitness, pob, total, min_val, max_val, prom)
        GuardarDatos(cromosoma, max_val, min_val, prom, pob)
        input("Presione una tecla para continuar...")

if __name__ == "__main__":
    main()