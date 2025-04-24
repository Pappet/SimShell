# core/plugin_manager.py

"""
PluginManager is responsible for discovering, loading, enabling, and disabling plugins.
It reads plugin manifests, resolves dependencies, and dispatches plugin lifecycle hooks.
"""

import importlib
import logging
from pathlib import Path
from typing import Any, Dict, List, Set

from yaml import safe_load, safe_dump

from setup.config import paths

logger = logging.getLogger(__name__)

class PluginManager:
    """
    Manages plugin lifecycle: discovery, dependency resolution, loading,
    enabling/disabling, and hook dispatching.
    """
    def __init__(self, app: Any):
        """
        Initialize the PluginManager.

        Args:
            app (Any): Reference to the main application instance.
        """
        self.app = app
        self.plugin_base = Path(paths["plugins_path"])
        self.available: List[Dict[str, Any]] = self._discover_plugins(self.plugin_base)
        self.dependents: Dict[str, Set[str]] = self._build_dependents_map()
        self.loaded: Dict[str, Any] = {}
        self.plugins: List[Any] = []

    def _discover_plugins(self, base_dir: Path) -> List[Dict[str, Any]]:
        """
        Scan subdirectories for plugin.yaml manifests.

        Returns:
            List of plugin metadata dictionaries.
        """
        plugins: List[Dict[str, Any]] = []
        if not base_dir.exists():
            logger.warning("Plugins directory '%s' not found.", base_dir)
            return plugins

        for sub in base_dir.iterdir():
            if not sub.is_dir():
                continue
            manifest = sub / "plugin.yaml"
            if not manifest.exists():
                logger.debug("Skipping '%s': no manifest.", sub)
                continue
            try:
                data = safe_load(manifest.read_text(encoding="utf-8")) or {}
                plugins.append({
                    "name": data["name"],
                    "module": data["module"],
                    "enabled": data.get("enabled", False),
                    "depends": data.get("depends", []),
                    "manifest": manifest,
                })
                logger.info("Discovered plugin: %s", data["name"])
            except Exception as e:
                logger.error("Error reading manifest '%s': %s", manifest, e, exc_info=True)
        return plugins

    def _build_dependents_map(self) -> Dict[str, Set[str]]:
        """
        Build a mapping from plugin names to sets of dependents.

        Returns:
            A dict where keys are plugin names and values are sets of names depending on the key.
        """
        deps = {m["name"]: set(m.get("depends", [])) for m in self.available}
        dependents: Dict[str, Set[str]] = {name: set() for name in deps}
        for name, reqs in deps.items():
            for dep in reqs:
                if dep in dependents:
                    dependents[dep].add(name)
                else:
                    logger.warning("Unknown dependency '%s' for plugin '%s'.", dep, name)
        return dependents

    def _resolve_load_order(self) -> List[str]:
        """
        Resolve plugin load order with topological sort of enabled plugins.

        Returns:
            Ordered list of plugin names.
        """
        deps = {m["name"]: set(m.get("depends", [])) for m in self.available if m["enabled"]}
        order: List[str] = []
        queue = [n for n, reqs in deps.items() if not reqs]

        while queue:
            name = queue.pop(0)
            order.append(name)
            for child in list(self.dependents.get(name, [])):
                if child in deps:
                    deps[child].discard(name)
                    if not deps[child]:
                        queue.append(child)
            deps.pop(name, None)

        if deps:
            logger.error("Circular or missing dependencies detected: %s", deps)
            return [m["name"] for m in self.available if m["enabled"]]
        return order

    def load_plugins(self) -> None:
        """
        Load all enabled plugins in resolved order.
        """
        for name in self._resolve_load_order():
            meta = next((m for m in self.available if m["name"] == name), None)
            if meta:
                self._load(meta)

    def _load(self, meta: Dict[str, Any]) -> None:
        """
        Import a plugin module and call its on_init.

        Args:
            meta: Metadata dict for the plugin.
        """
        module_path = meta["module"]
        try:
            module = importlib.import_module(module_path)
            cls = getattr(module, "PluginImpl")
            instance = cls(self.app)
            self.loaded[module_path] = instance
            self.plugins.append(instance)
            if hasattr(instance, "on_init"):
                instance.on_init()
            logger.info("Loaded plugin: %s", meta["name"])
        except Exception:
            logger.exception("Failed to load plugin '%s'.", meta["name"])

    def enable_plugin(self, name: str) -> None:
        """
        Enable a plugin and its dependencies, then save manifest.

        Args:
            name: Plugin name to enable.
        """
        meta = next((m for m in self.available if m["name"] == name), None)
        if not meta or meta["enabled"]:
            return

        for dep in meta.get("depends", []):
            self.enable_plugin(dep)

        meta["enabled"] = True
        data = safe_load(meta["manifest"].read_text(encoding="utf-8")) or {}
        data["enabled"] = True
        meta["manifest"].write_text(safe_dump(data, sort_keys=False))
        self._load(meta)
        logger.info("Enabled plugin: %s", name)

    def disable_plugin(self, name: str) -> None:
        """
        Disable a plugin and its dependents, call on_shutdown, and save manifest.

        Args:
            name: Plugin name to disable.
        """
        meta = next((m for m in self.available if m["name"] == name), None)
        if not meta or not meta["enabled"]:
            return

        for child in list(self.dependents.get(name, [])):
            self.disable_plugin(child)

        module_path = meta["module"]
        instance = self.loaded.pop(module_path, None)
        if instance in self.plugins:
            self.plugins.remove(instance)
        if instance and hasattr(instance, "on_shutdown"):
            try:
                instance.on_shutdown()
                logger.info("Called on_shutdown for plugin: %s", name)
            except Exception:
                logger.exception("Error in on_shutdown of plugin '%s'.", name)

        meta["enabled"] = False
        data = safe_load(meta["manifest"].read_text(encoding="utf-8")) or {}
        data["enabled"] = False
        meta["manifest"].write_text(safe_dump(data, sort_keys=False))
        logger.info("Disabled plugin: %s", name)

    def on_init(self) -> None:
        self._dispatch("on_init")

    def on_start(self) -> None:
        self._dispatch("on_start")

    def on_event(self, event: Any) -> None:
        self._dispatch("on_event", event)

    def on_update(self, dt: float) -> None:
        self._dispatch("on_update", dt)

    def on_render(self, surface: Any) -> None:
        self._dispatch("on_render", surface)

    def on_shutdown(self) -> None:
        self._dispatch("on_shutdown")

    def _dispatch(self, hook_name: str, *args: Any, **kwargs: Any) -> None:
        """
        Dispatch a plugin hook to all active plugins.

        Args:
            hook_name: Name of the plugin hook method.
        """
        for plugin in list(self.plugins):
            fn = getattr(plugin, hook_name, None)
            if callable(fn):
                try:
                    fn(*args, **kwargs)
                except Exception:
                    logger.exception("Error in plugin '%s'.%s", plugin, hook_name)
