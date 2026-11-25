"""Folder organizer: sorts the files in a folder into sub-folders by type
(Images, Documents, Videos, Audio, Archives, Code, Other) and writes a log.

Usage:
    python organizer.py /path/to/folder --dry-run   # only show what would happen
    python organizer.py /path/to/folder             # actually move files
    python organizer.py /path/to/folder --undo      # move files back using the log
"""
import argparse
import json
import shutil
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "Videos": {".mp4", ".mkv", ".mov", ".avi"},
    "Audio": {".mp3", ".wav", ".m4a", ".ogg"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "Code": {".py", ".js", ".html", ".css", ".java", ".json", ".cpp"},
}
LOG_NAME = ".organizer_log.json"


def category_for(path):
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return "Other"


def unique_target(target):
    """Never overwrite: add (1), (2) ... if the name already exists."""
    if not target.exists():
        return target
    i = 1
    while True:
        cand = target.with_name(f"{target.stem} ({i}){target.suffix}")
        if not cand.exists():
            return cand
        i += 1


def organize(folder, dry_run=False):
    folder = Path(folder)
    moves = []
    for f in sorted(folder.iterdir()):
        if not f.is_file() or f.name == LOG_NAME:
            continue
        dest = unique_target(folder / category_for(f) / f.name)
        moves.append((f, dest))
        print(f"{'[dry-run] ' if dry_run else ''}{f.name}  ->  {dest.parent.name}/{dest.name}")
        if not dry_run:
            dest.parent.mkdir(exist_ok=True)
            shutil.move(str(f), str(dest))
    if moves and not dry_run:
        log = [{"from": str(a), "to": str(b)} for a, b in moves]
        (folder / LOG_NAME).write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"{len(moves)} file(s) {'would be moved' if dry_run else 'moved'}.")
    return moves


def undo(folder):
    log_path = Path(folder) / LOG_NAME
    if not log_path.exists():
        print("No log found, nothing to undo.")
        return 0
    entries = json.loads(log_path.read_text(encoding="utf-8"))
    for e in reversed(entries):
        src, dst = Path(e["to"]), Path(e["from"])
        if src.exists():
            shutil.move(str(src), str(unique_target(dst)))
            print(f"restored {dst.name}")
    log_path.unlink()
    for d in Path(folder).iterdir():
        if d.is_dir() and d.name in CATEGORIES.keys() | {"Other"} and not any(d.iterdir()):
            d.rmdir()
    return len(entries)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--undo", action="store_true")
    a = ap.parse_args()
    undo(a.folder) if a.undo else organize(a.folder, a.dry_run)
