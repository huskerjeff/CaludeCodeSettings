---
name: Use snapshot refs for iframe-nested elements in playwright-cli
description: Locator strings fail on iframe content; passing the ref ID auto-resolves iframe traversal for fill/eval/click
type: feedback
originSessionId: 61e5120a-47d5-4e14-b08d-079b45eecdeb
---
When a `playwright-cli` command targets an element inside an iframe (e.g., ServiceNow's `gsft_main`), prefer the snapshot ref ID (e.g., `f1e318`) over a locator string like `getByRole('textbox', { name: '...' })`.

**Why:** On 2026-05-04, `playwright-cli fill "getByRole('textbox', { name: 'Additional comments (Client visible)' })" "casd"` failed with "does not match any elements" because the textbox lives inside the `gsft_main` iframe and the CLI does not traverse iframes when a locator string is passed at the top level. Switching to `playwright-cli fill f1e318 "casd"` worked — the generated playwright code shows the CLI auto-emitting `page.locator('iframe[name="gsft_main"]').contentFrame().getByRole(...)` when it resolves the ref.

The same applies to `eval`: `playwright-cli eval "el => ..." f1e42` succeeded; passing a locator string as the second arg failed with `el` undefined.

**How to apply:** Take a `playwright-cli snapshot` first, grep the output `.yml` for the target's role/name, copy the `[ref=fXeNN]` ID, and pass that ID as the element argument. Refs are stable across non-DOM-rebuilding actions (scrolls, fills) but invalidate on navigation — re-snapshot after `goto` or after dynamic DOM swaps. Click/hover/right-click also accept refs (`playwright-cli click f1e318 right` is documented in `SERVICENOW_EXPORT_FLOW.md`).
