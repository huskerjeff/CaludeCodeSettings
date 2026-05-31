#!/bin/sh
input=$(cat)
cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // "unknown"')
model=$(echo "$input" | jq -r '.model.display_name // "unknown"')
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')

# Shorten home directory to ~
home="$HOME"
short_cwd=$(echo "$cwd" | sed "s|^$home|~|")

if [ -n "$used" ]; then
    printf "%s | %s | ctx: %.0f%% used" "$short_cwd" "$model" "$used"
else
    printf "%s | %s" "$short_cwd" "$model"
fi
