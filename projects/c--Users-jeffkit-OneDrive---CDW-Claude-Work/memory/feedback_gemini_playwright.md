---
name: Gemini means playwright-cli Edge
description: When user asks to open Gemini, use playwright-cli with Edge and real profile to open gemini.google.com — includes known limitations and workarounds
type: feedback
originSessionId: 587782e4-14fd-49ea-9b34-fb4928ec5c82
---
When the user asks to "open Gemini", they mean use playwright-cli to open gemini.google.com in Edge with their real profile.

**Why:** On the CDW laptop, Chrome's profile is locked by corporate security software, and Google blocks automated browser login. Edge with the real profile works and is already signed into Google.

**How to apply:**
1. Always run `playwright-cli close-all` first to release stale profile locks
2. Then run: `playwright-cli open --browser=msedge --headed --profile="C:\Users\jeffkit\AppData\Local\Microsoft\Edge\User Data" https://gemini.google.com/`
3. Follow all playwright-cli critical rules (no && chaining, separate Bash calls, --headed, role locators)

**Known limitations:**
- `--profile` mode does NOT maintain a persistent control connection — the `open` command exits after navigation, so `snapshot`, `click`, etc. will fail afterward
- `--profile` restores ALL previous Edge tabs — if Edge had 25 tabs open, they all reopen. User fixed this by changing Edge's startup setting to "open new tab page"
- `--persistent` does NOT work — creates an empty profile without Google login
- `attach --cdp=msedge` requires Edge to have been launched with remote debugging enabled (DevToolsActivePort); normal Edge launches don't have this — still investigating as a workaround for ongoing interaction
- To interact with Gemini after opening (e.g., change model), may need to relaunch Edge with `--remote-debugging-port` flag, or user does it manually
