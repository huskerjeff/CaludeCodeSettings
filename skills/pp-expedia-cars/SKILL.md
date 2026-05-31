---
name: pp-expedia-cars
description: "Printing Press CLI for Expedia Cars. Discovered API spec for browser-intake-us5-datadoghq"
author: "Jeff Kittrell"
license: "Apache-2.0"
argument-hint: "<command> [args] | install cli|mcp"
allowed-tools: "Read Bash"
metadata:
  openclaw:
    requires:
      bins:
        - expedia-cars-pp-cli
---

# Expedia Cars — Printing Press CLI

## Prerequisites: Install the CLI

This skill drives the `expedia-cars-pp-cli` binary. **You must verify the CLI is installed before invoking any command from this skill.** If it is missing, install it first:

1. Install via the Printing Press installer:
   ```bash
   npx -y @mvanhorn/printing-press install expedia-cars --cli-only
   ```
2. Verify: `expedia-cars-pp-cli --version`
3. Ensure `$GOPATH/bin` (or `$HOME/go/bin`) is on `$PATH`.

If the `npx` install fails before this CLI has a public-library category, install Node or use the category-specific Go fallback after publish.

If `--version` reports "command not found" after install, the install step did not put the binary on `$PATH`. Do not proceed with skill commands until verification succeeds.

Discovered API spec for browser-intake-us5-datadoghq

## Vendor Exclusions

Always filter out the following vendors from any results before presenting to the user:

- **ACE Rent A Car** — excluded by user preference
- **Easirent** — excluded by user preference

If results are retrieved via DOM extraction or API response, remove any listing whose vendor name contains "ACE" or "Easirent" before displaying.

## HTTP Transport

This CLI uses Chrome-compatible HTTP transport over HTTP/3 for browser-facing endpoints. It does not require a resident browser process for normal API calls.

## Discovery Signals

This CLI was generated with browser-observed traffic context.
- Capture coverage: 171 API entries from 337 total network entries
- Protocols: graphql (92% confidence), rest_json (75% confidence)
- Auth signals: cookie — cookies: CRQS, CRQSS, DUAID, EG_ANONTOKEN, HMS, IDE, KRTBCOOKIE_377, MC1, MR, MUID, NID, NavActions, PugT, TDCPM, TDID, __Host-3PLSID, __Secure-3PAPISID, __Secure-3PSID, __Secure-3PSIDCC, __Secure-3PSIDRTS, __Secure-3PSIDTS, _abck, _dd_s, _fbp, _gcl_au, _uetsid, _uetvid, ak_bmsc, barometric[cuid], bm_lso, bm_s, bm_so, bm_ss, bm_sv, bm_sz, c, cesc, currency, eg_adblock, eg_ppid, g_state, iEAPID, linfo, pageVisited, page_name, session_id, tpid, ttd_TDID, tuuid, tuuid_lu, xdid; api_key — query: dd-api-key, inAuthId, key
- Generation hints: browser_clearance_required, requires_browser_auth, requires_protected_client
- Candidate command ideas: create_2x2.json — Derived from observed POST /cl/2x2.json traffic.; create_NpJ2or — Derived from observed POST /k4AZ50DsywoM/SlBOW8/_KqZ0-/Sz3D2J7Quhfi/LkNVBTN0TwM/DUUTBl/NpJ2or traffic.; create_collect — Derived from observed POST /egcs/v2/collect traffic.; create_graphql — Derived from observed POST /graphql traffic.; create_pix — Derived from observed POST /trvl-px/v2/pix traffic.; create_rum — Derived from observed POST /api/v2/rum traffic.; create_track — Derived from observed POST /api/uisprime/track traffic.; get_conversion — Derived from observed GET /pagead/conversion/{id}/ traffic.
- Caveats: empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.; empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.; empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.; empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.; empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.; empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.; empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.; empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.; empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.; empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.

## Command Reference

**.well-known** — Operations on web-identity

- `expedia-cars-pp-cli .well-known` — GET /.well-known/web-identity

**cl** — Operations on 2x2.json

- `expedia-cars-pp-cli cl` — POST /cl/2x2.json

**ds** — Operations on pwa

- `expedia-cars-pp-cli ds <id>` — GET /ds/api/v1/toolkit/page.Car-Search/{id}/en_US/pwa

**egcs** — Operations on collect

- `expedia-cars-pp-cli egcs` — POST /egcs/v2/collect

**getconfig** — Operations on sodar

- `expedia-cars-pp-cli getconfig` — GET /getconfig/sodar

**graphql** — Operations on graphql

- `expedia-cars-pp-cli graphql` — POST /graphql

**gsi** — Operations on status

- `expedia-cars-pp-cli gsi list_listaccounts` — GET /gsi/fedcm/listaccounts
- `expedia-cars-pp-cli gsi list_passive.json` — GET /gsi/fedcm/config/passive.json
- `expedia-cars-pp-cli gsi list_status` — GET /gsi/status

**k4AZ50DsywoM** — Operations on NpJ2or

- `expedia-cars-pp-cli k4AZ50DsywoM` — POST /k4AZ50DsywoM/SlBOW8/_KqZ0-/Sz3D2J7Quhfi/LkNVBTN0TwM/DUUTBl/NpJ2or

**maps** — Operations on js

- `expedia-cars-pp-cli maps list_gen_204` — GET /maps/api/mapsjs/gen_204
- `expedia-cars-pp-cli maps list_js` — GET /maps/api/js

**pagead** — Operations on conversion

- `expedia-cars-pp-cli pagead <id>` — GET /pagead/conversion/{id}/

**rum** — Operations on rum

