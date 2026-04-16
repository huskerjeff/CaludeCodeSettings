# Claude Instructions

## Automating claude.ai with playwright-cli

Use `playwright-cli` (`@playwright/cli`) — NOT `playwright` (`@playwright/test`). The testing framework runs headless and gets blocked by Cloudflare.

### Install

```bash
npm install -g @playwright/cli@latest
```

Verify: `playwright-cli --version`. If the global command isn't available, use `npx playwright-cli` instead.

### Open claude.ai (run once to log in — session persists after that)

```bash
playwright-cli open --browser=chrome --persistent --headed https://claude.ai/new
```

### Change model

```bash
# Open the model selector
playwright-cli click "getByTestId('model-selector-dropdown')"

# Then click the desired model (pick one):
playwright-cli click "getByRole('menuitem', { name: 'Opus 4.6 Most capable' })"
playwright-cli click "getByRole('menuitem', { name: 'Sonnet 4.6 Most efficient' })"
playwright-cli click "getByRole('menuitem', { name: 'Haiku 4.5 Fastest for quick' })"
```

### Type a prompt and submit (each command is a SEPARATE Bash call — never chain with &&)

```bash
playwright-cli open --browser=chrome --persistent --headed https://claude.ai/new
playwright-cli fill "getByRole('textbox', { name: 'Write your prompt to Claude' })" "your message here"
playwright-cli press Enter
```

### Critical rules

- **Never chain commands with `&&`** — kills the browser session; run each as a separate Bash call
- **Always `--headed`** — headless is blocked by Cloudflare
- **Always `--persistent`** — saves login session across runs
- **Always use role locators** (`getByRole`) not element refs — refs change every session
- **Session drops frequently** — check with `playwright-cli snapshot` before interacting; reopen if needed
- **`--persistent` reopens the last chat** — use `https://claude.ai/new` or `playwright-cli goto https://claude.ai/new` to start fresh

### What does NOT work

- `playwright-cli open https://claude.ai` — headless, Cloudflare blocks it
- `playwright-cli open --browser=chrome --persistent https://claude.ai` — still headless, still blocked

### CDW laptop (LT-AAD-F9FHV96C) — Edge + Gemini

On the CDW corporate laptop, corporate security software locks Chrome's User Data profile directory, preventing `--profile` from working. Google sign-in also blocks Playwright-automated browsers ("This browser or app may not be secure"). Use **Edge with your real profile** and **Gemini** instead of claude.ai:

#### Opening Gemini (must follow this exact sequence)

```bash
# Step 1: Always close existing playwright sessions first to release profile lock
playwright-cli close-all

# Step 2: Open Gemini in Edge with the real profile
playwright-cli open --browser=msedge --headed --profile="C:\Users\jeffkit\AppData\Local\Microsoft\Edge\User Data" https://gemini.google.com/
```

#### CDW laptop rules

- **Always run `playwright-cli close-all` first** — the real Edge profile can only be used by one process; stale sessions lock it
- **Use `--browser=msedge`** — Edge's profile is not locked by security software
- **Use `--profile`** (not `--persistent`) — uses your real Edge profile with existing Google login
- **Use Gemini** — already signed in via Google; claude.ai requires a separate login that gets blocked
- **`--profile` restores all previous Edge tabs** — if Edge had many tabs open, they all reopen. Close Edge gracefully before launching via playwright-cli, or use `attach --cdp=msedge` to connect to an already-running Edge
- **`--profile` mode does not maintain a persistent control connection** — the `open` command exits after navigation, so subsequent `snapshot`/`click` commands may fail. Use `attach --cdp=msedge` if you need ongoing interaction with an already-running Edge
- **Do NOT use `--persistent`** — it creates a separate empty profile without Google login
- All other critical rules (no `&&` chaining, `--headed`, role locators, separate Bash calls) still apply

### playwright-cli skill

A comprehensive `playwright-cli` skill is available at `~/.claude/skills/playwright-cli/SKILL.md` with full command reference including `attach --cdp`, session management, storage, network mocking, tracing, and video recording. The skill is loaded automatically when browser automation is needed.

