import sys


class Mochila:
    def __init__(self, volumen):
        self.volumen = float(volumen)


class ConjuntoItems:
    """
        Representa un conjunto de ítems
    """
    def __init__(self):
        self.items = []  # Lista de Item
        self.subconjuntos = []  # Lista de Subconjunto

    def generar_subconjuntos(self):
        """
        Genera todos los subconjuntos posibles de la lista de ítems actual
        usando una representación con máscaras de bits.

        Cada subconjunto se crea recorriendo todos los números binarios desde
        0 hasta (2^n - 1), donde n es la cantidad de ítems. Si el bit i del
        número está encendido, se incluye el ítem correspondiente en el
        subconjunto.

        El resultado se guarda en self.subconjuntos.
        """
        n = len(self.items)
        power_set_count = 1 << n  # 2^n: usamos números binarios para representar cada subconjunto

        # Iteramos a través de todos los números posibles desde 0 hasta 2^n - 1.
        # Cada número (set_mask) actúa como una "máscara de bits" que representa un subconjunto único.
        for set_mask in range(power_set_count):
            subconjunto = Subconjunto()
            # Para cada máscara, revisamos cada uno de los n ítems.
            for i in range(n):
                # Esta es la operación clave: (1 << i) crea un número donde solo el i-ésimo bit es 1 (ej: 001, 010, 100).
                # La operación AND a nivel de bits (&) comprueba si el i-ésimo bit está "encendido" en la máscara actual.
                # Si el resultado es mayor que 0, significa que el ítem en la posición 'i' pertenece a este subconjunto.
                if (set_mask & (1 << i)) > 0:
                    # Agregamos el ítem correspondiente a nuestro subconjunto temporal.
                    subconjunto.items.append(self.items[i])
            # Una vez que hemos comprobado todos los ítems para la máscara actual, añadimos el subconjunto completo a nuestra lista.
            self.subconjuntos.append(subconjunto)


class Item:
    def __init__(self, volumen, valor):
        self.volumen = float(volumen)
        self.valor = float(valor)


class Subconjunto:
    def __init__(self):
        self.items = []  # Lista de Item

    def volumen(self):
        volumen_total = 0.0
        for item in self.items:
            volumen_total += item.volumen
        return volumen_total

    def valor(self):
        valor_total = 0.0
        for item in self.items:
            valor_total += item.valor
        return valor_total


class Controlador:
    def __init__(self, mochila, conjuntoItems):
        self.mochila = mochila
        self.conjuntoItems = conjuntoItems

    def mejor_subconjunto(self):
        self.conjuntoItems.generar_subconjuntos()
        subconjuntos = self.conjuntoItems.subconjuntos

        mejor_subconjunto = None
        mejor_valor = 0.0

        for subconjunto in subconjuntos:
            if subconjunto.volumen() <= self.mochila.volumen:
                valor = subconjunto.valor()
                if valor > mejor_valor:
                    mejor_subconjunto = subconjunto
                    mejor_valor = valor

        return mejor_subconjunto


class Programa:
    @staticmethod
    def main(args):
        mochila = Mochila(4200)
        conjunto = ConjuntoItems()
        items = conjunto.items
        items.append(Item(150, 20))
        items.append(Item(325, 40))
        items.append(Item(600, 50))
        items.append(Item(805, 36))
        items.append(Item(430, 25))
        items.append(Item(1200, 64))
        items.append(Item(770, 54))
        items.append(Item(60, 18))
        items.append(Item(930, 46))
        items.append(Item(353, 28))

        controlador = Controlador(mochila, conjunto)
        mejor_subconjunto = controlador.mejor_subconjunto()

        print("La solución contiene los siguientes ítems: ")
        for item in mejor_subconjunto.items:
            print(f"Volumen: {item.volumen} cm3    Valor: ${item.valor}")

        print(
            f"Volumen total: {mejor_subconjunto.volumen()} cm3 "
            f"Valor total: ${mejor_subconjunto.valor()}"
        )


if __name__ == "__main__":
    Programa.main(sys.argv[1:])
