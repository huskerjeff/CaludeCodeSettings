# Claude Work - Memory

## Purpose
This working directory (`c:\Users\jeffkit\OneDrive - CDW\Claude_Work`) is used to create a morning plan for the rest of the day.

## User Preferences
- Communication style: brief, direct

## Repository Structure

```
Claude_Work/
├── Tasks/
│   └── TO-DOS.md               # Active single-action tasks
├── Completed/
│   ├── Tasks/
│   │   └── completed_todos.md  # Archived completed tasks
│   └── Projects/               # Completed project folders moved here
├── Projects/                   # Multi-step initiatives (each has own sub-folder + PROJECT.md)
│   ├── BaaS-Cluster-Networking/
│   ├── BaaS-Certificates-Renewal/
│   ├── RedBull-VxRail-Switch-Replacement/
│   ├── Deere-McLaren-Server-Health-Dashboard/
│   └── Scott-DC-Windows-Migration/
├── Job description/
│   └── JOB-DESCRIPTION.md      # Role: Senior System Engineer (Nutanix, VMware, Cisco UCS, Windows/AD)
└── Morning Brief/              # Daily plan files, named YYYY-MM-DD.md
```

## Key Conventions

### TO-DOS.md Format
Each entry uses:
`- **[Action verb] [Component]** - [Description]. **Priority:** High/Medium/Low. **Problem:** [Why needed]. **Files:** [Paths]. **Project:** [ProjectFolder] (optional)`

### PROJECT.md Format
Fields: Overview, Status (🔴 Not Started / 🟡 In Progress / ✅ Done), End Date, Scope, Next Action, Notes

### Task vs Project Rule
- **Task** = single actionable item (email, call, review, write one doc)
- **Project** = multi-step initiative with a defined end date → goes in Projects folder

### Priority Logic
- **High** = customer-facing, blocking another task/project, or significantly overdue
- **Medium** = named stakeholder waiting, or data accuracy work
- **Low** = documentation, recurring/informational, no deadline

## Daily Workflow
- `/morning-brief` command (at `~/.claude/commands/morning-brief.md`) generates a dated brief in `Morning Brief/` each day
- Brief pulls High tasks (sorted oldest first), then Medium, then Low, plus active project next steps
- `/add-to-todos` adds tasks to TO-DOS.md (asks for priority before saving)
- `/project-next-steps` reviews a project, asks for new context, saves it to `CONTEXT.md`, then generates Immediate / Short Term / Blocked next steps
- `/complete` marks a task or project done — archives tasks to Completed/Tasks/, moves project folders to Completed/Projects/

## Project Context Convention
Each project folder contains:
- `PROJECT.md` — structured status (scope, end date, next action, status)
- `CONTEXT.md` — timestamped running log of notes, decisions, blockers (Claude reads only this, not other files)
- Other files (scripts, docs, diagrams) — referenced in CONTEXT.md as needed

## Feedback & Preferences
- [feedback_sl1_templates.md](feedback_sl1_templates.md) — Using templates with SL1 is very helpful
- [feedback_gemini_playwright.md](feedback_gemini_playwright.md) — "Open Gemini" means use playwright-cli with Edge to open gemini.google.com
- [feedback_no_notebooklm.md](feedback_no_notebooklm.md) — Do not use notebooklm or notebooklm-research skills
- [feedback_session_injection.md](feedback_session_injection.md) — Session Injection: isolated profile + cookie injection bypasses profile locks and Cloudflare
- [feedback_session_refresh_cdp.md](feedback_session_refresh_cdp.md) — Refresh claude_session.json via Edge --remote-debugging-port + attach --cdp + state-save (chain with &&)

## External References
- [reference_snow_test_instance.md](reference_snow_test_instance.md) — ServiceNow test instance URL (siriuscomtest)

## User Role
Senior System Engineer at CDW — Nutanix, VMware vSphere, Cisco UCS, Windows Server, Active Directory
KPIs: Uptime, Project delivery, Team enablement, Incident resolution, Documentation quality
