# Gemini Automation Mandates (CDW Laptop)

- Whenever I am asked about skills, also check `C:\Users\huske\.claude`.

When automating browser tasks on this machine, follow these mandates to bypass corporate security locks and authentication blocks.

## Environment: CDW Laptop (LT-AAD-F9FHV96C)
- **Primary Browser:** Microsoft Edge (`msedge`)
- **Edge Profile Path:** `C:\Users\jeffkit\AppData\Local\Microsoft\Edge\User Data`
- **Session State File:** `.claude/claude_session.json`
- **Preferred AI:** Google Gemini (`https://gemini.google.com/`) or Claude (`https://claude.ai/`)

## Operational Protocol
1. **Isolated Profiles:** When using isolated profiles (e.g., `./.claude/claude_profile`), `playwright-cli close-all` is **optional**. This method allows the automated browser to run side-by-side with your main Edge browser.
2. **Main Profile (Gemini):** Using your "real" Edge profile still requires `playwright-cli close-all` to release file locks.
3. **Session Persistence (Claude):** Use the `--persistent --profile="./.claude/claude_profile"` flag.
4. **Session Injection:** Use `playwright-cli state-load .claude/claude_session.json` to inject credentials into isolated profiles.
5. **Visibility:** Always use `--headed`. Headless mode is frequently blocked by security/bot detection.
6. **Execution:** Run each interaction command as a separate call; do **NOT** chain them with `&&` as it can lead to session drops.
7. **Locators:** Prioritize role-based locators (`getByRole`, `getByTestId`) over element refs (`e1`), as they are more resilient to page updates.

## Standard Interaction Sequence
### Gemini (Main Profile Mode)
*Note: This mode REQUIRES closing your main browser.*
```bash
playwright-cli close-all
playwright-cli open --browser=msedge --headed --profile="C:\Users\jeffkit\AppData\Local\Microsoft\Edge\User Data" https://gemini.google.com/
```

### Claude / ServiceNow (Isolated Mode)
*Note: This mode can run WHILE your main browser is open.*
```bash
playwright-cli open --browser=msedge --headed --persistent --profile="./.claude/claude_profile"
playwright-cli state-load .claude/claude_session.json
playwright-cli goto https://claude.ai/new
```

### Gemini: Changing Models
To switch between Flash (Fast) and Pro:
1. Open the picker: `playwright-cli click "getByRole('button', { name: 'Open mode picker' })"`
2. Select Flash: `playwright-cli click "getByRole('menuitem', { name: 'Fast Answers quickly' })"`
3. Select Pro: `playwright-cli click "getByRole('menuitem', { name: 'Pro Advanced math and code with 3.1 Pro' })"`
4. Select Thinking: `playwright-cli click "getByRole('menuitem', { name: 'Thinking Solves complex problems' })"`

### NotebookLM: Authentication Refresh
If the `notebooklm` skill/program reports "Authentication expired":
1. The only reliable way to refresh the login is to run `notebooklm login` manually in a terminal session.
2. After the browser appears and you are logged in, you **must press Enter** in the terminal to save the session data.
3. This process may require manual execution by the user if the automated agent cannot complete the interactive handshake.
