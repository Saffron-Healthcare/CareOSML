# Claude Session Guidelines

## Project Context

**Project:** CareOsML

**Primary Goal:** Identify women who are missng a diagnosis of perimenopause or menopause using machine learning.

**GitHub:** https://github.com/Saffron-Healthcare/CareOSML

**Key Files:**
- `docs/README.md` - general overview of the project
- `docs/progress.md` - Detailed progress and session notes (updated each session)
- `docs/tasks.md` - Task backlog and remaining work
- This file (`claude.md`) - Static session guidelines and preferences

**Scope:** Limit searches and work to the project directory

---

## Team Communication

| Person | Technical Level | Preferred Style |
|--------|-----------------|-----------------|
| Julio | Expert Python | Full technical detail welcome |
| Krish | Expert Python | Technical + natural language explanations |
| Krishna | Moderate | Business impact, medical accuracy focus |
| Christina | Non-technical | Natural language, clinical rationale only |
| Sylvia | Non-technical | Natural language, operations focus |

---

## Session Routines

### Startup (Every New Session)
1. Read `docs/status.md` to understand current state
2. Read `docs/progress.md` for recent session context
3. Read `docs/standards/*.md` to ensure standards compliance
4. Propose the next task

### End (Every Commit)
1. Update `docs/status.md` with current state
2. Update `docs/progress.md` with session notes (if significant work done)


---

## Communication Style

### Explanations
- **Default:** Detailed explanations with examples
- **When requested "be brief":** Concise, get to the point
- **TypeScript concepts:** Always relate to Python equivalents
- **Code examples:** Show both TypeScript and Python side-by-side when helpful

### Tone
- Professional but friendly
- No excessive praise or validation
- Focus on technical accuracy
- Admit uncertainty when appropriate
- No emojis unless explicitly requested

---

## Tool Usage Preferences

### Reading Files
- **Multiple related files:** Read in parallel
- **Large files:** Read in sections if needed
- **Always read before editing:** Non-negotiable

### Code Changes
- **Test after changes:** Suggest test commands

### Testing
- **Always use `uv`:** Run all tests using `uv run pytest`
- **Example:** `uv run pytest test/test_risk_engine.py -v`
- **Strategy:** Critical integration tests only (not exhaustive unit tests)

### Commands
- **Prefer parallel:** When operations are independent
- **Explain first:** For destructive operations
- **Ask permission:** For installing software or system changes

---

## Do's and Don'ts

### Code - DO
- ✅ Add type hints everywhere
- ✅ Write clear, self-documenting code
- ✅ Keep functions small and testable
- ✅ Use black formatting

### Code - DON'T
- ❌ Over-engineer or add "nice-to-haves"
- ❌ Add features not in the original
- ❌ Create abstractions prematurely
- ❌ Modify medical logic without explicit discussion
- ❌ Skip validation in data models

### Process - DO
- ✅ One step at a time, confirm before moving on
- ✅ Update status.md and progress.md regularly
- ✅ Test incrementally
- ✅ Ask questions when logic is ambiguous

### Process - DON'T
- ❌ do not commit directly to main
- ❌ Jump ahead in translation order
- ❌ Batch too many changes at once
- ❌ Assume - ask when requirements are unclear

### Communication - DO
- ✅ Show code examples
- ✅ Admit when something is uncertain
- ✅ Suggest best practices when appropriate

### Communication - DON'T
- ❌ Use excessive superlatives ("amazing", "perfect", etc.)
- ❌ Add emojis by default
- ❌ Be overly verbose when brevity was requested

---

## Updating Documentation
**This file (`claude.md`):** Should remain static. Update only when:
- Team composition changes
- New preferences are discovered
- Process improvements are identified

**Dynamic files to update each session:**
- `docs/status.md` - Current state snapshot
- `docs/progress.md` - Detailed progress and notes
- `docs/tasks.md` - Task backlog
