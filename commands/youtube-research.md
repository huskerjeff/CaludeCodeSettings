---
description: "Automated YouTube → NotebookLM research pipeline. Pass a topic, a channel, or a YouTube URL. Usage: /youtube-research <topic|url> [--channel @Handle] [-n COUNT] [--pick-best] [--output podcast|infographic|report|video|quiz|flashcards|slide-deck|mind-map]"
---

# YouTube → NotebookLM Research Pipeline

You are executing an automated research pipeline. The user's input is: **$ARGUMENTS**

Parse the arguments:
- **output** = value after `--output` flag (default: `infographic,report`)
- **pick_best** = number after `--pick-best N` if provided (e.g. `--pick-best 6` → `6`); `true` if flag present with no number (selects 5–8 automatically); `false` if flag absent
- **channel** = value after `--channel` flag (e.g. `@VMware`), or `null` if not provided
- **count** = value after `-n` or `--max-results` flag (default: `10`)
- **input** = everything remaining after stripping `--output`, `--pick-best`, `--channel`, `-n`/`--max-results` and their values
- **search_args** = reconstructed from `input` + `--channel <channel>` (if present) + `-n <count>`
- **mode** = detect from input:
  - If input starts with `https://www.youtube.com` or `https://youtu.be` → **URL mode** (single video)
  - Otherwise → **Search mode**

---

## STEP 01 — PRE-FLIGHT

Run auth check and validate inputs:

```bash
notebooklm auth check --json
```

If auth fails, stop and tell the user to run `notebooklm login` first.

Confirm input is non-empty. If nothing provided, stop and ask the user for a topic or URL.

**If URL mode:** fetch the video title using yt-dlp to use as the notebook name:
```bash
python "C:/Users/jeffkit/.claude/skills/youtube-search/scripts/yt_scraper.py" "<url>" --max-results 1
```
Extract `title` from the result. Set `NOTEBOOK_TITLE` = the video title. Set `SLUG` = lowercase-hyphenated version of the title (truncated to 40 chars).

**If Search mode:** set `NOTEBOOK_TITLE` = `Research: <topic>`. Set `SLUG` = `<topic-slug>`.

Print status:
```
✅ Pre-flight complete
📌 Mode: [URL | Search]
📌 Input: <url or topic>
📦 Output: <output>
```

---

## STEP 02 — SEARCH YOUTUBE *(Search mode only — skip if URL mode)*

Invoke the **youtube-search skill** passing through all search arguments: topic (if any), `--channel` (if provided), and `-n <count>`.

The skill calls `yt_scraper.py` with the appropriate mode:
- Topic only → search mode
- `--channel` only → channel browse mode (newest first, no Shorts)
- Topic + `--channel` → channel+topic filter mode (newest first, no Shorts)

After the skill returns results, show the user a numbered list:
```
🔍 Found N videos:
1. [Title] — [Channel] ([views] views, [date])
2. ...
```

---

## STEP 03 — AUTO-SELECT BEST VIDEOS *(only runs if `--pick-best` flag was passed)*

If `--pick-best` was **not** specified: use all returned videos as sources and skip to Step 04.

If `--pick-best` **was** specified: select videos from the results using these criteria (score each):

| Criterion | Signal |
|-----------|--------|
| **Relevance** | Title/captions closely match topic |
| **Engagement** | Higher view count |
| **Recency** | More recent upload_date preferred |
| **Depth** | Longer duration + captions available |
| **Diversity** | Different channels / angles |

Target count:
- `--pick-best N` → select exactly N videos
- `--pick-best` (no number) → select 5–8 automatically

Discard videos with no captions unless the title is highly relevant.

Print your selections with a one-line rationale for each:
```
🎯 Selected N videos:
1. [Title] — relevance: high, views: 1.2M, captions: ✅
2. ...
```

---

## STEP 04 — CREATE NOTEBOOK

Create a new NotebookLM notebook titled `NOTEBOOK_TITLE`:

```bash
notebooklm create "<NOTEBOOK_TITLE>" --json
```

Parse and store the `id` field as `NOTEBOOK_ID`. Use this explicit ID for all subsequent commands (never rely on `notebooklm use`).

Print:
```
📓 Notebook created: <NOTEBOOK_TITLE> (ID: <NOTEBOOK_ID>)
```

---

## STEP 05 — ADD SOURCES

