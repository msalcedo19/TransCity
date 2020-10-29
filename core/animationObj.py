from entities.path import *
from entities.bus import *


class AnimationObject:
    """Clase encargada de llevar el estado de la animación del recorrido de un bus"""

    def __init__(self, x, y, actual_path: Path, paths_left, actual_bus: Bus, id_object):
        self.x = x
        self.y = y
        self.actual_path: Path = actual_path
        self.paths_left = paths_left
        self.actual_bus: Bus = actual_bus
        self.id_object = id_object
        self.actual_type_path = MoveTypeV2.DIAG_DER_ABJ

    def set_value(self, **kwargs):
        if kwargs.get('x'):
            self.x = kwargs['x']
        if kwargs.get('y'):
            self.y = kwargs['y']
        if kwargs.get('actual_path'):
            self.actual_path = kwargs['actual_path']
        if kwargs.get('paths_left'):
            self.paths_left = kwargs['paths_left']
        if kwargs.get('actual_bus'):
            self.actual_bus = kwargs['actual_bus']
        if kwargs.get('id_object'):
            self.id_object = kwargs['id_object']
