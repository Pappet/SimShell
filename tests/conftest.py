# tests/conftest.py
import os, sys
# Projekt‑Root (eine Ebene über tests/) zum Pfad hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))