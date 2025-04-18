import pytest
from core.scene_registry import scene_registry, register_scene, scene


@pytest.fixture(autouse=True)
def clear_registry_before_tests():
    # Ensure registry is empty before each test
    scene_registry.clear()


def test_register_scene_adds_entry():
    # dummy factory
    def factory(context, callback):
        return ('scene', context, callback)

    register_scene('test_key', factory)
    assert 'test_key' in scene_registry
    assert scene_registry['test_key'] is factory


def test_register_scene_overwrites_existing():
    def factory1(ctx, cb): return 1
    def factory2(ctx, cb): return 2

    register_scene('key', factory1)
    assert scene_registry['key'] is factory1

    register_scene('key', factory2)
    assert scene_registry['key'] is factory2


def test_scene_decorator_registers_class():
    # Use decorator to register a dummy class
    @scene('decorated')
    class Dummy:
        def __init__(self, context, callback):
            pass

    # After decoration, registry should contain Dummy under 'decorated'
    assert 'decorated' in scene_registry
    assert scene_registry['decorated'] is Dummy


def test_scene_decorator_returns_original_class():
    @scene('foo')
    class MyScene:
        pass

    # Decorator should return the class itself
    assert MyScene.__name__ == 'MyScene'
    assert isinstance(MyScene, type)
    # Registry entry also refers to the same class object
    assert scene_registry['foo'] is MyScene
