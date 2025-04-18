# core/decorators.py
import logging

logger = logging.getLogger(__name__)

def ensure_key(func):
    def wrapper(self, key, *args, **kwargs):
        if key not in self._stat_configs:
            logger.warning(f"Stat '{key}' not found. Cannot {func.__name__}.")
            return 0 if func.__name__ == "get" else False
        return func(self, key, *args, **kwargs)
    return wrapper