---
description: Review a project's context and generate prioritized next steps
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
---

# Project Next Steps

## Context

- Current timestamp: !`date "+%Y-%m-%d %H:%M"`
- Projects directory: c:\Users\jeffkit\OneDrive - CDW\Claude_Work\Projects

## Instructions

### Step 1 — List available projects

- Glob all `Projects/*/PROJECT.md` files
- Display a numbered list of project names (derived from folder names, humanized)
- Prompt: "Which project would you like to work on? Reply with a number."
- Wait for user selection

### Step 2 — Read project context

For the selected project, read two files in parallel:
- `Projects/[selected]/PROJECT.md` — structured status, scope, end date, next action
- `Projects/[selected]/CONTEXT.md` — accumulated context and history (may not exist yet)

Do NOT read any other files in the folder unless explicitly referenced in CONTEXT.md.

### Step 3 — Ask for new context

Display a brief summary of what you know about the project (2-4 sentences from PROJECT.md + CONTEXT.md).

Then ask:
"Is there any new context to add before I generate next steps? (e.g. meeting outcomes, blockers, decisions, status changes)

Reply with the new context, or 'none' to skip."

Wait for user response.

### Step 4 — Save new context (if provided)

If user provided new context (not 'none'):
- Append to `Projects/[selected]/CONTEXT.md` using this format:

```markdown
## [YYYY-MM-DD HH:MM]

[User's context verbatim, lightly cleaned up for clarity]
```

- If CONTEXT.md does not exist, create it with a header first:

```markdown
# Context Log — [Project Name]

Accumulated notes, decisions, and history for this project. Updated each session.

---

## [YYYY-MM-DD HH:MM]

[Context]
```

### Step 5 — Generate next steps

Based on everything in PROJECT.md and CONTEXT.md, produce a prioritized next steps list:

```markdown
## Next Steps — [Project Name] — [Date]

**Current Status:** [one line]
**End Date:** [from PROJECT.md]

### Immediate (do next)
1. [Most critical action, specific and actionable]
2. ...

### Short Term (this week)
1. ...

### Blocked / Waiting On
- [Any blockers or dependencies]

### Open Questions
- [Anything that needs a decision before proceeding]
```

### Step 6 — Offer to update PROJECT.md

Ask: "Would you like me to update the Next Action in PROJECT.md with today's immediate steps? (yes/no)"

If yes:
- Update the `## Next Action` section in PROJECT.md with the top 1-2 immediate steps
- Update `## Status` if the user's new context implies a status change
