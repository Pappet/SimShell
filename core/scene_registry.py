"""
Module core/scene_registry.py

Provides a central registry for mapping scene keys to scene factory classes,
enabling dynamic scene lookup and instantiation.
Includes a decorator for easy scene registration.
"""

# Central registry mapping string keys to scene factory classes
scene_registry: dict[str, type] = {}


def register_scene(key: str, scene_factory: type) -> None:
    """
    Register a scene factory class under the given key.

    Args:
        key (str): Unique identifier for the scene.
        scene_factory (type): The scene class to instantiate for this key.
    """
    scene_registry[key] = scene_factory


def scene(key: str) -> callable:
    """
    Class decorator that registers the decorated scene class in `scene_registry`.

    The decorated class must implement an __init__ accepting at least:
    - context: GameContext providing shared services
    - switch_scene_callback: Callable to trigger scene transitions
    Optionally can accept exit_callback for scenes that handle exit actions.

    Usage:
        @scene("menu")
        class MainMenuScene:
            ...

    Args:
        key (str): The registry key for the scene.

    Returns:
        Callable: Decorator function for scene classes.
    """
    def decorator(cls: type) -> type:
        register_scene(key, cls)
        return cls
    return decorator
