# core/plugin_manager.py

import os
import importlib
import logging
from pathlib import Path

import yaml  # verlangt, dass PyYAML installiert ist
from setup.config import paths, save

logger = logging.getLogger(__name__)

class PluginManager:
    """
    Verantwortlich für:
      - Discovery aller Plugins im Ordner paths['plugins_path']
      - Einlesen der plugin.yaml-Manifeste (name, module, enabled, depends)
      - Abhängigkeits-Auflösung (topologische Sortierung)
      - Laden (on_init), Aktivieren, Deaktivieren (on_shutdown) von Plugins
      - Hook-Dispatcher (on_update, on_render, etc.)
    """

    def __init__(self, app):
        self.app         = app
        self.plugin_base = Path(paths["plugins_path"])
        # 1) alle Manifeste einlesen
        self.available   = self._discover_plugins(self.plugin_base)
        # 2) Dependents-Map bauen (wer hängt von wem ab)
        self.dependents  = self._build_dependents_map()
        # 3) geladene Instanzen speichern
        self.loaded      = {}   # module_path -> instance
        self.plugins     = []   # Liste der aktiven Plugin-Instanzen

    def _discover_plugins(self, base_dir: Path):
        """Scannt Unterordner und liest plugin.yaml in jedem ein."""
        plugins = []
        if not base_dir.exists():
            logger.warning(f"Plugin-Verzeichnis '{base_dir}' nicht gefunden.")
            return plugins

        for sub in base_dir.iterdir():
            if not sub.is_dir():
                continue
            manifest = sub / "plugin.yaml"
            if not manifest.exists():
                logger.debug(f"Kein Manifest in {sub}, übersprungen.")
                continue
            try:
                data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
                plugins.append({
                    "name":    data["name"],
                    "module":  data["module"],
                    "enabled": data.get("enabled", False),
                    "depends": data.get("depends", []),
                    "manifest": manifest,
                })
                logger.info(f"Plugin entdeckt: {data['name']}")
            except Exception as e:
                logger.error(f"Fehler beim Lesen von {manifest}: {e}", exc_info=True)
        return plugins

    def _build_dependents_map(self):
        """Invertiert 'depends' zu einer Dependents-Map."""
        deps = {m["name"]: set(m.get("depends", [])) for m in self.available}
        dependents = {name: set() for name in deps}
        for name, reqs in deps.items():
            for dep in reqs:
                if dep in dependents:
                    dependents[dep].add(name)
                else:
                    logger.warning(f"Unbekannte Abhängigkeit '{dep}' in Plugin '{name}'")
        return dependents

    def _resolve_load_order(self):
        """
        Topologische Sortierung aller aktivierten Plugins.
        Gibt eine Liste von Plugin-Namen in Lade-Reihenfolge zurück.
        """
        # working copy der Abhängigkeiten (nur enabled)
        deps = {
            m["name"]: set(m.get("depends", []))
            for m in self.available if m["enabled"]
        }
        order = []
        # alle ohne deps zuerst
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
            # Kreis oder fehlende Abhängigkeit
            logger.error(f"Zirkuläre oder fehlende Abhängigkeiten: {deps}")
            # fallback: in Originalreihenfolge
            return [m["name"] for m in self.available if m["enabled"]]
        return order

    def load_plugins(self):
        """Lädt alle Plugins nach Abhängigkeits-Reihenfolge."""
        for name in self._resolve_load_order():
            meta = next((m for m in self.available if m["name"] == name), None)
            if meta:
                self._load(meta)

    def _load(self, meta):
        """Importiert ein einzelnes Plugin-Modul und ruft on_init() auf."""
        module_path = meta["module"]
        try:
            mod = importlib.import_module(module_path)
            cls = getattr(mod, "PluginImpl")
            inst = cls(self.app)
            self.loaded[module_path] = inst
            self.plugins.append(inst)
            if hasattr(inst, "on_init"):
                inst.on_init()
            logger.info("Plugin geladen: %s", meta["name"])
        except Exception:
            logger.exception("Fehler beim Laden von %s", meta["name"])

    def enable_plugin(self, name: str):
        """
        Aktiviert ein Plugin und all seine Dependencies rekursiv.
        Speichert danach die Config.
        """
        meta = next((m for m in self.available if m["name"] == name), None)
        if not meta or meta["enabled"]:
            return

        # Dependencies zuerst aktivieren
        for dep in meta.get("depends", []):
            dep_meta = next((m for m in self.available if m["name"] == dep), None)
            if dep_meta and not dep_meta["enabled"]:
                self.enable_plugin(dep)

        # dieses Plugin aktivieren
        meta["enabled"] = True
        mdata = yaml.safe_load(meta["manifest"].read_text()) or {}
        mdata["enabled"] = True
        meta["manifest"].write_text(yaml.safe_dump(mdata, sort_keys=False))
        self._load(meta)
        logger.info("Plugin aktiviert: %s", name)

    def disable_plugin(self, name: str):
        """
        Deaktiviert ein Plugin und alle davon abhängigen Plugins rekursiv.
        Ruft on_shutdown() jedes Plugin ab, entfernt Instanz und speichert Config.
        """
        meta = next((m for m in self.available if m["name"] == name), None)
        if not meta or not meta["enabled"]:
            return

        # zuerst alle Dependents ausschalten
        for child in list(self.dependents.get(name, [])):
            child_meta = next((m for m in self.available if m["name"] == child), None)
            if child_meta and child_meta["enabled"]:
                self.disable_plugin(child)

        # dann dieses Plugin
        module_path = meta["module"]
        inst = self.loaded.pop(module_path, None)
        if inst in self.plugins:
            self.plugins.remove(inst)
        if inst and hasattr(inst, "on_shutdown"):
            try:
                inst.on_shutdown()
                logger.info("Plugin on_shutdown aufgerufen: %s", name)
            except Exception:
                logger.exception("Fehler in on_shutdown von %s", name)

        meta["enabled"] = False
        mdata = yaml.safe_load(meta["manifest"].read_text()) or {}
        mdata["enabled"] = False
        meta["manifest"].write_text(yaml.safe_dump(mdata, sort_keys=False))
        logger.info("Plugin deaktiviert: %s", name)

    # Hook-Dispatcher – von GameApp aufgerufen:
    def on_init(self):     self._dispatch("on_init")
    def on_start(self):    self._dispatch("on_start")
    def on_event(self, e): self._dispatch("on_event", e)
    def on_update(self, dt):   self._dispatch("on_update", dt)
    def on_render(self, surf): self._dispatch("on_render", surf)
    def on_shutdown(self): self._dispatch("on_shutdown")

    def _dispatch(self, hook_name, *args, **kwargs):
        """Interne Hilfsmethode, um Hooks auf alle aktiven Plugins anzuwenden."""
        for plugin in list(self.plugins):
            fn = getattr(plugin, hook_name, None)
            if callable(fn):
                try:
                    fn(*args, **kwargs)
                except Exception:
                    logger.exception("Plugin-Fehler in %s.%s", plugin, hook_name)
