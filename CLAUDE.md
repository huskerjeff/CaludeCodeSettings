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

### Change model (claude.ai)

The model selector button shows the current model name (e.g., "Sonnet 4.6"). Click it to open the dropdown, then select a model. Each command is a separate Bash call.

```bash
# Step 1: Open the model selector (click the button showing current model name)
playwright-cli snapshot  # check current state first
playwright-cli click "getByRole('button', { name: 'Sonnet 4.6' })"  # or whatever model name is shown

# Step 2: Select desired model (pick one):
playwright-cli click "getByRole('menuitemradio', { name: 'Opus 4.7 Most capable for ambitious work' })"
playwright-cli click "getByRole('menuitemradio', { name: 'Sonnet 4.6 Most efficient for everyday tasks' })"
playwright-cli click "getByRole('menuitemradio', { name: 'Haiku 4.5 Fastest for quick answers' })"
```

**Note:** Model names and roles change over time. If a locator fails, take a `snapshot` and inspect the actual menu items. The role changed from `menuitem` to `menuitemradio` and model descriptions updated (e.g., "Most capable" → "Most capable for ambitious work"). Always verify with a snapshot first.

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

### CDW laptop (LT-AAD-F9FHV96C) — Edge + Gemini/Claude

On the CDW corporate laptop, corporate security software locks Chrome's User Data profile directory, and Google blocks automated browser login. Use **Edge** for all browser automation.

**Session state file:** `C:\Users\jeffkit\.claude\claude_session.json`
**Isolated profile:** `./.claude/claude_profile`

#### Opening Claude (Session Injection — preferred, maintains control connection)

Each command is a SEPARATE Bash call — never chain with `&&`.

```bash
# Step 1: Close existing playwright sessions to release profile locks
playwright-cli close-all

# Step 2: Open Edge with isolated persistent profile (do NOT navigate to claude.ai yet)
playwright-cli open --browser=msedge --headed --persistent --profile="./.claude/claude_profile"

# Step 3: Load saved auth cookies (the session file must be in the working directory or under it)
# If the file is at ~/.claude/claude_session.json, copy it to the working directory first
playwright-cli state-load claude_session.json

# Step 4: NOW navigate to Claude
playwright-cli goto https://claude.ai/new
```

**How Session Injection works:**

The core problem: Cloudflare and claude.ai block automated browsers that aren't authenticated. You can't log in through the automated browser because security checks detect Playwright. The solution is **cookie teleportation** — capture authentication cookies from a working session and inject them into a clean, isolated browser profile before navigating to the site.

1. **Isolated profile** (`./.claude/claude_profile`): A private, playwright-managed browser profile separate from your real Edge profile. This avoids "profile in use" locks so the automated browser and your normal Edge can run side-by-side. Unlike `--profile` with real Edge User Data, this does NOT restore previous tabs.
2. **`--persistent`**: Keeps the playwright control connection alive after opening. Without it, the `open` command exits and you lose the ability to `snapshot`, `click`, `goto`, etc. This is critical for any interaction beyond just opening a page.
3. **`state-load` (cookie injection)**: Loads saved authentication cookies (`claude_session.json`) into the browser context. These cookies contain the digital proof that you've already logged in and passed Cloudflare's security checks. When the page loads, it sees a "known, logged-in user" rather than a "suspicious new bot."
4. **Order matters**: You MUST load cookies BEFORE navigating to claude.ai. If you pass the URL in the `open` command, the browser navigates immediately without cookies and gets blocked. Open to `about:blank` first → inject cookies → THEN `goto`.

**Session state file (`claude_session.json`):**
- Contains authentication cookies (session tokens, Cloudflare clearance, etc.)
- Created with `playwright-cli state-save claude_session.json`
- Stored at `~/.claude/claude_session.json` for safekeeping
- Must be copied to the working directory before `state-load` (sandbox restricts file access to working directory)
- **When cookies go stale**, refresh them via the CDP procedure in `~/.claude/reference/CDP-Session-Refresh-Process.md` (launch Edge with `--remote-debugging-port=9222`, user logs in, then `playwright-cli attach --cdp=http://localhost:9222 && playwright-cli state-save claude_session.json`)
- Cookies expire over time — if `goto` redirects to `/logout` or login page, recapture by logging in manually and running `state-save` again

**First-time setup:**
1. Run `playwright-cli open --browser=msedge --headed --persistent --profile="./.claude/claude_profile"`
2. Log in to claude.ai manually in the browser that opens
3. Run `playwright-cli state-save claude_session.json` to capture cookies
4. Copy to safekeeping: `cp claude_session.json ~/.claude/claude_session.json`

**If `state-load` gives "File access denied":** The file must be under the working directory. Copy it first: `cp ~/.claude/claude_session.json .`

#### Opening Gemini (Profile Mode — no ongoing control)

```bash
# Step 1: Close existing playwright sessions
playwright-cli close-all

# Step 2: Open Gemini in Edge with the real profile
playwright-cli open --browser=msedge --headed --profile="C:\Users\jeffkit\AppData\Local\Microsoft\Edge\User Data" https://gemini.google.com/
```

