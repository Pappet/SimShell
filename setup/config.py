# setup/config.py

import os
import json

# Versuche, YAML zu benutzen – falls installiert
try:
    import yaml
    _use_yaml = True
except ImportError:
    _use_yaml = False

# Entscheide, ob wir eine YAML- oder JSON-Datei laden
_cfg_file = os.path.join(
    os.path.dirname(__file__),
    'config.yaml' if _use_yaml else 'config.json'
)

# Lade die Konfiguration
with open(_cfg_file, 'r', encoding='utf-8') as f:
    if _use_yaml and _cfg_file.endswith(('.yml', '.yaml')):
        _data = yaml.safe_load(f)
        if _data is None:
            _data = {}
    else:
        _data = json.load(f) or {}

# Extrahiere die einzelnen Bereiche (mit leeren Dicts als Fallback)
screen      = _data.get('screen', {})
paths       = _data.get('paths', {})
logging     = _data.get('logging', {})
fonts       = _data.get('fonts', {})
ui          = _data.get('ui', {})
theme       = _data.get('theme', {})
scenes      = _data.get('scenes', {})
# neu: Plugins als Liste von Metadaten
plugins = _data.get('plugins', [])

def save():
    """Schreibt den aktuellen _data-Stand zurück in die YAML/JSON."""
    with open(_cfg_file, 'w', encoding='utf-8') as f:
        if _use_yaml:
            yaml.safe_dump(_data, f, sort_keys=False)
        else:
            json.dump(_data, f, indent=2)