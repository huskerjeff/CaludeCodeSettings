---
name: Session Injection technique for playwright-cli
description: Use isolated profile + cookie injection to bypass profile locks and Cloudflare blocks when automating claude.ai or other auth-protected sites
type: feedback
originSessionId: 587782e4-14fd-49ea-9b34-fb4928ec5c82
---
"Session Injection" technique enables playwright-cli to open auth-protected sites (claude.ai, etc.) without fighting over browser profile locks or getting blocked by Cloudflare/login security.

**Why:** On the CDW laptop, the real Edge profile is locked when Edge is open (only one process can use it), and Cloudflare/Google block automated browser logins. This technique solves both problems.

**How to apply:**
1. **Create an isolated profile** — use a private profile directory (e.g., `.claude/claude_profile`) instead of the real Edge profile. This lets the automated browser and manual browser run side-by-side.
2. **Save auth cookies once** — from a working authenticated session, run `playwright-cli state-save claude_session.json` to capture authentication cookies.
3. **Inject cookies before navigating** — on subsequent runs, use `playwright-cli state-load claude_session.json` to load saved cookies into the isolated profile BEFORE navigating to the target site. The site sees a "known, logged-in user" instead of a bot.
4. **Open with persistent isolated profile:**
   ```bash
   playwright-cli open --browser=msedge --headed --persistent --profile=".claude/claude_profile" https://claude.ai/new
   playwright-cli state-load claude_session.json
   ```

**Key advantage over `--profile` with real User Data:** 
- No profile lock conflicts — can run alongside normal Edge
- `--persistent` maintains control connection (snapshot, click, etc. keep working)
- Cookies persist across sessions in the isolated profile
- Avoids restoring 25+ previous Edge tabs