**Note:** `--profile` with the real Edge profile does NOT maintain a control connection — the `open` command exits after navigation. Use this only when you just need to open a page, not interact with it. Also restores all previous Edge tabs — close Edge first if you don't want that.

#### CDW laptop rules

- **Always run `playwright-cli close-all` first** — stale sessions lock profiles
- **Use `--browser=msedge`** — Chrome's profile is locked by corporate security software
- **For ongoing interaction (click, snapshot, model changes)** — use Session Injection (Claude method above)
- **For just opening a page** — use Profile Mode (Gemini method above)
- All critical rules apply: no `&&` chaining, `--headed`, role locators, separate Bash calls

#### What does NOT work on CDW laptop (lessons learned)

- **`--browser=chrome` with `--profile`** — corporate security software (endpoint protection) locks Chrome's User Data directory even after Chrome is closed. Edge is not affected.
- **Google SSO in playwright-automated browsers** — Google detects Playwright's automation flags (`--remote-debugging-port`, `--enable-automation`) and blocks login with "This browser or app may not be secure"
- **`--persistent` alone for claude.ai** — creates a new empty profile with no auth cookies. You must inject cookies via `state-load` or log in manually first.
- **Passing a URL in the `open` command with Session Injection** — navigating immediately (e.g., `playwright-cli open ... https://claude.ai/new`) causes the session to drop before you can load cookies. Always open to `about:blank` first, load cookies, THEN `goto`.
- **`--profile` with real Edge User Data for ongoing control** — the `open` command exits after navigation, losing the control connection. `snapshot`, `click`, and other interaction commands fail afterward. Only use `--profile` when you just need to open a page.
- **`--profile` with real Edge User Data restores all previous tabs** — if Edge had 25 tabs open, they all reopen. Changing Edge's `restore_on_startup` preference programmatically does not reliably prevent this.
- **`attach --cdp=msedge`** — requires Edge to have been launched with remote debugging enabled (`DevToolsActivePort`). Normal Edge launches and playwright `--profile` launches do not enable this.
- **`playwright-cli kill-all`** — does not release profile locks held by Edge processes started via `--profile`. Use `powershell Stop-Process -Name msedge` if `close-all` doesn't work.

### playwright-cli skill

A comprehensive `playwright-cli` skill is available at `~/.claude/skills/playwright-cli/SKILL.md` with full command reference including `attach --cdp`, session management, storage, network mocking, tracing, and video recording. The skill is loaded automatically when browser automation is needed.

---

## Automating Windows Desktop Apps (Calculator, etc.) with PowerShell

Use UI Automation to click named buttons — more reliable than SendKeys for UWP apps like Calculator.

### Open an app

```bash
start calc       # Calculator
start notepad    # Notepad
```

### Interact with Calculator via UI Automation (preferred)

```powershell
Add-Type -AssemblyName UIAutomationClient
Add-Type -AssemblyName UIAutomationTypes

$desktop = [System.Windows.Automation.AutomationElement]::RootElement
$calcCondition = New-Object System.Windows.Automation.PropertyCondition(
    [System.Windows.Automation.AutomationElement]::NameProperty, 'Calculator')
$calc = $desktop.FindFirst([System.Windows.Automation.TreeScope]::Children, $calcCondition)

function Click-Button($name) {
    $condition = New-Object System.Windows.Automation.PropertyCondition(
        [System.Windows.Automation.AutomationElement]::NameProperty, $name)
    $btn = $calc.FindFirst([System.Windows.Automation.TreeScope]::Descendants, $condition)
    $invoke = $btn.GetCurrentPattern([System.Windows.Automation.InvokePattern]::Pattern)
    $invoke.Invoke()
    Start-Sleep -Milliseconds 150
}

# Example: 5 x 4 = 20
Click-Button 'Clear'
Click-Button 'Five'
Click-Button 'Multiply by'
Click-Button 'Four'
Click-Button 'Equals'
```

### Button names reference (Standard/Scientific mode)

| Button | Name |
|--------|------|
| 0–9 | `Zero` `One` `Two` ... `Nine` |
| + | `Plus` |
| - | `Minus` |
| × | `Multiply by` |
| ÷ | `Divide by` |
| = | `Equals` |
| C | `Clear` |
| ⌫ | `Backspace` |
| . | `Decimal separator` |

### Key notes

- **Always `Click-Button 'Clear'` first** — clears previous result before a new calculation.
- **`AppActivate` does NOT work for UWP apps** — throws "Process not found" even when process exists.
- **SendKeys is unreliable for UWP** — focus issues cause keystrokes to go to wrong window or carry over previous state.
- **If `$calc` is null**, app may not be open yet — add `Start-Sleep -Milliseconds 1500` after `start calc`.
- **Discover button names**: `$calc.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition) | ForEach-Object { $_.Current.Name }`

