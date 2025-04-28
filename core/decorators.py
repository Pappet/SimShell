"""
Module core/decorators.py

Provides decorators for internal consistency checks in managers.
Currently includes `ensure_key` to validate stat keys before method execution.
"""

import logging

logger = logging.getLogger(__name__)


def ensure_key(func):
    """
    Decorator that ensures a given key exists in the `_stat_configs` mapping.

    This prevents operations on undefined statistics by checking membership
    in `self._stat_configs`. If the key is missing, logs a warning and
    returns a safe default (0 for getters, False for setters/modifiers).

    Args:
        func (Callable): The stat manager method to wrap (e.g., get, set, modify).

    Returns:
        Callable: Wrapped function that checks key validity before calling.
    """
    def wrapper(self, key, *args, **kwargs):
        # Verify the statistic key is registered
        if key not in self._stat_configs:
            logger.warning(
                f"Stat '{key}' not found. Cannot {func.__name__}."
            )
            # Return default based on method intent: getters return 0, others False
            return 0 if func.__name__ == "get" else False
        # Forward to the original method if the key is valid
        return func(self, key, *args, **kwargs)

    return wrapper
