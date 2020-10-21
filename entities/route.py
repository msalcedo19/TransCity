from entities.path import Path


class Route:
    __paths: []
    __block: bool
    __code: int

    def __init__(self, code: int):
        self.__paths = []
        self.__block = False
        self.__code = code

    def encode(self):
        return dict(code=self.__code, isBlock=self.__block)

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
