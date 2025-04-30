# SimShell – Commit Guidelines

This document defines the rules and conventions for writing clear, consistent, and meaningful commit messages in the SimShell project.

---

## ✅ Commit Message Format

Each commit message must follow this format:

```
[Tag] Short description in present tense
```

**Examples:**

- `[Feat] Add basic Panel layout`
- `[Fix] Correct button click offset bug`
- `[Doc] Write test strategy and checklist`
- `[Test] Add unit test for stat manager`
- `[Refactor] Split UI and game logic in SimShell`
- `[Learn] Try out event dispatch using function pointers`
- `[Chore] Reorganize file structure for clarity`
- `[WIP] Implement initial version of stats system`

---

## 🔖 Allowed Tags

| Tag        | When to use                                                      |
|------------|-------------------------------------------------------------------|
| `[Feat]`   | Adding a new feature or module                                   |
| `[Fix]`    | Fixing a bug                                                     |
| `[Refactor]` | Changing code structure without altering behavior                 |
| `[Doc]`    | Adding or updating documentation                                 |
| `[Test]`   | Adding or updating tests                                         |
| `[Chore]`  | Other tasks like build scripts, restructuring                    |
| `[WIP]`    | Work in progress commits                                         |
| `[Learn]`  | Trying out ideas, experiments, or documenting new learnings      |

---

## 🧩 Best Practices

- **One commit = one logical change**
- Write commit messages in **present tense**
- Keep the description **short and clear**
- If the change is large, consider splitting into multiple commits
- For work in progress, use `[WIP]` and squash later if needed

---

## ℹ️ More Information

For general development rules and project structure, refer to the [Developer Commitment & Guidelines](docs/DEVELOPER_COMMITMENT.md).

---

By following these guidelines, the commit history will remain clear, searchable, and helpful for development and future maintenance.

