import tempfile
from pathlib import Path
import organizer


def make(tmp, names):
    for n in names:
        (Path(tmp) / n).write_text("x")


def test_sorts_and_undo():
    with tempfile.TemporaryDirectory() as tmp:
        make(tmp, ["a.jpg", "b.pdf", "c.mp4", "d.xyz", "e.py"])
        organizer.organize(tmp)
        assert (Path(tmp) / "Images" / "a.jpg").exists()
        assert (Path(tmp) / "Documents" / "b.pdf").exists()
        assert (Path(tmp) / "Other" / "d.xyz").exists()
        organizer.undo(tmp)
        assert (Path(tmp) / "a.jpg").exists() and not (Path(tmp) / "Images").exists()


def test_dry_run_moves_nothing():
    with tempfile.TemporaryDirectory() as tmp:
        make(tmp, ["a.jpg"])
        organizer.organize(tmp, dry_run=True)
        assert (Path(tmp) / "a.jpg").exists()


def test_no_overwrite():
    with tempfile.TemporaryDirectory() as tmp:
        make(tmp, ["a.jpg"])
        (Path(tmp) / "Images").mkdir()
        (Path(tmp) / "Images" / "a.jpg").write_text("old")
        organizer.organize(tmp)
        assert (Path(tmp) / "Images" / "a (1).jpg").exists()
        assert (Path(tmp) / "Images" / "a.jpg").read_text() == "old"
