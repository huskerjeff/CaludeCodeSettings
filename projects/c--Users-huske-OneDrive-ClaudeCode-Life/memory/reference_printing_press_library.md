---
name: reference-printing-press-library
description: The Printing Press public library at printingpress.dev and its GitHub repo list pre-built CLIs — check there before generating a new one
metadata: 
  node_type: memory
  type: reference
  originSessionId: 9ac5c2b8-d5b9-4515-8fc8-b1dd0933acb6
---

The Printing Press public library lists 180+ pre-built agent-native CLIs that can be installed instead of generating from scratch.

- **Website:** https://printingpress.dev/
- **GitHub library repo:** https://github.com/mvanhorn/printing-press-library
- **Registry JSON:** https://raw.githubusercontent.com/mvanhorn/printing-press-library/main/registry.json

**IMPORTANT — fetch method matters:** The raw `registry.json` gets truncated by WebFetch and will miss entries. Always use the **GitHub page** (`https://github.com/mvanhorn/printing-press-library`) to get the full list — it returns all 180+ entries reliably. Never tell the user a CLI doesn't exist based on a truncated registry fetch.

Before running `/printing-press <api>`, check the registry for an existing CLI. Install with:

```bash
npx -y @mvanhorn/printing-press-library install <cli-name>
```

Example: `espn-pp-cli` was already in the library and installed — no generation needed. `facebook-marketplace` exists even though a truncated registry fetch missed it.
