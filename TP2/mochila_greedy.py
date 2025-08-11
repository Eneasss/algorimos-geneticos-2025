import sys

class Mochila:
    """Representa la mochila con una capacidad de volumen definida."""
    def __init__(self, volumen):
        if volumen <= 0:
            raise ValueError("El volumen de la mochila debe ser positivo.")
        self.volumen = float(volumen)

class Item:
    """Representa un ítem con volumen y valor.
    
    Attributes:
        volumen (float): El espacio que ocupa el ítem.
        valor (float): El valor que aporta el ítem.
    """
    def __init__(self, volumen, valor):
        if volumen <= 0 or valor <= 0:
            raise ValueError("Tanto el volumen como el valor del ítem deben ser positivos.")
        self.volumen = float(volumen)
        self.valor = float(valor)

    def __repr__(self):
        return f"Item(volumen={self.volumen}, valor={self.valor})"

    @property
    def ratio_valor_volumen(self):
        """Calcula y devuelve la relación valor/volumen del ítem."""
        return self.valor / self.volumen

class SolucionMochila:
    """Almacena el resultado de los ítems seleccionados.
    
    Similar a 'Subconjunto' en la versión exhaustiva, pero renombrada
    para mayor claridad en el contexto del problema.
    """
    def __init__(self):
        self.items = []

    def agregar_item(self, item):
        self.items.append(item)

    def obtener_volumen_total(self):
        """Calcula la suma de los volúmenes de los ítems en la solución."""
        return sum(item.volumen for item in self.items)

    def obtener_valor_total(self):
        """Calcula la suma de los valores de los ítems en la solución."""
        return sum(item.valor for item in self.items)

class EstrategiaMochilaGreedy:
    """Implementa el algoritmo voraz para resolver el problema de la mochila.
    
    La estrategia consiste en seleccionar ítems basándose en la mejor relación
    valor/volumen.
    """
    def resolver(self, mochila, items):
        """Selecciona los mejores ítems para la mochila usando una estrategia voraz.

        Args:
            mochila (Mochila): La mochila a llenar.
            items (list[Item]): La lista de ítems disponibles.

        Returns:
            SolucionMochila: La solución encontrada con los ítems seleccionados.
        """
        # Ordena los ítems de mayor a menor según su ratio valor/volumen.
        items_ordenados = sorted(items, key=lambda item: item.ratio_valor_volumen, reverse=True)
        
        solucion = SolucionMochila()
        volumen_actual = 0.0

        for item in items_ordenados:
            if volumen_actual + item.volumen <= mochila.volumen:
                solucion.agregar_item(item)
                volumen_actual += item.volumen
                
        return solucion

class Programa:
    """Clase de utilidad para ejecutar el programa principal."""
    @staticmethod
    def main():
        """Punto de entrada principal de la aplicación."""
        try:
            mochila = Mochila(4200)
            items_disponibles = [
                Item(150, 20),
                Item(325, 40),
                Item(600, 50),
                Item(805, 36),
                Item(430, 25),
                Item(1200, 64),
                Item(770, 54),
                Item(60, 18),
                Item(930, 46),
                Item(353, 28)
            ]

            estrategia = EstrategiaMochilaGreedy()
            mejor_solucion = estrategia.resolver(mochila, items_disponibles)

            print("La solución GULOSA contiene los siguientes ítems: ")
            for item in mejor_solucion.items:
                print(f"  - Volumen: {item.volumen:<5} cm3 | Valor: ${item.valor:<5} | Ratio: {item.ratio_valor_volumen:.2f}")

            print("\n--------------------------------------------------")
            print(
                f"Volumen total: {mejor_solucion.obtener_volumen_total()} cm3 (Capacidad: {mochila.volumen} cm3)"
                f"\nValor total:   ${mejor_solucion.obtener_valor_total()}"
            )
            print("--------------------------------------------------")

        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    Programa.main()