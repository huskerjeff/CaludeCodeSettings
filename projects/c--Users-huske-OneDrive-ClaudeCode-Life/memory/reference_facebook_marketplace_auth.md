---
name: reference-facebook-marketplace-auth
description: How to authenticate and search Facebook Marketplace CLI on Windows — what fails and what actually works
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9ac5c2b8-d5b9-4515-8fc8-b1dd0933acb6
---

Full working process is documented in `C:\Users\huske\OneDrive\ClaudeCode_Life\FBMarketPlace.auth`. Read that file first every time.

## What DOES NOT work on Windows (don't retry these)

- **`pycookiecheat`** — only works on macOS/Linux. Throws `OSError: This script only works on MacOS or Linux.` Always fails.
- **`cookie-scoop-cli` via `cargo install`** — requires MSVC build tools (`link.exe`). No pre-built Windows binary exists. Don't attempt.
- **Reading Chrome cookie DB directly with Python** — Chrome locks the SQLite file while running. Even when closed, Chrome 127+ uses app-bound encryption that DPAPI alone can't decrypt — values come out as garbage.
- **Writing `cookies = "..."` to `config.toml`** — the CLI ignores this key. It only reads from `FACEBOOK_MARKET_COOKIES` env var.
- **`auth login --chrome`** — calls pycookiecheat internally, always fails on Windows.
- **`auth refresh`** — also calls pycookiecheat internally, always fails on Windows.
- **`marketplace_search` (underscore)** — wrong command name. Use `marketplace-search` (hyphen).

## What WORKS

### Step 1: Get cookies via playwright-cli
Make sure the playwright browser is open and logged into Facebook:
```bash
playwright-cli open --browser=chrome --persistent --headed https://www.facebook.com
playwright-cli cookie-list
```
Pull the `.facebook.com` cookies from the output: `datr`, `sb`, `xs`, `c_user`, `fr`, `ps_l`, `ps_n`, `wd`, `dpr`, `presence`.

### Step 2: Set env var and search with --agent
```powershell
$env:FACEBOOK_MARKET_COOKIES = "datr=...; sb=...; xs=...; c_user=...; ..."
facebook-marketplace-pp-cli marketplace-search --variables "<full relay JSON>" --agent
```

The `--agent` flag bypasses the session proof check. Even if `doctor` says "Auth: not configured", searches still work when the API is reachable.

### Step 3: Full Relay variables template for search
Use the CLI's built-in default as the base (from `marketplace-search --help`), swap:
- `"query": "ipad"` → your search term
- `"filter_location_latitude": 41.2565` → Omaha NE lat
- `"filter_location_longitude": -95.9345` → Omaha NE lon
- `"filter_radius_km": 65` → radius

The `__relay_internal__pv__GHLShouldChangeMarketplaceSponsoredDataFieldNamerelayprovider` field must be present or you get `noncoercible_variable_value` error.

## Omaha NE coordinates
- Latitude: 41.2565
- Longitude: -95.9345
