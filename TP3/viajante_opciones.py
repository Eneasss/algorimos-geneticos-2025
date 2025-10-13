import random
import pandas as pd

class Heuristica:
    """Opciones 1 y 2"""
    def __init__(self, nombres, distancias):
        self.nombres = nombres
        self.distancias = distancias
        self.visitadas = [0] * 24  # Arreglo de bits: 0-No visitada, 1-Visitada
        self.recorrido = [0] * 25  # Arreglo de índices de capitales
        self.inicio = 0

    def inicializar_visitadas(self):
        """Llena el arreglo de "0" = No visitada"""
        for c in range(24):
            self.visitadas[c] = 0

    def elegir_ciudad(self):
        """Muestra lista y pide la ciudad de inicio"""
        print()
        while True:
            print("Seleccione la ciudad de inicio")
            for c in range(24):
                print(f"{c}: {self.nombres[c]}")

            try:
                inicio = int(input())
                if 0 <= inicio <= 23:
                    return inicio
                else:
                    print("Por favor, ingrese un número entre 0 y 23")
            except ValueError:
                print("Por favor, ingrese un número válido")

    def buscar_ciudad(self, actual):
        """Busca la ciudad a menor distancia de la actual"""
        menor = 10000
        destino = 0

        for c in range(24):  # Recorre índices de capitales
            if self.visitadas[c] == 0:  # Revisa que no esté marcada como ya visitada
                if self.distancias[actual][c] < menor:  # Compara las distancias y va guardando la menor
                    menor = self.distancias[actual][c]
                    destino = c
        return destino

    def calcular_recorrido(self, inicio):
        """Calcula el recorrido a seguir"""
        ciudad_actual = inicio
        self.recorrido[0] = self.recorrido[24] = ciudad_actual  # Coloca el índice de la ciudad de inicio donde es necesario
        self.visitadas[ciudad_actual] = 1

        for c in range(1, 24):  # Llena el recorrido pasando por las ciudades más cercanas
            self.recorrido[c] = self.buscar_ciudad(ciudad_actual)
            ciudad_actual = self.recorrido[c]
            self.visitadas[ciudad_actual] = 1

    def mostrar_recorrido(self):
        """Muestra el recorrido y su km total"""
        acum = 0

        for c in range(25):
            print(self.nombres[self.recorrido[c]])

        for c in range(24):
            acum = acum + self.distancias[self.recorrido[c]][self.recorrido[c + 1]]

        print(f"El recorrido total es de {acum} km")

    def solucion_uno(self):
        """Encuentra el recorrido para una ciudad determinada"""
        self.inicializar_visitadas()
        inicio = self.elegir_ciudad()
        self.calcular_recorrido(inicio)
        self.mostrar_recorrido()

    def solucion_dos(self):
        """Encuentra el óptimo entre todas las capitales"""
        optimo = 100000
        capital_inicio = 100

        for c in range(24):  # Realiza una iteración por capital c
            self.inicializar_visitadas()
            self.inicio = c
            self.calcular_recorrido(self.inicio)
            acum = 0

            for i in range(24):  # Calculo el km del recorrido
                acum = acum + self.distancias[self.recorrido[i]][self.recorrido[i + 1]]

            if acum <= optimo:
                optimo = acum
                capital_inicio = c

        print(
            f"El recorrido óptimo que visita todas las capitales se logra partiendo desde {self.nombres[capital_inicio]}")

        # Similar a la solución pero usando la capital que encontró como óptima
        self.inicializar_visitadas()
        self.inicio = capital_inicio
        self.calcular_recorrido(self.inicio)
        self.mostrar_recorrido()


class Genetico:
    """Opcion 3"""
    def __init__(self, nombres, distancias):
        self.nombres = nombres
        self.distancias = distancias
        self.cant_poblacion = 50
        self.poblacion = [[0 for _ in range(25)] for _ in range(self.cant_poblacion)]
        self.crom_min = 0 # Cromosoma con menor kilometraje
        self.min = 0 # Kilometraje del crom_min

    def inicializar_poblacion(self):
        for c in range(self.cant_poblacion):
            for i in range(25):
                self.poblacion[c][i] = 0

    def generar_poblacion(self):
        self.inicializar_poblacion()
        for c in range(self.cant_poblacion):
            for i in range(1, 24):
                while True:
                    x = random.randint(0, 23)
                    if self.poblacion[c][x] == 0:
                        break
                self.poblacion[c][x] = i
            self.poblacion[c][24] = self.poblacion[c][0]

    def mostrar_recorrido(self):
        for c in range(25):
            print(self.nombres[self.poblacion[self.crom_min][c]])
        print(f"El recorrido total es de {self.min} km")

    def solucion_tres(self):
        self.generar_poblacion()
        for c in range(200):
            pass # Borrar pass y agregar los métodos correspondientes para el alg. genético (calcular distancia, fitness, ruleta, etc.)

        self.mostrar_recorrido()


class Program:
    @staticmethod
    def main():
        # Leer el archivo Excel
        archivo_excel = 'TablaCapitales.xlsx'
        df = pd.read_excel(archivo_excel, index_col=0)

        # Obtener los nombres de las ciudades desde la primera columna (índice)
        nombres = df.index.tolist()

        # Obtener la matriz de distancias
        distancias = df.values.tolist()

        opc = -1
        while opc != 0:
            print()
            print("Seleccione la opción con la que se resolverá el problema:")
            print("1-Heurística Desde Determinada Ciudad\n2-Heurística Óptimo\n3-Algoritmo Genético\n0-Salir")

            try:
                opc = int(input())

                if opc == 1:
                    sol1 = Heuristica(nombres, distancias)
                    sol1.solucion_uno()
                elif opc == 2:
                    sol2 = Heuristica(nombres, distancias)
                    sol2.solucion_dos()
                elif opc == 3:
                    sol3 = Genetico(nombres, distancias)
                    sol3.solucion_tres()
                elif opc == 0:
                    print("Saliendo...")
                else:
                    print("Opción no válida")

            except ValueError:
                print("Por favor, ingrese un número válido")
                opc = -1  # Para continuar el bucle


if __name__ == "__main__":
    Program.main()