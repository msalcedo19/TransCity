from entities.path import Path


class Route:
    __paths: []

    def __init__(self):
        self.__paths = []

    def add_path(self, path: Path):
        self.__paths.append(path)

    def get_paths(self) -> []:
        return self.__paths
