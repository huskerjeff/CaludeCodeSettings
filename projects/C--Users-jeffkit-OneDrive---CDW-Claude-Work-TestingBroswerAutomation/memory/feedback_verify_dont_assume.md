---
name: Verify before assuming an action failed
description: Check the visible result before chasing a "fix" — assumptions about iframes, focus, or framework quirks are often wrong
type: feedback
originSessionId: 61e5120a-47d5-4e14-b08d-079b45eecdeb
---
When an action seems like it *might* not have worked (e.g., a keypress that "should" have hit an iframe), do not preemptively pivot to a more complex fallback. Verify the actual outcome first — ask the user, take a snapshot, or inspect state.

**Why:** On 2026-05-04, after `playwright-cli press "Control+End"` on a ServiceNow ticket page, I assumed the keystroke wouldn't scroll the iframe content and immediately tried `eval` with `#gsft_main`. The user interrupted: Ctrl+End had already worked. The unnecessary fallback wasted a turn and the user had to correct me.

**How to apply:** After any UI action where the result is visually verifiable, prefer "did it work?" over "here's why it probably didn't." For ServiceNow specifically: keyboard scroll (`Control+End`, `Control+Home`, `PageDown`) does reach the active form even when content is iframed — don't assume otherwise.
