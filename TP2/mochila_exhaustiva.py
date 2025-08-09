import sys


class Mochila:
    def __init__(self, volumen):
        self.volumen = float(volumen)


class ConjuntoItems:
    def __init__(self):
        self.items = []  # Lista de Item
        self.subconjuntos = []  # Lista de Subconjunto

    def generar_subconjuntos(self):
        n = len(self.items)
        power_set_count = 1 << n  # 2^n

        for set_mask in range(power_set_count):
            subconjunto = Subconjunto()
            for i in range(n):
                if (set_mask & (1 << i)) > 0:
                    subconjunto.items.append(self.items[i])
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
