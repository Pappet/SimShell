"""
Module core/plugin_manager.py

Implements PluginManager, responsible for discovering, loading, enabling,
and disabling game plugins. Reads plugin manifests, resolves dependencies,
and dispatches lifecycle hooks (on_init, on_start, on_event, etc.) to
active plugins.
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
    Manage plugin lifecycle and event dispatching.

    Responsibilities:
    - Discover plugin manifests under configured plugins_path
    - Resolve dependency graph and load enabled plugins in correct order
    - Enable or disable plugins at runtime, updating manifests
    - Dispatch plugin hooks: on_init, on_start, on_event, on_update,
      on_render, on_shutdown
    """

    def __init__(self, app: Any):
        """
        Initialize the PluginManager.

        Args:
            app (Any): Reference to the GameApp instance for plugin callbacks.
        """
        # Reference to main application for callback context
        self.app = app
        # Base directory where plugins are stored
        self.plugin_base = Path(paths["plugins_path"])
        # List of available plugin metadata dictionaries
        self.available: List[Dict[str, Any]] = self._discover_plugins(self.plugin_base)
        # Map of plugin name to set of dependents
        self.dependents: Dict[str, Set[str]] = self._build_dependents_map()
        # Loaded plugin instances by module path
        self.loaded: Dict[str, Any] = {}
        # Ordered list of active plugin instances
        self.plugins: List[Any] = []

    def _discover_plugins(self, base_dir: Path) -> List[Dict[str, Any]]:
        """
        Scan subdirectories for plugin.yaml manifests and collect metadata.

        Args:
            base_dir (Path): Directory to search for plugin subdirectories.

        Returns:
            List[Dict[str, Any]]: Metadata for each discovered plugin.
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
                logger.debug("Skipping '%s': no manifest found.", sub)
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
                logger.error(
                    "Error reading manifest '%s': %s", manifest, e, exc_info=True
                )
        return plugins

    def _build_dependents_map(self) -> Dict[str, Set[str]]:
        """
        Construct reverse dependency map: plugin -> set of plugins depending on it.

        Returns:
            Dict[str, Set[str]]: Mapping of plugin names to their dependents.
        """
        # Map each plugin to its declared dependencies
        deps = {m["name"]: set(m.get("depends", [])) for m in self.available}
        # Initialize empty set of dependents for each plugin
        dependents: Dict[str, Set[str]] = {name: set() for name in deps}
        # Fill in dependents from dependencies
        for name, reqs in deps.items():
            for dep in reqs:
                if dep in dependents:
                    dependents[dep].add(name)
                else:
                    logger.warning(
                        "Unknown dependency '%s' for plugin '%s'.", dep, name
                    )
        return dependents

    def _resolve_load_order(self) -> List[str]:
        """
        Compute load order for enabled plugins via topological sort.

        Returns:
            List[str]: Names of enabled plugins in correct load order.
        """
        # Filter only enabled plugins and copy their dependency sets
        deps = {
            m["name"]: set(m.get("depends", []))
            for m in self.available if m["enabled"]
        }
        order: List[str] = []
        # Start with plugins without dependencies
        queue = [name for name, reqs in deps.items() if not reqs]

        while queue:
            name = queue.pop(0)
            order.append(name)
            # Remove this plugin from its dependents' dependency sets
            for child in list(self.dependents.get(name, [])):
                if child in deps:
                    deps[child].discard(name)
                    if not deps[child]:
                        queue.append(child)
            deps.pop(name, None)

        if deps:
            logger.error(
                "Circular or missing dependencies detected: %s", deps
            )
            # Fallback: load in discovery order
            return [m["name"] for m in self.available if m["enabled"]]
        return order

    def load_plugins(self) -> None:
        """
        Load and initialize all enabled plugins in resolved order.
        """
        for name in self._resolve_load_order():
            meta = next((m for m in self.available if m["name"] == name), None)
            if meta:
                self._load(meta)

    def _load(self, meta: Dict[str, Any]) -> None:
        """
        Import the plugin module, instantiate PluginImpl, and call on_init.

        Args:
            meta (Dict[str, Any]): Metadata for the plugin.
        """
        module_path = meta["module"]
        try:
            module = importlib.import_module(module_path)
            cls = getattr(module, "PluginImpl")
            instance = cls(self.app)
            self.loaded[module_path] = instance
            self.plugins.append(instance)
            # Invoke plugin initialization hook
            if hasattr(instance, "on_init"):
                instance.on_init()
            logger.info("Loaded plugin: %s", meta["name"])
        except Exception:
            logger.exception(
                "Failed to load plugin '%s'.", meta["name"]
            )

    def enable_plugin(self, name: str) -> None:
        """
        Enable a plugin and its dependencies, then persist enabled state.

        Args:
            name (str): Name of the plugin to enable.
        """
        meta = next((m for m in self.available if m["name"] == name), None)
        if not meta or meta["enabled"]:
            return

        # Ensure dependencies are enabled first
        for dep in meta.get("depends", []):
            self.enable_plugin(dep)

        # Mark enabled and update manifest
        meta["enabled"] = True
        data = safe_load(meta["manifest"].read_text(encoding="utf-8")) or {}
        data["enabled"] = True
        meta["manifest"].write_text(safe_dump(data, sort_keys=False))

        # Load the newly enabled plugin
        self._load(meta)
        logger.info("Enabled plugin: %s", name)

    def disable_plugin(self, name: str) -> None:
        """
        Disable a plugin and all its dependents, call on_shutdown, then persist.

        Args:
            name (str): Name of the plugin to disable.
        """
        meta = next((m for m in self.available if m["name"] == name), None)
        if not meta or not meta["enabled"]:
            return

        # Recursively disable dependents first
        for child in list(self.dependents.get(name, [])):
            self.disable_plugin(child)

        # Remove from loaded plugins
        module_path = meta["module"]
        instance = self.loaded.pop(module_path, None)
        if instance in self.plugins:
            self.plugins.remove(instance)
        # Invoke shutdown hook if available
        if instance and hasattr(instance, "on_shutdown"):
            try:
                instance.on_shutdown()
                logger.info("Called on_shutdown for plugin: %s", name)
            except Exception:
                logger.exception(
                    "Error in on_shutdown of plugin '%s'.", name
                )

        # Persist disabled state to manifest
        meta["enabled"] = False
        data = safe_load(meta["manifest"].read_text(encoding="utf-8")) or {}
        data["enabled"] = False
        meta["manifest"].write_text(safe_dump(data, sort_keys=False))
        logger.info("Disabled plugin: %s", name)

    # Plugin lifecycle dispatchers
    def on_init(self) -> None:
        """Dispatch on_init to all active plugins."""
        self._dispatch("on_init")

    def on_start(self) -> None:
        """Dispatch on_start to all active plugins."""
        self._dispatch("on_start")

    def on_event(self, event: Any) -> None:
        """Dispatch on_event to all active plugins with the event."""
        self._dispatch("on_event", event)

    def on_update(self, dt: float) -> None:
        """Dispatch on_update to all active plugins with delta time."""
        self._dispatch("on_update", dt)

    def on_render(self, surface: Any) -> None:
        """Dispatch on_render to all active plugins with the surface."""
        self._dispatch("on_render", surface)

    def on_shutdown(self) -> None:
        """Dispatch on_shutdown to all active plugins."""
        self._dispatch("on_shutdown")

    def _dispatch(self, hook_name: str, *args: Any, **kwargs: Any) -> None:
        """
        Internal helper to call a given hook on every plugin.

        Args:
            hook_name (str): Name of the hook to invoke on each plugin.
            *args: Positional arguments to forward to the plugin hook.
            **kwargs: Keyword arguments to forward to the plugin hook.
        """
        for plugin in list(self.plugins):
            fn = getattr(plugin, hook_name, None)
            if callable(fn):
                try:
                    fn(*args, **kwargs)
                except Exception:
                    logger.exception(
                        "Error in plugin '%s'.%s", plugin, hook_name
                    )
