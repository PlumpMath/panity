from object import Object
from properties import SerializedProperty

class Component(Object):
    """base class for everything that can be attached to game objects."""

    def __init__(self, game_object):
        Object.__init__(self)
        self.game_object = game_object

    @classmethod
    def getAttributes(cls):
        """return all special property attributes."""
        d = {}
        for a, b in cls.__dict__.items():
            if isinstance(b, SerializedProperty):
                d[a] = b
        return d
