# CDP Session Refresh Process

A step-by-step procedure for refreshing `claude_session.json` (the cookie file used by `playwright-cli` to access claude.ai without being blocked by Cloudflare).

## Audience

This document is written for an AI model (Claude, another LLM) that has shell access and is running on the user's CDW laptop (`LT-AAD-F9FHV96C`, Windows 11). The AI executes the commands; the human user performs the manual login step.

## When to use this

Run this procedure when:
- `claude_session.json` cookies have expired (`playwright-cli goto https://claude.ai/new` redirects to `/login` or `/logout`)
- You are setting up `claude_session.json` for the first time
- The user explicitly asks to refresh the claude.ai session

## Why this process exists (background context)

Automating claude.ai with `playwright-cli` is normally blocked by two things:

1. **Cloudflare challenges** — Cloudflare detects Playwright's automation flags and blocks or challenges the browser.
2. **Manual login is also blocked** — logging in through a playwright-launched browser triggers the same detection.

The workaround is **Session Injection**: capture authentication cookies once from a real, trusted Edge session and inject them into the playwright-controlled browser before navigating. The cookies prove to Cloudflare that this is a known logged-in user.

The problem this document solves: *how to capture those cookies in the first place.* The user prefers logging in through their real Edge profile (which already has saved credentials, MFA trust devices, corporate SSO, etc.) rather than logging in again inside an isolated playwright profile. To bridge the real Edge session to playwright, we launch Edge with Chrome DevTools Protocol (CDP) enabled, then use `playwright-cli attach --cdp` to connect to it and export the cookies.

## Prerequisites

- `playwright-cli` installed and available on PATH (`playwright-cli --version` should work)
- Edge installed at its default location (`msedge.exe` resolvable via PATH)
- Port `9222` not in use by another process
- User is physically present and can log in to claude.ai manually

## The procedure

### Step 1 — Close existing playwright sessions

```bash
playwright-cli close-all
```

**Why:** Any leftover playwright-controlled browser holds locks on browser profiles and can conflict with subsequent commands. `close-all` releases every session the `playwright-cli` daemon is tracking. Safe to run even when nothing is open (no error, no output).

### Step 2 — Force-close any running Edge processes

Use PowerShell:

```powershell
Stop-Process -Name msedge -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2
```

**Why:** Edge is a single-instance application — launching `msedge.exe` while Edge is already running just opens a new window in the *existing* process, which ignores command-line flags like `--remote-debugging-port`. To make Edge actually honor the debug port flag, every current `msedge.exe` process must first exit. `-ErrorAction SilentlyContinue` makes the command a no-op if Edge is already closed. The 2-second sleep gives the OS time to fully release file locks on the user profile before we relaunch.

**Warning to user:** This closes the user's Edge windows and loses unsaved tabs. If the user has work in Edge, ask them to save it before running this step.

### Step 3 — Launch Edge with remote debugging enabled

Use PowerShell:

```powershell
Start-Process "msedge.exe" -ArgumentList "--remote-debugging-port=9222","https://claude.ai/new"
```

**Why:**
- `--remote-debugging-port=9222` tells Edge to start a CDP server on `localhost:9222`. This is the hook playwright will use to attach later. Without this flag, `playwright-cli attach --cdp` cannot connect.
- Passing `https://claude.ai/new` as a second argument makes Edge open that URL on launch, saving the user a navigation click.
- Edge uses the user's *real* profile by default (no `--user-data-dir` override), so all saved passwords, MFA trust, and corporate SSO state are available for login.

### Step 4 — Wait for the user to log in

Tell the user explicitly: "Edge is open with claude.ai. Log in if you're not already, then tell me when you're ready."

**Why:** You (the AI) cannot complete the login yourself — MFA, SSO redirects, and Cloudflare challenges require a real human. Don't poll the page or try to click login buttons. Just wait. The user will reply when logged in.

### Step 5 — Attach via CDP and save state in one command

When the user confirms they're logged in:

```bash
playwright-cli attach --cdp=http://localhost:9222 && playwright-cli state-save claude_session.json
```

**Why chain with `&&` in a single Bash call (this is the critical gotcha):**

`playwright-cli attach` does **not** support a `--persistent` flag. Unlike `playwright-cli open --persistent`, the attached session does not survive across separate Bash invocations. If you run:

```bash
playwright-cli attach --cdp=http://localhost:9222
# separate Bash call:
playwright-cli state-save claude_session.json
```

...the second command will fail with `Error: Browser 'default' is not open`. The attach session was already torn down.

Chaining both commands in **one** Bash call with `&&` keeps the attached session alive long enough for `state-save` to read the browser's cookies and write them to `claude_session.json` in the current working directory.

**What `state-save` does:** It calls Playwright's `context.storageState({ path })`, which serializes all cookies and localStorage for every origin the browser knows about. The resulting file is JSON, ~500KB–1MB, and contains the authentication tokens we need to bypass Cloudflare on future runs.

### Step 6 — Copy the session file to the safekeeping location

```bash
cp claude_session.json ~/.claude/claude_session.json
```

**Why:** The sandbox restricts file access to the current working directory, so `state-save` must write to the working directory. But the canonical long-term storage location is `~/.claude/claude_session.json` (per the user's `CLAUDE.md`). Future sessions will copy from there back to whatever working directory is active.

### Step 7 — Verify the save succeeded

```bash
ls -la ~/.claude/claude_session.json
```

**Why:** A successful save produces a file in the 500KB–1MB range. If the file is much smaller (say, under 10KB), something went wrong — likely the attach didn't actually connect, or the user hadn't completed login when state-save ran. The file size is the fastest sanity check.

## Verifying the refresh worked

Run a clean Session Injection flow to confirm the new cookies work:

```bash
playwright-cli close-all
```

```bash
playwright-cli open --browser=msedge --headed --persistent --profile="./.claude/claude_profile"
```

```bash
playwright-cli state-load claude_session.json
```

```bash
playwright-cli goto https://claude.ai/new
```

Then check the result — the page title should be "Claude" and the URL should stay on `claude.ai/new`. If the page redirects to `/login` or shows a Cloudflare challenge that doesn't resolve, the cookies did not transfer correctly and the refresh failed.

## Critical rules (don't violate these)

1. **Never chain `playwright-cli` commands with `&&` except the attach+state-save pair in Step 5.** Every other `playwright-cli` command should be a separate Bash call — chaining kills the browser session for subsequent commands. The Step 5 chain works specifically because `state-save` is the final action and doesn't need the session to persist afterward.
2. **Always use `--headed`.** Headless Edge is blocked by Cloudflare.
3. **Always use role locators** (`getByRole(...)`) in subsequent automation — DOM refs change every session.
4. **Never commit `claude_session.json` to git.** It contains authentication tokens equivalent to a password. It should live in `~/.claude/` only, never in a repo.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `attach --cdp` errors "connection refused" | Edge launched without `--remote-debugging-port`, or port 9222 is in use | Repeat steps 2–3. Check no other process owns port 9222 (`netstat -ano \| findstr :9222`) |
| `state-save` errors "Browser 'default' is not open" | Ran state-save in a separate Bash call from attach | Re-run step 5 with both commands chained by `&&` |
| Saved file is under 10KB | User hadn't finished login before Step 5 ran | Confirm login complete, redo Step 5 |
| After refresh, `goto claude.ai/new` still redirects to login | Cookies saved from wrong origin or for wrong account | Confirm in Edge that the logged-in account is correct before Step 5 |
| `Stop-Process` reports "cannot find process" | Edge already closed | Not an error — that's why we use `-ErrorAction SilentlyContinue` |
