# core/decorators.py

def ensure_key(func):
    def wrapper(self, key, *args, **kwargs):
        if key not in self._stat_configs:
            self.debug_console.log(f"Stat '{key}' not found. Cannot {func.__name__}.")
            return 0 if func.__name__ == "get" else False
        return func(self, key, *args, **kwargs)
    return wrapper