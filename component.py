from object import Object
from properties import SerializedProperty

class Component(Object):
    """Base class for everything that can be attached to game objects.
    You need to subclass this class for it to be useful.
    """

    # These special attributes are mapped in __getattr__ to components.
    # That said you can write
    #    any_component.camera
    # instead of the longer
    #    any_component.game_object.getComponent("camera")
    special_attrs = set(["rigidbody", "camera", "light", "animation",
                        "constant_force", "renderer", "audio", "gui_text",
                        "network_view", "gui_texture", "collider", "hinge_joint",
                        "particle_emitter", "particle_system"])

    def __init__(self, game_object):
        Object.__init__(self)
        # add the component to the game object's components dict
        assert not game_object.components.has_key(type(self).__name__)
        game_object.components[type(self).__name__] = self
        self.game_object = game_object

    def destroy(self):
        """Clean up. This method can be overridden in subclasses."""
        pass


    @classmethod
    def getClassSerializedProperties(cls):
        """Return all special property attributes in a dict. Only attributes
        derived from SerializedProperty are respected.
        """
        d = {}
        for a, b in cls.__dict__.items():
            if isinstance(b, SerializedProperty):
                d[a] = b
        return d

    def getSerializedProperties(self):
        """Return all special property attributes' values in a dict.
        Only attributes derived from SerializedProperty are respected.
        """
        d = {}
        for p, v in type(self).getClassSerializedProperties().iteritems():
            d[p] = v.getValue(self)
        return d
    
    def __getattr__(self, name):
        if name in Component.special_attrs:
            return self.game_object.getComponent(name)
        else:
            s = "Component '{}' of game object '{}' has no attribute '{}'".format(
                type(self).__name__, self.game_object, name)
            raise AttributeError(s)
