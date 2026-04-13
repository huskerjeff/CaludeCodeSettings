---
description: Create a new project folder with PROJECT.md and CONTEXT.md in the Claude_Work Projects directory
---

<objective>
Create a new project entry in the work planning system by gathering key details from the user, then generating the project folder, PROJECT.md, and CONTEXT.md files.

Working directory: c:\Users\jeffkit\OneDrive - CDW\Claude_Work
Projects folder: Projects/
</objective>

<process>
1. Ask the user the following questions one at a time and wait for their responses:
   - "What is the project name?" (will be used to create the folder name in kebab-case)
   - "Brief overview — what is this project and what does it accomplish?"
   - "End date? (Enter a date or type TBD)"
   - "List the scope items — what are the main things this project involves? (one per line, or comma-separated)"

2. Convert the project name to kebab-case for the folder name (e.g., "Red Bull Switch Fix" → "RedBull-Switch-Fix")

3. Create the folder: `Projects/[kebab-case-name]/`

4. Create `Projects/[kebab-case-name]/PROJECT.md` using this exact format:

```
# [Project Name]

## Overview
[Overview from user]

## Status
🔴 Not Started

## End Date
[End date or TBD]

## Scope
[Each scope item as a bullet point]

## Next Action
- [Ask user: "What's the first next action for this project?"]

## Notes
- Added [today's date YYYY-MM-DD]
```

5. Create `Projects/[kebab-case-name]/CONTEXT.md` with this content:

```
# [Project Name] — Context Log

Use this file to log notes, decisions, blockers, and updates as the project progresses.
Add entries with a timestamp prefix: YYYY-MM-DD — [note]

---
```

6. Confirm to the user: "Project '[Project Name]' created at Projects/[folder-name]/. Files created: PROJECT.md, CONTEXT.md."
</process>

<output>
Files created:
- `Projects/[project-name]/PROJECT.md` — Structured project status file
- `Projects/[project-name]/CONTEXT.md` — Running log for notes and decisions
</output>

<success_criteria>
- User was asked for all required fields (name, overview, end date, scope, next action)
- Folder created with kebab-case name under Projects/
- PROJECT.md created with all fields populated and status set to 🔴 Not Started
- CONTEXT.md created with header and logging instructions
- Confirmation message displayed to user
</success_criteria>
