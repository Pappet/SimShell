# SimShell – MVP Compliance Checklist

This checklist defines the minimal requirements and rules that each module and feature must fulfill to be considered part of the MVP (Minimal Viable Product) of the NoMapNeeded framework.

---

## ✅ Core Rules

| Rule | Module | Validation |
|-----|-----|-----|
| Each UI Button must trigger an event, not contain game logic | `UI.Button` | Unit test: Button emits event on click |
| Game logic must not directly use or access UI modules | `StatsManager`, `TimeManager`, etc. | Code review check |
| No global variables outside of SimShell (except constants) | `Core` | Static analysis check |
| Every screen/view must be registered via the Tab system | `Tabs` | Unit test: Screen registration works |
| SimShell is responsible only for input dispatch & lifecycle | `Core.SimShell` | Code review, clear documentation |
| Each module must have at least one unit test | All modules | Test coverage check |
| Each module has a header comment and README | All modules | Manual check |

---

## 🚀 MVP Functional Requirements

These features must exist and comply with the rules above:

### Core
- SimShell core loop & input handling
- Event dispatch system

### UI Components
- Buttons (with click event)
- Labels (static text)
- Panels (as containers)
- Simple grid/row/column layout

### Game Logic
- Stats/Status system (e.g. fatigue, money, time)
- Time management system (actions consume time)

### Integration
- Button click can trigger an event that modifies game stats
- Basic Tab system to switch between views

---

## 🔥 MVP Completion Criteria

The MVP is considered complete when:

- All features listed above are implemented
- All core rules are followed and validated
- Every module has at least one test
- An example game exists that uses all MVP features
- A developer (myself) can explain each module and how it interacts with others

---

## 📄 Next Steps

Once MVP is complete, proceed to:

- Write a "Lessons Learned" file
- Plan the next phase (Extensions)
- Improve test coverage and documentation

