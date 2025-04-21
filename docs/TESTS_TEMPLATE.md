# NoMapNeeded – Test Template & Strategy

This document defines the structure, conventions, and goals for writing tests in the NoMapNeeded framework. All modules must include basic unit tests and, where appropriate, integration tests.

---

## ✅ General Testing Principles

- Every module must have at least one **unit test**
- Integration tests must be added for cross-module behavior (e.g., UI triggers event, which modifies game state)
- Tests must be readable and self-contained
- Each test must include a short comment describing its intent

---

## 📦 Test Directory Structure

```
/tests
│
├── unit
│   ├── button_test.py
│   ├── panel_test.py
│   ├── stats_test.py
│   └── ...
│
├── integration
│   ├── ui_to_event_test.py
│   ├── stats_persistence_test.py
│   └── ...
```

Each module should also contain inline `test` blocks for direct testing of exposed functions.

---

## 🧪 Unit Test Template

```python
[TODO]
```

---

## 🔗 Integration Test Template

```python
[TODO]
```

---

## 📝 Test Documentation

Each test file should include a short header comment:

```python
// _test_stats.py
// Unit tests for the Stats module. Ensures stat creation, retrieval, and modification behave as expected.
```

---

## 📈 Test Tracking Goals

- ✅ Each module tested in isolation
- ✅ Cross-module behavior verified via integration tests
- ✅ CI-compatible (tests can be run via `pytest` or custom runner)
- ✅ Easy to extend when new features are added

---

## 📄 Next Steps

- Add unit tests for all MVP modules
- Begin adding integration tests once event system is connected
- Document uncovered modules and plan for future coverage

