from utils.generator import Generator
from utils.GUI import GUI
"""Clase que representa al objeto bus.

    Devuelve en una tupla las dos raíces que resuelven la
    ecuación cuadrática:

        ax^2 + bx + c = 0.

    Utiliza la fórmula general (también conocida
    coloquialmente como el "chicharronero").

    Parámetros:
    a -- coeficiente cuadrático (debe ser distinto de 0)
    b -- coeficiente lineal
    c -- término independiente

    Excepciones:
    ValueError -- Si (a == 0)

    """


def main():
    gen = Generator()
    gen.load_map()
    GUI(gen)


main()