- `expedia-cars-pp-cli rum` — POST /api/v2/rum

**targeting-service** — Operations on adinfo

- `expedia-cars-pp-cli targeting-service` — GET /targeting-service/v3/adinfo

**trvl-px** — Operations on pix

- `expedia-cars-pp-cli trvl-px` — POST /trvl-px/v2/pix

**typeahead** — Operations on Las Vegas, NV, United States of America (LAS-Harry Reid Intl.)

- `expedia-cars-pp-cli typeahead` — GET /api/v4/typeahead/Las Vegas, NV, United States of America (LAS-Harry Reid Intl.)

**uisprime** — Operations on track

- `expedia-cars-pp-cli uisprime` — POST /api/uisprime/track


### Finding the right command

When you know what you want to do but not which command does it, ask the CLI directly:

```bash
expedia-cars-pp-cli which "<capability in your own words>"
```

`which` resolves a natural-language capability query to the best matching command from this CLI's curated feature index. Exit code `0` means at least one match; exit code `2` means no confident match — fall back to `--help` or use a narrower query.

## Auth Setup
Set your API key via environment variable:

```bash
export BROWSER_INTAKE_US5_DATADOGHQ_API_KEY="<your-key>"
```

Or persist it in `~/.config/expedia-cars-pp-cli/config.toml`.

Run `expedia-cars-pp-cli doctor` to verify setup.

## Agent Mode

Add `--agent` to any command. Expands to: `--json --compact --no-input --no-color --yes`.

- **Pipeable** — JSON on stdout, errors on stderr
- **Filterable** — `--select` keeps a subset of fields. Dotted paths descend into nested structures; arrays traverse element-wise. Critical for keeping context small on verbose APIs:

  ```bash
  expedia-cars-pp-cli .well-known --agent --select id,name,status
  ```
- **Previewable** — `--dry-run` shows the request without sending
- **Offline-friendly** — sync/search commands can use the local SQLite store when available
- **Non-interactive** — never prompts, every input is a flag
- **Explicit retries** — use `--idempotent` only when an already-existing create should count as success

### Response envelope

Commands that read from the local store or the API wrap output in a provenance envelope:

```json
{
  "meta": {"source": "live" | "local", "synced_at": "...", "reason": "..."},
  "results": <data>
}
```

Parse `.results` for data and `.meta.source` to know whether it's live or local. A human-readable `N results (live)` summary is printed to stderr only when stdout is a terminal — piped/agent consumers get pure JSON on stdout.

## Agent Feedback

When you (or the agent) notice something off about this CLI, record it:

```
expedia-cars-pp-cli feedback "the --since flag is inclusive but docs say exclusive"
expedia-cars-pp-cli feedback --stdin < notes.txt
expedia-cars-pp-cli feedback list --json --limit 10
```

Entries are stored locally at `~/.expedia-cars-pp-cli/feedback.jsonl`. They are never POSTed unless `EXPEDIA_CARS_FEEDBACK_ENDPOINT` is set AND either `--send` is passed or `EXPEDIA_CARS_FEEDBACK_AUTO_SEND=true`. Default behavior is local-only.

Write what *surprised* you, not a bug report. Short, specific, one line: that is the part that compounds.

## Output Delivery

Every command accepts `--deliver <sink>`. The output goes to the named sink in addition to (or instead of) stdout, so agents can route command results without hand-piping. Three sinks are supported:

| Sink | Effect |
|------|--------|
| `stdout` | Default; write to stdout only |
| `file:<path>` | Atomically write output to `<path>` (tmp + rename) |
| `webhook:<url>` | POST the output body to the URL (`application/json` or `application/x-ndjson` when `--compact`) |

Unknown schemes are refused with a structured error naming the supported set. Webhook failures return non-zero and log the URL + HTTP status on stderr.

## Named Profiles

A profile is a saved set of flag values, reused across invocations. Use it when a scheduled agent calls the same command every run with the same configuration - HeyGen's "Beacon" pattern.

```
expedia-cars-pp-cli profile save briefing --json
expedia-cars-pp-cli --profile briefing .well-known
expedia-cars-pp-cli profile list --json
expedia-cars-pp-cli profile show briefing
expedia-cars-pp-cli profile delete briefing --yes
```

Explicit flags always win over profile values; profile values win over defaults. `agent-context` lists all available profiles under `available_profiles` so introspecting agents discover them at runtime.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 2 | Usage error (wrong arguments) |
| 3 | Resource not found |
| 4 | Authentication required |
| 5 | API error (upstream issue) |
| 7 | Rate limited (wait and retry) |
| 10 | Config error |

## Argument Parsing

Parse `$ARGUMENTS`:

1. **Empty, `help`, or `--help`** → show `expedia-cars-pp-cli --help` output
2. **Starts with `install`** → ends with `mcp` → MCP installation; otherwise → see Prerequisites above
3. **Anything else** → Direct Use (execute as CLI command with `--agent`)

## MCP Server Installation

Install the MCP binary from this CLI's published public-library entry or pre-built release, then register it:

```bash
claude mcp add expedia-cars-pp-mcp -- expedia-cars-pp-mcp
```

Verify: `claude mcp list`

## Direct Use

1. Check if installed: `which expedia-cars-pp-cli`
   If not found, offer to install (see Prerequisites at the top of this skill).
2. Match the user query to the best command from the Unique Capabilities and Command Reference above.
3. Execute with the `--agent` flag:
   ```bash
   expedia-cars-pp-cli <command> [subcommand] [args] --agent
   ```
4. If ambiguous, drill into subcommand help: `expedia-cars-pp-cli <command> --help`.