**If URL mode:** add the single video URL:
```bash
notebooklm source add "<url>" --notebook <NOTEBOOK_ID> --json
```

**If Search mode:** add each selected video URL one at a time:
```bash
notebooklm source add "<youtube_url>" --notebook <NOTEBOOK_ID> --json
```

Collect all returned `source_id` values. If a source fails, log a warning and continue with the rest.

After all adds, wait for processing:

```bash
notebooklm source list --json --notebook <NOTEBOOK_ID>
```

Poll every 20 seconds until all sources show `status: ready` (timeout: 5 minutes). Report progress as sources come online.

Print:
```
📥 Sources added: N/N ready
```

---

## STEP 06 — ANALYZE *(Search mode only — skip if URL mode)*

Run 3 deep analysis questions against the notebook to build understanding:

```bash
notebooklm ask "What are the key themes, insights, and debates across all these sources on <topic>?" --notebook <NOTEBOOK_ID>
notebooklm ask "What are the most important facts, statistics, and expert opinions presented?" --notebook <NOTEBOOK_ID>
notebooklm ask "What are the practical takeaways and open questions about <topic>?" --notebook <NOTEBOOK_ID>
```

Summarize the answers in 3–5 bullet points per question. Display to the user as a **Research Brief**.

---

## STEP 07 — DELIVERABLE

Generate the requested output(s). Default is both infographic AND briefing-doc report.

### Infographic (default)
```bash
notebooklm generate infographic --notebook <NOTEBOOK_ID> --orientation landscape --detail standard --json
```
Parse `artifact_id`. Then wait and download:
```bash
notebooklm artifact wait <artifact_id> --notebook <NOTEBOOK_ID> --timeout 900
notebooklm download infographic ./research-<topic-slug>-infographic.png --artifact <artifact_id> --notebook <NOTEBOOK_ID>
```

### Briefing Report (default)
```bash
notebooklm generate report --format briefing-doc --notebook <NOTEBOOK_ID> --json
```
Parse `artifact_id`. Then wait and download:
```bash
notebooklm artifact wait <artifact_id> --notebook <NOTEBOOK_ID> --timeout 900
notebooklm download report ./research-<topic-slug>-briefing.md --artifact <artifact_id> --notebook <NOTEBOOK_ID>
```

### Other outputs (if `--output` was specified)

| Flag value | Command |
|------------|---------|
| `podcast` | `notebooklm generate audio "Deep dive on <topic>" --notebook <NOTEBOOK_ID> --json` |
| `video` | `notebooklm generate video "Explainer on <topic>" --notebook <NOTEBOOK_ID> --json` |
| `quiz` | `notebooklm generate quiz --notebook <NOTEBOOK_ID> --json` |
| `flashcards` | `notebooklm generate flashcards --notebook <NOTEBOOK_ID> --json` |
| `slide-deck` | `notebooklm generate slide-deck --notebook <NOTEBOOK_ID> --json` |
| `mind-map` | `notebooklm generate mind-map --notebook <NOTEBOOK_ID> --json` |
| `study-guide` | `notebooklm generate report --format study-guide --notebook <NOTEBOOK_ID> --json` |

For each: parse `artifact_id`, wait with `artifact wait`, then download to `./research-<topic-slug>-<type>.<ext>`.

⚠️ If generation fails due to rate limiting, tell the user and suggest retrying in 5–10 minutes with:
```bash
notebooklm generate <type> --notebook <NOTEBOOK_ID> --retry 2
```

---

## COMPLETION SUMMARY

Print a final summary:

**If Search mode:**
```
✅ Research pipeline complete for: "<topic>"

📓 Notebook: <NOTEBOOK_TITLE> (ID: <NOTEBOOK_ID>)
📥 Sources: N YouTube videos
📊 Deliverables saved:
   - research-<slug>-infographic.png
   - research-<slug>-briefing.md

💡 Research Brief:
[3–5 key insights from Step 06]

🔗 Continue in NotebookLM: https://notebooklm.google.com
```

**If URL mode:**
```
✅ Video added to NotebookLM

📓 Notebook: <NOTEBOOK_TITLE> (ID: <NOTEBOOK_ID>)
📥 Source: 1 video (ready)
📊 Deliverables saved:
   - research-<slug>-infographic.png
   - research-<slug>-briefing.md

🔗 Continue in NotebookLM: https://notebooklm.google.com
```
