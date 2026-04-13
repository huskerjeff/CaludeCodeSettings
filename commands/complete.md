---
description: Mark a task or project as complete and move it to the Completed folder
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
---

# Complete

## Context

- Current timestamp: !`date "+%Y-%m-%d %H:%M"`
- Working directory: c:\Users\jeffkit\OneDrive - CDW\Claude_Work

## Instructions

### Step 1 — Ask what to complete

Ask: "What would you like to mark as complete?\n\n1. A task (from TO-DOS.md)\n2. A project\n\nReply with 1 or 2."

Wait for user response.

---

### If Task (option 1):

**Step 1a — List tasks**
- Read `Tasks/TO-DOS.md`
- Display a numbered list of all tasks (bold title + date)
- Prompt: "Which task is complete? Reply with a number."
- Wait for user selection

**Step 1b — Archive the task**
- Read `Completed/Tasks/completed_todos.md` (create if it doesn't exist)
- Append the completed task entry to the bottom of `Completed/Tasks/completed_todos.md`:

```markdown
## [Original heading title] — Completed [YYYY-MM-DD]

- ~~[Original todo line]~~
```

- Remove the completed task's entire section (h2 heading + todo line) from `Tasks/TO-DOS.md`

**Step 1c — Confirm**
- Say: "Task marked complete and archived."

---

### If Project (option 2):

**Step 2a — List projects**
- Glob all `Projects/*/PROJECT.md`
- Display a numbered list of project names
- Prompt: "Which project is complete? Reply with a number."
- Wait for user selection

**Step 2b — Update PROJECT.md**
- Read the selected project's `PROJECT.md`
- Update `## Status` to `✅ Done`
- Add `## Completed` field with today's date below Status

**Step 2c — Move the project folder**
- Move the entire project folder from `Projects/[name]/` to `Completed/Projects/[name]/`
- Use: `mv "Projects/[name]" "Completed/Projects/[name]"`

**Step 2d — Clean up linked tasks**
- Read `Tasks/TO-DOS.md`
- Check for any tasks with `**Project:** [project-name]`
- If found, list them and ask: "These tasks are linked to this project. Mark them complete too? (yes/no)"
- If yes, archive each one using the task archive steps above

**Step 2e — Confirm**
- Say: "Project '[name]' marked complete and moved to Completed/Projects/."

---

## Completed Folder Structure

```
Completed/
├── Tasks/
│   └── completed_todos.md    # All archived tasks, newest at bottom
└── Projects/
    └── [project-folder]/     # Full project folder moved here
        ├── PROJECT.md        # Status updated to ✅ Done
        └── CONTEXT.md        # Preserved for reference
```
