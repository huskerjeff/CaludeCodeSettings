# Claude Code Settings

Personal Claude Code configuration synced across machines.

## Contents

- `commands/` — custom slash commands
- `skills/` — custom skills
- `settings.json` — Claude Code settings
- `CLAUDE.md` — persistent instructions for Claude
- `todos/` — saved todos

## Setup on a new machine

```bash
git clone https://github.com/huskerjeff/CaludeCodeSettings.git ~/.claude
```

## Keeping in sync

```bash
# Pull latest changes
cd ~/.claude && git pull

# Push new changes
cd ~/.claude && git add . && git commit -m "update" && git push
```
