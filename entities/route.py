from entities.path import Path


class Route:
    __paths: []
    __block: bool

    def __init__(self):
        self.__paths = []
        self.__block = False

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
