from entities.path import Path


class Route:
    """Clase que representa al objeto ruta.

        Atributos:
        paths -- Conjunto de caminos que debe tomar el bus para completar la ruta
        block -- Indica si la ruta se encuentra bloqueada
        code -- Identificador único de la ruta

        """

    __paths: []
    __block: bool
    __code: int

    def __init__(self, code: int):
        self.__paths = []
        self.__block = False
        self.__code = code

    def __eq__(self, other_route):
        return self.__code == other_route.get_code()

    def __str__(self):
        str_paths = ""
        for path in self.__paths:
            str_paths += str(path.get_code()) + " "
        return "Route " + str(self.__code) + " Paths " + str_paths

    def encode(self):
        paths = []
        for path in self.__paths:
            paths.append(path.get_code())
        return dict(isBlock=self.__block, paths=paths)

    def get_code(self):
        return self.__code

    def add_path(self, path: Path):
        self.__paths.append(path)

    def get_paths(self) -> []:
        return self.__paths

    def block(self):
        self.__block = True

    def unblock(self):
        self.__block = False

    def is_block(self):
        return self.__block
