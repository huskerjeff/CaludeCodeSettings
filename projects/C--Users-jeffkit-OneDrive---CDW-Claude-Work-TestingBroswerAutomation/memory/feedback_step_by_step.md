---
name: Verify each step before chaining
description: When automation has multiple steps (find element → click → wait → click again), prove each step works in isolation before stringing them together
type: feedback
originSessionId: 461c6eb3-f466-4f3f-b3c4-c04df34e5bf3
---
When building multi-step browser/UI automation, do not chain all the steps in one script and run it end-to-end. Test each step in isolation first.

**Why:** During the claude.ai model-selector test (2026-05-02), I built a 5-step end-to-end script (open page → find button → click → find Haiku radio → click). Step 4 failed and we couldn't tell if the cause was "dropdown didn't open," "wrong button clicked," "timing too short," or "Haiku locator wrong." Had to add diagnostics and rerun. The user pulled me back: "just click the model dropdown box" — one step, verify visually, then continue.

**How to apply:**
- Default to single-action scripts during exploration. One script clicks the model selector. Period. Run it. Confirm the dropdown is visible. Then write the next script.
- Only collapse into a chained end-to-end script after each step is independently proven.
- Diagnostic dumps go in throwaway probe scripts, not in the "production" flow.
- Especially relevant for UIA / playwright-cli / pyautogui — failures are often silent and hard to attribute when steps are stacked.
