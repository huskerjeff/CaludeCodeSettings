---
name: claude_session.json is per-machine, and capture via CDP attach
description: Session state for playwright-cli is machine-specific (Cloudflare clearance cookies bind to browser/IP); capture via edge://inspect remote-debugging + attach --cdp=msedge, never commit
type: feedback
originSessionId: 4076c39d-36ca-4cce-aabd-cfd5397c688a
---
`claude_session.json` (captured via `playwright-cli state-save`) is machine-specific and cannot be copied between laptops. It must be regenerated on each machine.

**Why:** The file embeds `cf_clearance` and related Cloudflare cookies that bind to browser fingerprint + IP. Cookies captured on machine A (e.g. the `huske` laptop) fail Cloudflare's challenge when injected into a browser on machine B (e.g. the `jeffkit` CDW laptop) — you get stuck on "Just a moment…" even though the Claude auth cookies are valid. The file is gitignored in `~/.claude/.gitignore` and should stay that way.

**How to capture on a new machine (the solution that worked 2026-04-22):**
Playwright-controlled browsers are blocked by Cloudflare/Google ("This browser may not be secure"), so you cannot log in *through* a playwright browser. Instead, attach to the user's already-logged-in real Edge:

1. Ask the user to log in to claude.ai in their normal Edge.
2. Ask the user to open `edge://inspect/#remote-debugging` and check **"Allow remote debugging for this browser instance"**. This toggle enables CDP on a running Edge without relaunching — the missing piece that prior CLAUDE.md notes called "still investigating".
3. `playwright-cli close-all` to release any isolated profile.
4. `playwright-cli attach --cdp=msedge` — should list their claude.ai tab as tab 0 with page title "Claude" (not "Just a moment…").
5. `playwright-cli state-save claude_session.json` from the CWD.
6. `cp claude_session.json ~/.claude/claude_session.json` for safekeeping.
7. `playwright-cli close-all` to detach (do NOT close their Edge — attach doesn't own the browser lifecycle, but `close-all` cleanly releases the CDP connection).

**How to apply in future flows:** If a playwright flow hits a Cloudflare "Just a moment…" page during `state-load`, stop and ask the user to refresh the session via the CDP-attach path above. Don't retry the failing state-load; the issue is the session file, not a transient network error.
