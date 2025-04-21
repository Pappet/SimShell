# core/scene_registry.py

# Central registry for scenes
scene_registry = {}

def register_scene(key, scene_factory):
    """Adds a scene to the registry."""
    scene_registry[key] = scene_factory

def scene(key):
    """
    Decorator that registers a scene class in the registry.
    The decorated class must have a constructor
    that accepts (context, switch_scene_callback).
    """
    def decorator(cls):
        register_scene(key, cls)
        return cls
    return decorator
