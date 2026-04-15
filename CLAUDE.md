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

