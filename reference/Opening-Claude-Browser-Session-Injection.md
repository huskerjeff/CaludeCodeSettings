# Opening claude.ai with playwright-cli (Session Injection)

A step-by-step procedure for opening claude.ai in a playwright-controlled Edge browser **without triggering a Cloudflare challenge**. This is the "Session Injection" technique — it works by giving the automated browser pre-captured authentication cookies *before* it navigates to claude.ai, so Cloudflare sees a known logged-in user instead of a suspicious bot.

## Audience

This document is written for an AI model (Claude, another LLM) that has shell access and is running on the user's CDW laptop (`LT-AAD-F9FHV96C`, Windows 11). The AI executes the commands; no human interaction is required *unless* the cookies turn out to be stale (see "If this fails" at the bottom).

## When to use this

Every time you need to open claude.ai programmatically — to fill a prompt, take a screenshot, scrape a response, etc. This is the default entry-point for any claude.ai automation.

## Why this works (background context)

Three problems block naive `playwright-cli open https://claude.ai`:

1. **Cloudflare detects Playwright** — it sees automation flags and serves a "Just a moment..." challenge page that won't clear.
2. **Edge profile locks** — using your real Edge profile fails because Edge is probably already running and holds the profile lock.
3. **Corporate security** — on the CDW laptop, Chrome's User Data is locked by endpoint protection, so `--browser=chrome` doesn't work at all.

Session Injection solves all three:

- **Fresh isolated profile** (`./.claude/claude_profile`) avoids the profile lock conflict. It's a dedicated playwright profile that has nothing to do with your normal Edge.
- **Cookie injection** (`state-load claude_session.json`) loads pre-captured authentication cookies — including Cloudflare's `cf_clearance` cookie — into the isolated profile *before* any navigation happens. When the browser later visits claude.ai, Cloudflare inspects the cookies, sees valid clearance, and lets the page load normally.
- **`--browser=msedge`** sidesteps the Chrome corporate lock entirely.

The magic is the **order**: inject cookies first, then navigate. If you navigate first (or pass the URL to the `open` command), the browser hits Cloudflare cookieless and gets blocked — even though `state-load` would have had valid cookies.

## Prerequisites

- `playwright-cli` installed and on PATH (`playwright-cli --version` must work)
- Edge installed (`msedge` available)
- A valid `claude_session.json` at `~/.claude/claude_session.json`
  - If this file is missing or its cookies are stale, run the CDP refresh procedure at `~/.claude/reference/CDP-Session-Refresh-Process.md` first

## The procedure

Each step below is a **separate Bash call**. Do not chain these with `&&` — chaining kills the browser session for subsequent commands.

### Step 1 — Close any existing playwright sessions

```bash
playwright-cli close-all
```

**Why:** The playwright-cli daemon tracks one or more "sessions" (browser instances it controls). Any leftover session from a prior run holds a lock on the isolated profile directory (`./.claude/claude_profile`), which would cause Step 2 to fail with a profile-in-use error. `close-all` releases every session cleanly. Safe to run even when nothing is open — it just does nothing and returns no output.

### Step 2 — Copy the session file into the working directory

```bash
cp ~/.claude/claude_session.json ./claude_session.json
```

**Why:** The canonical storage location for the session file is `~/.claude/claude_session.json` (safe, machine-specific, gitignored). But `playwright-cli state-load` runs inside a sandbox that only has read access to the *current working directory and below*. It cannot read from `~/.claude/`. So we copy the file down to the working directory before using it.

If the file already exists in the working directory from a prior run, this overwrites it with the canonical copy — which is what we want, because the safekeeping version is always the most recent.

### Step 3 — Open Edge with an isolated persistent profile (no URL yet)

```bash
playwright-cli open --browser=msedge --headed --persistent --profile="./.claude/claude_profile"
```

Breaking down each flag:

- **`--browser=msedge`** — use Edge, not Chrome. Chrome fails on the CDW laptop because corporate security software locks Chrome's user data directory. Edge is unaffected.
- **`--headed`** — show the browser window. Headless mode is aggressively blocked by Cloudflare — the `Just a moment...` page never clears. Headed mode with real rendering is the only reliable option.
- **`--persistent`** — keep the playwright control connection alive after the `open` command returns. Without this, the browser would launch but you couldn't send follow-up commands (`snapshot`, `click`, `goto`, etc.) to it — the control connection would drop immediately. We need the connection alive because Steps 4 and 5 talk to the same browser.
- **`--profile="./.claude/claude_profile"`** — point Edge at a private profile directory we own. This is **not** the user's real Edge profile — it's a playwright-managed throwaway that lives under the working directory. Using an isolated profile means:
  - No lock conflict with the user's real Edge (they can keep using Edge normally in parallel).
  - No 25 previous tabs reopening (the real profile would restore whatever the user had open).
  - Full control over what cookies/state live in this profile.
