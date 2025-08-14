import sys


class Mochila:
    """Representa la mochila con una capacidad de peso definida."""

    def __init__(self, peso):
        if peso <= 0:
            raise ValueError("El peso de la mochila debe ser positivo.")
        self.peso = float(peso)


class Item:
    """Representa un ítem con peso y valor.

    Attributes:
        peso (float): El espacio que ocupa el ítem.
        valor (float): El valor que aporta el ítem.
    """

    def __init__(self, peso, valor):
        if peso <= 0 or valor <= 0:
            raise ValueError("Tanto el peso como el valor del ítem deben ser positivos.")
        self.peso = float(peso)
        self.valor = float(valor)

    def __repr__(self):
        return f"Item(peso={self.peso}, valor={self.valor})"

    @property
    def ratio_valor_peso(self):
        """Calcula y devuelve la relación valor/peso del ítem."""
        return self.valor / self.peso


class SolucionMochila:
    """Almacena el resultado de los ítems seleccionados.

    Similar a 'Subconjunto' en la versión exhaustiva, pero renombrada
    para mayor claridad en el contexto del problema.
    """

    def __init__(self):
        self.items = []

    def agregar_item(self, item):
        self.items.append(item)

    def obtener_peso_total(self):
        """Calcula la suma de los pesos de los ítems en la solución."""
        return sum(item.peso for item in self.items)

    def obtener_valor_total(self):
        """Calcula la suma de los valores de los ítems en la solución."""
        return sum(item.valor for item in self.items)


class EstrategiaMochilaGreedy:
    """Implementa el algoritmo voraz para resolver el problema de la mochila.

    La estrategia consiste en seleccionar ítems basándose en la mejor relación
    valor/peso.
    """

    def resolver(self, mochila, items):
        """Selecciona los mejores ítems para la mochila usando una estrategia voraz.

        Args:
            mochila (Mochila): La mochila a llenar.
            items (list[Item]): La lista de ítems disponibles.

        Returns:
            SolucionMochila: La solución encontrada con los ítems seleccionados.
        """
        # Ordena los ítems de mayor a menor según su ratio valor/peso.
        items_ordenados = sorted(items, key=lambda item: item.ratio_valor_peso, reverse=True)

        solucion = SolucionMochila()
        peso_actual = 0.0

        for item in items_ordenados:
            if peso_actual + item.peso <= mochila.peso:
                solucion.agregar_item(item)
                peso_actual += item.peso

        return solucion


class Programa:
    """Clase de utilidad para ejecutar el programa principal."""

    @staticmethod
    def main():
        """Punto de entrada principal de la aplicación."""
        try:
            mochila = Mochila(3000)
            items_disponibles = [
                Item(1800, 72),
                Item(600, 36),
                Item(1200, 60)
            ]

            estrategia = EstrategiaMochilaGreedy()
            mejor_solucion = estrategia.resolver(mochila, items_disponibles)

            print("La solución GULOSA contiene los siguientes ítems: ")
            for item in mejor_solucion.items:
                print(
                    f"  - Peso: {item.peso:<5} gr | Valor: ${item.valor:<5} | Ratio: {item.ratio_valor_peso:.2f}")

            print("\n--------------------------------------------------")
            print(
                f"Peso total: {mejor_solucion.obtener_peso_total()} gr (Capacidad: {mochila.peso} gr)"
                f"\nValor total:   ${mejor_solucion.obtener_valor_total()}"
            )
            print("--------------------------------------------------")

        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    Programa.main()