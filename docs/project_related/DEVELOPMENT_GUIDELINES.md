# SimShell – Development Guidelines

This document defines high-level development practices and principles for working on the NoMapNeeded framework. It complements the [Developer Commitment](./DEVELOPER_COMMITMENT.md), [Commit Guidelines](./COMMIT_GUIDELINES.md), [MVP Compliance Checklist](./MVP_COMPLIANCE_CHECKLIST.md) and [Tests Template](./TESTS_TEMPLATE.md).

---

## 🧱 Code Architecture Principles

- **Modularity First**: Each module should handle one responsibility only.
- **Loose Coupling**: Avoid direct dependencies between unrelated modules.
- **Separation of Concerns**: UI triggers events; game logic consumes them.
- **Encapsulate Logic**: Logic related to game state (e.g., stats) must never live in UI code.

---

## 📦 Project Structure (Standard Layout)

```
/core      → SimShell & application shell logic
/ui        → All functional modules (UI, stats, events, time, tabs)
/tests     → Unit and integration tests
/docs      → Design documents and meta-guides
/utility   → Small utility code
```

Each module should have:
- A clearly named `.py` source file
- At least one inline `test` block
- A header comment explaining the module’s purpose

---

## 🧪 Testing

See [Tests Template & Strategy](./TESTS_TEMPLATE.md) for details.

Summary:
- Each module must have at least one **unit test**
- Integration tests must validate cross-module behavior
- Tests should be readable and focused

---

## 📄 Documentation

- All core concepts and decisions should be documented in `/docs`
- Every new phase must include a **Lessons Learned** file
- Modules should be self-explanatory through inline comments and usage examples

---

## ✅ Commit Messages

Commit message rules have been moved to their own document:
➡️ See [Commit Guidelines](./COMMIT_GUIDELINES.md)

---

## 🧭 Development Flow

1. Plan feature or module using [Project Roadmap](./PROJECT_ROADMAP.md)
2. Ensure feature fits into [MVP Compliance Checklist](./MVP_COMPLIANCE_CHECKLIST.md) or a later phase
3. Implement with tests and documentation
4. Commit using proper tags ([Commit Guidelines](./COMMIT_GUIDELINES.md))
5. Reflect on process in Lessons Learned if feature is substantial

---

For all contributors: remember this is a learning-first project. Clear code, documented thought processes, and simplicity are more important than advanced tricks or full coverage. Build to understand — and enjoy it!