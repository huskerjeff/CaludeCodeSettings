# Playwright CLI Guide

Source: originally saved in `ClaudeCode_Life/Mem/reference_playwright_cli_full_guide.md`
Also copied to: `~/.claude/CLAUDE.md`

---

## Installation

```bash
npm install -g @playwright/cli@latest
playwright-cli --version
```

If the global command isn't available, use `npx playwright-cli` in its place.

## Opening claude.ai (Cloudflare bypass)

You MUST use `--headed` — without it, Cloudflare detects Playwright as a bot and blocks access.
`--persistent` saves the session so you stay logged in across runs.

```bash
playwright-cli open --browser=chrome --persistent --headed https://claude.ai/new
```

### What does NOT work
- `playwright-cli open https://claude.ai` — headless, Cloudflare blocks it
- `playwright-cli open --browser=chrome --persistent https://claude.ai` — still headless, still blocked
- `playwright-cli open --browser=chrome --profile="%LOCALAPPDATA%/Google/Chrome/User Data"` — also blocked (headless)
- `playwright-cli attach --extension` — requires "Playwright MCP Bridge" Chrome extension

## Changing the model

```bash
# Open the model selector
playwright-cli click "getByTestId('model-selector-dropdown')"

# Select a model (pick one):
playwright-cli click "getByRole('menuitem', { name: 'Opus 4.6 Most capable' })"
playwright-cli click "getByRole('menuitem', { name: 'Sonnet 4.6 Most efficient' })"
playwright-cli click "getByRole('menuitem', { name: 'Haiku 4.5 Fastest for quick' })"
```

## Typing a prompt and submitting

```bash
# Step 1: Open browser (reopen if session dropped)
playwright-cli open --browser=chrome --persistent --headed https://claude.ai/new

# Step 2: (Optional) Change model — see section above

# Step 3: Fill the prompt using the stable role locator
playwright-cli fill "getByRole('textbox', { name: 'Write your prompt to Claude' })" "your message here"

# Step 4: Submit
playwright-cli press Enter
```

After submitting, the URL changes to `/chat/<uuid>` and the page title becomes the chat topic.

## Critical rules

- **Never chain commands with `&&`** — this kills the browser session. Run each `playwright-cli` command as a separate Bash tool call.
- **Always use role locators** for the prompt field, not element refs (`e291` etc.) — refs change every session.
- **The browser session drops frequently** — always check with `playwright-cli snapshot` before interacting and reopen if needed.
- **`--persistent` reopens the last active chat** — use `https://claude.ai/new` in the open command or `playwright-cli goto https://claude.ai/new` to start fresh.
