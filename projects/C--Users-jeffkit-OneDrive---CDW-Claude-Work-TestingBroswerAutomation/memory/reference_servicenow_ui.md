---
name: ServiceNow (siriuscom) UI selectors and behaviors
description: Verified accessibility-tree selectors for the global search box, ticket form fields, and shortcut behaviors on siriuscom.service-now.com
type: reference
originSessionId: 61e5120a-47d5-4e14-b08d-079b45eecdeb
---
Tenant: `siriuscom.service-now.com`. Verified 2026-05-04 against the Polaris/Next Experience UI.

**Global search (top bar):**
- Role: `combobox` (not `textbox`).
- Accessible name: `Search` (use `exact: true` — there is also a `Choose search context` combobox adjacent).
- Behavior: typing a ticket number (e.g., `TKT0901778`) and pressing `Enter` navigates directly to `ticket.do?sys_id=...` — no need to click a result. The page hint text confirms: "No exact match. Press Enter for full results."
- Selector that worked: `getByRole('combobox', { name: 'Search', exact: true })` for `fill`; then `playwright-cli press Enter`.

**Ticket form (`ticket.do`):**
- All form fields render inside iframe `name="gsft_main"`. Locator strings at the top-level page do not see them — use snapshot refs (see `feedback_playwright_cli_iframe_refs.md`).
- Common textbox accessible names observed: `Number`, `Opened by` (prefixed with "Read only - cannot be modified"), `Opened`, `Closed`, `Proposed due date`, `Due date`, `Procedure`, `Short description`, `Description`, `Additional comments (Client visible)`.
- Filling `Additional comments` does not save until the form's Save/Update button is clicked.

**Stable HTML identifiers (preferred over ephemeral refs):**
ServiceNow form fields follow a `<table>.<field>` naming convention exposed as both `id` and `name` attributes — these survive reloads/sessions, unlike playwright-cli refs which change every snapshot.

Example (Description field on ticket form, verified 2026-05-04):
- Tag: `TEXTAREA`
- `id` = `name` = `ticket.description`
- `class` = `form-control`
- `aria-labelledby` = `label.ticket.description`

Targeting from inside the iframe: `[name="ticket.description"]` or CSS `#ticket\\.description` (escape the dot). The same `<table>.<field>` pattern applies to all fields on the form (e.g., `ticket.short_description`, `ticket.opened_by`). To discover the actual `id`/`name` for any field, run:
```
playwright-cli eval "el => ({id: el.id, name: el.name, tag: el.tagName})" <ref>
```

**Keyboard scroll:**
- `Control+End` on the parent page scrolls the active ticket form to its bottom — the iframe does *not* eat the keystroke. Confirmed visually 2026-05-04.

**Phase 1 / Phase 2 flows:** documented in `SERVICENOW_PLAYWRIGHT_FLOW.md` and `SERVICENOW_EXPORT_FLOW.md` in the project root.
