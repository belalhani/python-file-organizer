# Folder Organizer (Python automation)

Sorts the files in a messy folder (like Downloads) into `Images`, `Documents`, `Videos`,
`Audio`, `Archives`, `Code` and `Other`.

```bash
python organizer.py ~/Downloads --dry-run   # preview only, nothing moves
python organizer.py ~/Downloads             # sort the files
python organizer.py ~/Downloads --undo      # put everything back
```

- Never overwrites: a name clash becomes `name (1).ext`
- Writes a log so the whole run can be undone
- No dependencies, tests included: `python -c "import test_organizer as t; t.test_sorts_and_undo(); t.test_dry_run_moves_nothing(); t.test_no_overwrite()"` (or `pytest`)

Built by Belal Hani.
