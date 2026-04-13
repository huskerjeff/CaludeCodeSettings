# Playwright CLI Skill — Installation Instructions for Claude

This package contains the `playwright-cli` Claude Code skill. Follow these steps to install it on a new machine.

---

## Step 1: Install the npm package

Run this in the terminal:

```bash
npm install -g @playwright/cli@latest
```

Verify:

```bash
playwright-cli --version
```

If the global command is unavailable, use `npx playwright-cli` in all commands.

---

## Step 2: Install the skill files into the project

Copy the skill folder into the `.claude/skills/` directory of the target project:

```bash
# From the location of this package, run:
mkdir -p /path/to/project/.claude/skills/playwright-cli/references

cp SKILL.md /path/to/project/.claude/skills/playwright-cli/
cp references/* /path/to/project/.claude/skills/playwright-cli/references/
```

On Windows (bash):

```bash
mkdir -p /c/path/to/project/.claude/skills/playwright-cli/references
cp SKILL.md /c/path/to/project/.claude/skills/playwright-cli/
cp references/* /c/path/to/project/.claude/skills/playwright-cli/references/
```

---

## Step 3: Verify the skill is loaded

Start a new Claude Code session in the project. The `playwright-cli` skill should appear in the available skills list. You can test it with:

```bash
playwright-cli --version
```

---

## How to use the skill to automate claude.ai

### Open claude.ai (MUST use --headed or Cloudflare blocks it)

```bash
playwright-cli open --browser=chrome --persistent --headed https://claude.ai/new
```

### Change the model

```bash
playwright-cli click "getByTestId('model-selector-dropdown')"
# Then pick one:
playwright-cli click "getByRole('menuitem', { name: 'Opus 4.6 Most capable' })"
playwright-cli click "getByRole('menuitem', { name: 'Sonnet 4.6 Most efficient' })"
playwright-cli click "getByRole('menuitem', { name: 'Haiku 4.5 Fastest for quick' })"
```

### Type a prompt and submit

```bash
playwright-cli fill "getByRole('textbox', { name: 'Write your prompt to Claude' })" "your message here"
playwright-cli press Enter
```

### Critical rules
- **Never chain commands with `&&`** — run each as a separate Bash tool call or terminal command
- **Use role locators** for the prompt field — element refs (e.g. `e291`) change every session
- **Browser session drops frequently** — check with `playwright-cli snapshot` and reopen if needed
- **`--persistent` reopens the last active chat** — use `https://claude.ai/new` to start fresh
