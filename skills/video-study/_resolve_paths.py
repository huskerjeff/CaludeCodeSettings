"""Path resolution for the video-study skill — cross-machine.

Usage:
  python _resolve_paths.py learning      # prints Learning base folder path
  python _resolve_paths.py latest-docx   # prints newest .docx across known playwright-cli download dirs

Override via env vars: LEARNING_DIR, PLAYWRIGHT_DOWNLOADS_DIR.

Learning-folder selection order (first wins):
  1. $env:LEARNING_DIR (explicit override)
  2. An existing ClaudeCode_Life\\Learning under any known cloud-sync folder in ~
     (iCloud Drive, OneDrive variants, Dropbox, Google Drive)
  3. ClaudeCode_Life\\Learning placed under the first populated cloud folder,
     prioritizing iCloud Drive, then personal OneDrive, then corporate OneDrive
  4. ~\\ClaudeCode_Life\\Learning (non-cloud fallback)
"""
import glob
import os
import sys

HOME = os.path.expanduser("~")

# Preferred cloud-sync roots in priority order. First match that exists and is
# non-empty wins. Names are relative to HOME; comparisons are case-insensitive
# on Windows via os.path.isdir.
CLOUD_ROOT_NAMES = [
    "iCloudDrive",
    "iCloud Drive",
    "OneDrive",
    "OneDrive - CDW",
    "Dropbox",
    "Google Drive",
]


def _populated_cloud_roots():
    """Yield HOME-relative cloud dirs that exist AND contain files."""
    # Also discover any other OneDrive-* variants we didn't enumerate explicitly.
    try:
        extras = [
            n for n in os.listdir(HOME)
            if n.lower().startswith("onedrive") and n not in CLOUD_ROOT_NAMES
        ]
    except OSError:
        extras = []
    for name in CLOUD_ROOT_NAMES + extras:
        path = os.path.join(HOME, name)
        if not os.path.isdir(path):
            continue
        try:
            if os.listdir(path):
                yield path
        except OSError:
            continue


def resolve_learning():
    override = os.environ.get("LEARNING_DIR")
    if override:
        return override

    roots = list(_populated_cloud_roots())

    # Prefer an existing ClaudeCode_Life\Learning under any cloud root.
    for root in roots:
        candidate = os.path.join(root, "ClaudeCode_Life", "Learning")
        if os.path.isdir(candidate):
            return candidate
    local = os.path.join(HOME, "ClaudeCode_Life", "Learning")
    if os.path.isdir(local):
        return local

    # Otherwise place ClaudeCode_Life\Learning in the top-priority cloud root.
    if roots:
        return os.path.join(roots[0], "ClaudeCode_Life", "Learning")

    return local


def resolve_latest_docx():
    override = os.environ.get("PLAYWRIGHT_DOWNLOADS_DIR")
    candidates = [override] if override else []
    # playwright-cli writes to <cwd>/.playwright-cli, so include common launch dirs.
    candidates.append(os.path.join(HOME, ".playwright-cli"))
    for root in _populated_cloud_roots():
        candidates.append(os.path.join(root, ".playwright-cli"))
        candidates.append(os.path.join(root, "ClaudeCode_Life", ".playwright-cli"))
        candidates.append(os.path.join(root, "Claude_Work", ".playwright-cli"))

    seen = set()
    files = []
    for d in candidates:
        if not d or d in seen or not os.path.isdir(d):
            continue
        seen.add(d)
        files.extend(glob.glob(os.path.join(d, "*.docx")))
    if not files:
        return ""
    return max(files, key=os.path.getctime)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "learning"
    if cmd == "learning":
        print(resolve_learning())
    elif cmd == "latest-docx":
        print(resolve_latest_docx())
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
