# SimShell – Developer Commitment & Guidelines

## 🎯 Purpose
This document serves as a personal agreement and guideline for the development of the SimShell framework. It ensures that I work in a structured, modular, and understandable way — with the goal of completing the project and learning from it.

---

## 🟢 Personal Commitment

1. **Understanding over Copying**
   - I commit to not blindly copying functions or modules.
   - Before adopting code from external sources or ChatGPT, I will write **in my own words** in the commit message or documentation what the code does and why I am using it.

2. **Document Every Function and Module**
   - Each file must include a **header comment** explaining what the module does and what its role is in the overall framework.

3. **No Shortcuts for Core Modules**
   - I will implement every core module (Event System, UI Widgets, Stats System, etc.) **myself**.

4. **Regular Reflection**
   - After each phase, I will write a **Lessons Learned file** (e.g., `docs/lessons_phase1.md`).

---

## 📄 Development Guidelines (Summary)

| Rule | Reason |
|-----|-----|
| No logic inside UI elements | UI triggers events; game logic happens in Game Modules |
| Tests for every new module | Maintainability & safety |
| Documentation for every module | Readability & learning progress |
| "Small steps, clean commit history" | Traceability |

---

## 🔥 Learning Validation Checklist

Before marking a feature or milestone as "done," I will check:

- ✅ Can I explain to someone else what the module does?
- ✅ Have I written at least one test for the module?
- ✅ Have I added a short comment or README for the module?
- ✅ Would I still understand this code a year from now?

Optional:
- 📌 Review with ChatGPT or a friend: "Can you understand what I built here?"

---

## 🚀 Project Phase Commitment

| Phase | Learning Goal |
|----|----|
| Phase 1: MVP | Understand modules, event dispatch, and UI element handling |
| Phase 2: Extensions | Advanced architecture (tabs, save/load), encapsulate events properly |
| Phase 3: Comfort Features | Focus handling, layout system, integration tests |
| Phase 4: Plugins/Scripting | Design and implement dynamic extensibility |

---

## ⭐️ Completion Criteria

This project is considered **complete and successful** when:

- ✅ All planned MVP and extension features are implemented
- ✅ A complete project documentation exists
- ✅ I can use the framework independently in an example game
- ✅ I can explain to anyone how the framework works and why I built it this way

