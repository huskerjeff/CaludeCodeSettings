---
name: Prefer mouse-free automation when possible
description: When automating UI on the user's active machine, prefer methods that don't move the mouse cursor (UIA Invoke, keyboard shortcuts) so the user can keep working
type: feedback
originSessionId: 461c6eb3-f466-4f3f-b3c4-c04df34e5bf3
---
For UI automation on the user's active workstation, prefer techniques that don't take over the mouse cursor. Real mouse clicks (uiautomation's `Click`, pyautogui) move the cursor visibly and conflict with the user's own input — if they happen to move the mouse mid-script, the click misses and silently fails.

**Why:** During the claude.ai model-selector test (2026-05-02), I used `simulateMove=True` mouse clicks and the user moved the mouse during one run, causing the click to miss. They explicitly asked for the mouse-free path: "Let try that option B that is mouse free."

**How to apply:**
- Try `InvokePattern.Invoke()` for buttons before falling back to mouse clicks. UIA invoke fires the underlying handler without touching the cursor.
- For radio buttons, `GetSelectionItemPattern().Select()` is the no-mouse equivalent.
- Caveat: React web content sometimes only responds to real mouse events. If invoke doesn't trigger the UI, fall back to mouse — but inform the user before doing so.
- Don't combine real mouse clicks with steps that take the user > a few seconds to react. Either commit to mouse and warn them, or stay mouse-free.
