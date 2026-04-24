---
name: Refresh claude_session.json via Edge CDP debug port
description: When claude_session.json cookies go stale, capture fresh ones by launching Edge with --remote-debugging-port, logging in manually, attaching via CDP, and running state-save
type: feedback
originSessionId: 51d0cd38-78a3-4a6a-83f0-8cc1f37fa31d
---
To refresh `claude_session.json` with fresh authentication cookies, launch Edge with remote debugging enabled, log in manually in your real Edge profile, then attach via CDP and save state.

**Why:** The Session Injection workflow needs a valid `claude_session.json` to inject. When those cookies expire, you need to capture new ones. The user prefers logging in through their real Edge profile (which already has saved passwords, MFA trust, etc.) rather than logging in again inside a playwright-controlled isolated profile. `attach --cdp` works when Edge is launched with `--remote-debugging-port`.

**How to apply:**
1. Close all playwright sessions and Edge to release profile locks:
   ```bash
   playwright-cli close-all
   ```
   ```powershell
   Stop-Process -Name msedge -Force -ErrorAction SilentlyContinue; Start-Sleep -Seconds 2
   ```
2. Launch Edge manually with remote debugging port and claude.ai:
   ```powershell
   Start-Process "msedge.exe" -ArgumentList "--remote-debugging-port=9222","https://claude.ai/new"
   ```
3. User logs in manually (real Edge profile, SSO / MFA as normal).
4. Once user confirms logged in, attach AND state-save in the same Bash call (attach doesn't persist the session across separate invocations, so chain with `&&`):
   ```bash
   playwright-cli attach --cdp=http://localhost:9222 && playwright-cli state-save claude_session.json
   ```
5. Copy to safekeeping:
   ```bash
   cp claude_session.json ~/.claude/claude_session.json
   ```

**Key gotcha:** `playwright-cli attach` does NOT support `--persistent`. If you run `attach` in one Bash call and `state-save` in the next, the second call errors with "Browser 'default' is not open." Chain them with `&&` in a single Bash call so state-save runs while attach's session is still alive.