- **Note the absence of a URL** — the browser opens to `about:blank`. We intentionally do NOT navigate to claude.ai yet. If we did, the browser would hit Cloudflare cookieless and get challenged, and Step 4 would be too late to help.

After this step, an Edge window is visible on the user's screen showing a blank page.

### Step 4 — Load the authentication cookies into the browser

```bash
playwright-cli state-load claude_session.json
```

**Why:** This reads `claude_session.json` (the file we just copied into the working directory) and applies every cookie and localStorage entry to the browser's context. The critical cookies are:

- **`sessionKey`** (claude.ai's own auth token) — proves the user is logged in.
- **`cf_clearance`** (Cloudflare's clearance token) — proves this browser previously passed Cloudflare's challenge. Cloudflare honors this for a window of time tied to the browser fingerprint and IP.
- Various anti-bot telemetry cookies that Cloudflare also inspects.

Because the browser is still sitting on `about:blank`, no network request has been made yet — so the cookies get set cleanly before anything happens.

### Step 5 — Navigate to claude.ai

```bash
playwright-cli goto https://claude.ai/new
```

**Why:** Now the browser navigates. Cloudflare inspects the incoming request, sees `cf_clearance` and the claude.ai session cookies, decides this is a trusted returning user, and serves the real page. No challenge, no redirect, no `Just a moment...`. The page title becomes "Claude" and you land on `/new`.

From here you can interact with the page normally — fill the textarea, click buttons, take screenshots — using standard `playwright-cli` commands like `fill`, `click`, `press`, `snapshot`.

## Using the session (common follow-ups)

### Submit a prompt

```bash
playwright-cli fill "getByRole('textbox', { name: 'Write your prompt to Claude' })" "your prompt text here"
```

```bash
playwright-cli press Enter
```

### Take a snapshot of the page

```bash
playwright-cli snapshot
```

### Switch to a different model

```bash
playwright-cli click "getByRole('button', { name: 'Sonnet 4.6' })"
```

```bash
playwright-cli click "getByRole('menuitemradio', { name: 'Opus 4.7 Most capable for ambitious work' })"
```

(Model names and roles change over time — run `snapshot` first to see what's actually in the menu if a locator fails.)

## Critical rules (don't violate these)

1. **Never chain `playwright-cli` commands with `&&`.** Each command must be a separate Bash call. The only exception is the `attach --cdp && state-save` pair in the CDP refresh procedure — and that's only because `attach` can't be made persistent any other way.
2. **Always use `--headed`.** Headless is blocked by Cloudflare.
3. **Always use role locators** (`getByRole(...)`). Element refs change every session — they will work once and then fail silently.
4. **Open with no URL, then `state-load`, then `goto`.** Never pass a URL to the `open` command when using Session Injection — you'll navigate before the cookies are loaded and get blocked.
5. **Never commit `claude_session.json` to git.** It contains authentication tokens equivalent to a password. It is gitignored in `~/.claude/.gitignore` and must stay that way.

## If this fails

If Step 5 redirects to `/login`, `/logout`, or shows a Cloudflare challenge that doesn't clear, the cookies in `claude_session.json` are stale. Don't retry — cookies don't un-expire.

Run the CDP refresh procedure documented at `~/.claude/reference/CDP-Session-Refresh-Process.md` to capture fresh cookies. That procedure requires the user to log in manually in a real Edge window (with `--remote-debugging-port=9222`), after which playwright attaches via CDP and calls `state-save` to write a new `claude_session.json`. Once refreshed, return to Step 1 above.

## Quick reference (the whole thing, bottom-to-top)

```bash
# 1. Close any existing sessions
playwright-cli close-all

# 2. Copy session file to working directory
cp ~/.claude/claude_session.json ./claude_session.json

# 3. Open Edge with isolated profile, NO URL
playwright-cli open --browser=msedge --headed --persistent --profile="./.claude/claude_profile"

# 4. Inject cookies
playwright-cli state-load claude_session.json

# 5. Navigate — now safe from Cloudflare
playwright-cli goto https://claude.ai/new
```
