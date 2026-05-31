# Expedia Cars CLI

Discovered API spec for browser-intake-us5-datadoghq

Learn more at [Expedia Cars](https://www.expedia.com).

## Install

The recommended path installs both the `expedia-cars-pp-cli` binary and the `pp-expedia-cars` agent skill in one shot:

```bash
npx -y @mvanhorn/printing-press install expedia-cars
```

For CLI only (no skill):

```bash
npx -y @mvanhorn/printing-press install expedia-cars --cli-only
```


### Without Node

The generated install path is category-agnostic until this CLI is published. If `npx` is not available before publish, install Node or use the category-specific Go fallback from the public-library entry after publish.

### Pre-built binary

Download a pre-built binary for your platform from the [latest release](https://github.com/mvanhorn/printing-press-library/releases/tag/expedia-cars-current). On macOS, clear the Gatekeeper quarantine: `xattr -d com.apple.quarantine <binary>`. On Unix, mark it executable: `chmod +x <binary>`.

<!-- pp-hermes-install-anchor -->
## Install for Hermes

From the Hermes CLI:

```bash
hermes skills install mvanhorn/printing-press-library/cli-skills/pp-expedia-cars --force
```

Inside a Hermes chat session:

```bash
/skills install mvanhorn/printing-press-library/cli-skills/pp-expedia-cars --force
```

## Install for OpenClaw

Tell your OpenClaw agent (copy this):

```
Install the pp-expedia-cars skill from https://github.com/mvanhorn/printing-press-library/tree/main/cli-skills/pp-expedia-cars. The skill defines how its required CLI can be installed.
```

## Quick Start

### 1. Install

See [Install](#install) above.

### 2. Set Up Credentials

Get your API key from your API provider's developer portal. The key typically looks like a long alphanumeric string.

```bash
export BROWSER_INTAKE_US5_DATADOGHQ_API_KEY="<paste-your-key>"
```

You can also persist this in your config file at `~/.config/expedia-cars-pp-cli/config.toml`.

### 3. Verify Setup

```bash
expedia-cars-pp-cli doctor
```

This checks your configuration and credentials.

### 4. Try Your First Command

```bash
expedia-cars-pp-cli .well-known
```

## Usage

Run `expedia-cars-pp-cli --help` for the full command reference and flag list.

## Commands

### .well-known

Operations on web-identity

- **`expedia-cars-pp-cli .well-known list_web_identity`** - GET /.well-known/web-identity

### cl

Operations on 2x2.json

- **`expedia-cars-pp-cli cl create_2x2.json`** - POST /cl/2x2.json

### ds

Operations on pwa

- **`expedia-cars-pp-cli ds get_pwa`** - GET /ds/api/v1/toolkit/page.Car-Search/{id}/en_US/pwa

### egcs

Operations on collect

- **`expedia-cars-pp-cli egcs create_collect`** - POST /egcs/v2/collect

### getconfig

Operations on sodar

- **`expedia-cars-pp-cli getconfig list_sodar`** - GET /getconfig/sodar

### graphql

Operations on graphql

- **`expedia-cars-pp-cli graphql create_graphql`** - POST /graphql

### gsi

Operations on status

- **`expedia-cars-pp-cli gsi list_listaccounts`** - GET /gsi/fedcm/listaccounts
- **`expedia-cars-pp-cli gsi list_passive.json`** - GET /gsi/fedcm/config/passive.json
- **`expedia-cars-pp-cli gsi list_status`** - GET /gsi/status

### k4AZ50DsywoM

Operations on NpJ2or

- **`expedia-cars-pp-cli k4AZ50DsywoM create_NpJ2or`** - POST /k4AZ50DsywoM/SlBOW8/_KqZ0-/Sz3D2J7Quhfi/LkNVBTN0TwM/DUUTBl/NpJ2or

### maps

Operations on js

- **`expedia-cars-pp-cli maps list_gen_204`** - GET /maps/api/mapsjs/gen_204
- **`expedia-cars-pp-cli maps list_js`** - GET /maps/api/js

### pagead

Operations on conversion

- **`expedia-cars-pp-cli pagead get_conversion`** - GET /pagead/conversion/{id}/

### rum

Operations on rum

- **`expedia-cars-pp-cli rum create_rum`** - POST /api/v2/rum

### targeting-service

Operations on adinfo

- **`expedia-cars-pp-cli targeting-service list_adinfo`** - GET /targeting-service/v3/adinfo

### trvl-px

Operations on pix

- **`expedia-cars-pp-cli trvl-px create_pix`** - POST /trvl-px/v2/pix

### typeahead

Operations on Las Vegas, NV, United States of America (LAS-Harry Reid Intl.)

- **`expedia-cars-pp-cli typeahead list_Las Vegas, NV, United States of America (LAS_Harry Reid Intl.)`** - GET /api/v4/typeahead/Las Vegas, NV, United States of America (LAS-Harry Reid Intl.)

### uisprime

Operations on track

- **`expedia-cars-pp-cli uisprime create_track`** - POST /api/uisprime/track


## Output Formats

```bash
# Human-readable table (default in terminal, JSON when piped)
expedia-cars-pp-cli .well-known

# JSON for scripting and agents
expedia-cars-pp-cli .well-known --json

# Filter to specific fields
expedia-cars-pp-cli .well-known --json --select id,name,status

# Dry run — show the request without sending
expedia-cars-pp-cli .well-known --dry-run

# Agent mode — JSON + compact + no prompts in one flag
expedia-cars-pp-cli .well-known --agent
```

## Agent Usage

This CLI is designed for AI agent consumption:

- **Non-interactive** - never prompts, every input is a flag
- **Pipeable** - `--json` output to stdout, errors to stderr
- **Filterable** - `--select id,name` returns only fields you need
- **Previewable** - `--dry-run` shows the request without sending
- **Explicit retries** - add `--idempotent` to create retries when a no-op success is acceptable
- **Confirmable** - `--yes` for explicit confirmation of destructive actions
- **Piped input** - write commands can accept structured input when their help lists `--stdin`
- **Offline-friendly** - sync/search commands can use the local SQLite store when available
- **Agent-safe by default** - no colors or formatting unless `--human-friendly` is set

Exit codes: `0` success, `2` usage error, `3` not found, `4` auth error, `5` API error, `7` rate limited, `10` config error.

## Use with Claude Code

Install the focused skill — it auto-installs the CLI on first invocation:

```bash
npx skills add mvanhorn/printing-press-library/cli-skills/pp-expedia-cars -g
```

Then invoke `/pp-expedia-cars <query>` in Claude Code. The skill is the most efficient path — Claude Code drives the CLI directly without an MCP server in the middle.

<details>
<summary>Use as an MCP server in Claude Code (advanced)</summary>

If you'd rather register this CLI as an MCP server in Claude Code, install the MCP binary first:


Install the MCP binary from this CLI's published public-library entry or pre-built release.

Then register it:

```bash
claude mcp add expedia-cars expedia-cars-pp-mcp -e BROWSER_INTAKE_US5_DATADOGHQ_API_KEY=<your-key>
```

</details>

## Use with Claude Desktop

This CLI ships an [MCPB](https://github.com/modelcontextprotocol/mcpb) bundle — Claude Desktop's standard format for one-click MCP extension installs (no JSON config required).

To install:

1. Download the `.mcpb` for your platform from the [latest release](https://github.com/mvanhorn/printing-press-library/releases/tag/expedia-cars-current).
2. Double-click the `.mcpb` file. Claude Desktop opens and walks you through the install.
3. Fill in `BROWSER_INTAKE_US5_DATADOGHQ_API_KEY` when Claude Desktop prompts you.

Requires Claude Desktop 1.0.0 or later. Pre-built bundles ship for macOS Apple Silicon (`darwin-arm64`) and Windows (`amd64`, `arm64`); for other platforms, use the manual config below.

<details>
<summary>Manual JSON config (advanced)</summary>

If you can't use the MCPB bundle (older Claude Desktop, unsupported platform), install the MCP binary and configure it manually.


Install the MCP binary from this CLI's published public-library entry or pre-built release.

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "expedia-cars": {
      "command": "expedia-cars-pp-mcp",
      "env": {
        "BROWSER_INTAKE_US5_DATADOGHQ_API_KEY": "<your-key>"
      }
    }
  }
}
```

</details>

## Health Check

```bash
expedia-cars-pp-cli doctor
```

Verifies configuration, credentials, and connectivity to the API.

## Configuration

Config file: `~/.config/expedia-cars-pp-cli/config.toml`

Static request headers can be configured under `headers`; per-command header overrides take precedence.

Environment variables:

| Name | Kind | Required | Description |
| --- | --- | --- | --- |
| `BROWSER_INTAKE_US5_DATADOGHQ_API_KEY` | per_call | Yes | Set to your API credential. |

## Troubleshooting
**Authentication errors (exit code 4)**
- Run `expedia-cars-pp-cli doctor` to check credentials
- Verify the environment variable is set: `echo $BROWSER_INTAKE_US5_DATADOGHQ_API_KEY`
**Not found errors (exit code 3)**
- Check the resource ID is correct
- Run the `list` command to see available items

## HTTP Transport

This CLI uses Chrome-compatible HTTP transport over HTTP/3 for browser-facing endpoints. It does not require a resident browser process for normal API calls.

## Discovery Signals

This CLI was generated with browser-captured traffic analysis.
- Target observed: https://browser-intake-us5-datadoghq.com/api/v2/rum
- Capture coverage: 171 API entries from 337 total network entries
- Reachability: browser_clearance_http (82% confidence)
- Protocols: graphql (92% confidence), rest_json (75% confidence)
- Auth signals: cookie — cookies: CRQS, CRQSS, DUAID, EG_ANONTOKEN, HMS, IDE, KRTBCOOKIE_377, MC1, MR, MUID, NID, NavActions, PugT, TDCPM, TDID, __Host-3PLSID, __Secure-3PAPISID, __Secure-3PSID, __Secure-3PSIDCC, __Secure-3PSIDRTS, __Secure-3PSIDTS, _abck, _dd_s, _fbp, _gcl_au, _uetsid, _uetvid, ak_bmsc, barometric[cuid], bm_lso, bm_s, bm_so, bm_ss, bm_sv, bm_sz, c, cesc, currency, eg_adblock, eg_ppid, g_state, iEAPID, linfo, pageVisited, page_name, session_id, tpid, ttd_TDID, tuuid, tuuid_lu, xdid; api_key — query: dd-api-key, inAuthId, key
- Protection signals: akamai (75% confidence)
- Generation hints: browser_clearance_required, requires_browser_auth, requires_protected_client
- Candidate command ideas: create_2x2.json — Derived from observed POST /cl/2x2.json traffic.; create_NpJ2or — Derived from observed POST /k4AZ50DsywoM/SlBOW8/_KqZ0-/Sz3D2J7Quhfi/LkNVBTN0TwM/DUUTBl/NpJ2or traffic.; create_collect — Derived from observed POST /egcs/v2/collect traffic.; create_graphql — Derived from observed POST /graphql traffic.; create_pix — Derived from observed POST /trvl-px/v2/pix traffic.; create_rum — Derived from observed POST /api/v2/rum traffic.; create_track — Derived from observed POST /api/uisprime/track traffic.; get_conversion — Derived from observed GET /pagead/conversion/{id}/ traffic.

Warnings from discovery:
- empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.
- empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.
- empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.
- empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.
- empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.
- empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.
- empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.
- empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.
- empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.
- empty_payload: API-looking request returned an empty or null payload; schema confidence is weak.

---

Generated by [CLI Printing Press](https://github.com/mvanhorn/cli-printing-press)
