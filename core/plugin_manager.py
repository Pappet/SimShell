# core/plugin_manager.py
import importlib
import logging
import os, pkgutil, importlib
from setup.config import plugins, save


logger = logging.getLogger(__name__)

class PluginManager:
    def __init__(self, app):
        self.app = app
        self.plugins = []
        # alle Plugins‑Metadaten
        self.available  = plugins
        # Instanzen geladener Plugins
        self.loaded     = {}

    def load_plugins(self):
        for meta in self.available:
            if meta.get("enabled", False):
                self._load(meta)

    def _load(self, meta):
        module_path = meta["module"]
        try:
            mod = importlib.import_module(module_path)
            cls = getattr(mod, "PluginImpl")
            inst = cls(self.app)
            self.loaded[module_path] = inst
            self.plugins.append(inst)
            if inst and hasattr(inst, "on_init"):
                inst.on_init()
            logger.info("Plugin geladen: %s", meta["name"])
        except Exception:
            logger.exception("Fehler beim Laden von %s", meta["name"])

    def _call(self, hook_name, *args, **kwargs):
        for plugin in self.plugins:
            fn = getattr(plugin, hook_name, None)
            if callable(fn):
                try:
                    fn(*args, **kwargs)
                except Exception:
                    logger.exception("Plugin‑Fehler in %s.%s", plugin, hook_name)

    def enable_plugin(self, name):
        meta = next(m for m in self.available if m["name"] == name)
        if not meta.get("enabled"):
            meta["enabled"] = True
            self._load(meta)
            save()
            logger.info("Plugin aktiviert: %s", name)

    def disable_plugin(self, name):
        meta = next(m for m in self.available if m["name"] == name)
        if meta.get("enabled"):
            meta["enabled"] = False
            inst = self.loaded.pop(meta["module"], None)
            print(meta["module"])
            if inst and hasattr(inst, "on_shutdown"):
                inst.on_shutdown()
            save()
            logger.info("Plugin deaktiviert: %s", name)

    # for every Hook a Wrapper
    def on_init(self):     self._call("on_init")
    def on_start(self):    self._call("on_start")
    def on_event(self, e): self._call("on_event", e)
    def on_update(self, dt): self._call("on_update", dt)
    def on_render(self, surf): self._call("on_render", surf)
    def on_shutdown(self):  self._call("on_shutdown")
