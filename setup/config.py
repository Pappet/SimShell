"""
Module setup/config.py

Loads and provides application configuration from JSON or YAML files.
Supports automatic fallback if PyYAML is unavailable, exposing
configuration sections as module-level variables and offering a save()
function to persist changes.
"""

import os
import json

# Attempt to use YAML if available for richer config support
try:
    import yaml
    _use_yaml = True
except ImportError:
    _use_yaml = False

# Determine the configuration file path (YAML preferred if available)
_cfg_file = os.path.join(
    os.path.dirname(__file__),
    'config.yaml' if _use_yaml else 'config.json'
)

# Load the configuration data from file
with open(_cfg_file, 'r', encoding='utf-8') as f:
    if _use_yaml and _cfg_file.endswith(('.yml', '.yaml')):
        _data = yaml.safe_load(f) or {}
    else:
        _data = json.load(f) or {}

# Expose individual config sections with defaults
screen = _data.get('screen', {})
paths = _data.get('paths', {})
logging = _data.get('logging', {})
fonts = _data.get('fonts', {})
ui = _data.get('ui', {})
theme = _data.get('theme', {})
scenes = _data.get('scenes', {})
plugins = _data.get('plugins', [])
sounds = _data.get('sounds', {})


def save() -> None:
    """
    Persist the current configuration data back to the config file.

    Writes _data into the original file format (YAML or JSON), preserving
    ordering for readability.
    """
    with open(_cfg_file, 'w', encoding='utf-8') as f:
        if _use_yaml:
            # Dump YAML without sorting keys to preserve structure order
            yaml.safe_dump(_data, f, sort_keys=False)
        else:
            # Pretty-print JSON with indentation
            json.dump(_data, f, indent=2)
