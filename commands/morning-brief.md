---
description: Generate a prioritized daily work plan from tasks and projects
allowed-tools:
  - Read
  - Write
  - Glob
---

<objective>
Generate a daily morning brief for a Senior System Engineer at CDW.
Pulls from active tasks and projects to produce a prioritized, focused plan for the day.
Saves the brief to a dated file and displays it in chat.

Working directory: c:\Users\jeffkit\OneDrive - CDW\Claude_Work
</objective>

<context>
- Today's date is available in your system context (currentDate). Use it for both the filename (YYYY-MM-DD) and the header (Full Day Name, Month Day, Year).
</context>

<process>
1. Read source files in parallel:
   - Read `Tasks/TO-DOS.md`
   - Glob all `Projects/*/PROJECT.md` and read each one

2. Parse tasks from TO-DOS.md:
   - Extract all items starting with `- **` (active todos)
   - For each: capture title, priority (High/Medium/Low), problem summary, and Project link if present
   - Group by priority: High → Medium → Low
   - Within High priority, sort oldest first (by h2 heading date)

3. Parse projects:
   - Extract name, status, end date, and Next Action from each PROJECT.md
   - Only include projects with status 🟡 In Progress or 🔴 Not Started

4. Write brief to `Morning Brief/YYYY-MM-DD.md` (use today's date):
   - If file already exists, overwrite it with the refreshed brief
   - Use the output format below exactly

5. Display the full brief content in chat and confirm: "Morning brief created for [Day, Date]."
</process>

<output>
File: `Morning Brief/YYYY-MM-DD.md`

```markdown
# [Full Day Name], [Month Day, Year]

> **Focus:** [Single highest-leverage action today — based on oldest High priority tasks and active In Progress projects]

---

## High Priority Tasks

- [ ] **[Task Title]** — [one-line summary] *(Project: [name] if linked)*
- [ ] ...

## Medium Priority Tasks

- [ ] **[Task Title]** — [one-line summary]
- [ ] ...

## Low Priority Tasks

- [ ] **[Task Title]** — [one-line summary]
- [ ] ...

---

## Active Projects — Next Steps

| Project | Status | Next Action | End Date |
|---------|--------|-------------|----------|
| [Name] | 🟡 In Progress | [Next action] | [Date or TBD] |
| [Name] | 🔴 Not Started | [Next action] | [Date or TBD] |

---

## Notes
_Add notes here as the day progresses._
```
</output>

<success_criteria>
- Tasks grouped correctly by priority (High → Medium → Low)
- High priority tasks sorted oldest first
- Project links noted inline for linked tasks
- Only In Progress or Not Started projects shown in the table
- Brief written to correct dated file in Morning Brief/
- Full content displayed in chat
</success_criteria>
