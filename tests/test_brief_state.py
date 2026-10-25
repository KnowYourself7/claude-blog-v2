"""Tests for the blog-brief state script (step progress and resume)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "blog-brief" / "scripts"))

import brief_state  # noqa: E402

SLUG = "linen-winter"
FOCUS = "can you wear linen in winter"


def _run(capsys, out_dir: Path, *args: str) -> tuple[int, dict]:
    code = brief_state.main([args[0], "--slug", SLUG, "--out", str(out_dir), *args[1:]])
    return code, json.loads(capsys.readouterr().out)


def _touch(out_dir: Path, name: str) -> None:
    (out_dir / f"{SLUG}-{name}").write_text("x", encoding="utf-8")


def _finish(capsys, out_dir: Path, step: int, *files: str, note: str | None = None) -> dict:
    for name in files:
        _touch(out_dir, name)
    code, _ = _run(capsys, out_dir, "set", "--step", str(step), "--status", "in_progress")
    assert code == 0
    extra = ["--note", note] if note else []
    code, result = _run(capsys, out_dir, "set", "--step", str(step), "--status", "done", *extra)
    assert code == 0, result
    return result


def _state(out_dir: Path) -> dict:
    return json.loads((out_dir / f"{SLUG}-state.json").read_text(encoding="utf-8"))


@pytest.fixture
def out_dir(tmp_path: Path, capsys) -> Path:
    code, _ = _run(capsys, tmp_path, "init", "--focus", FOCUS)
    assert code == 0
    return tmp_path


def test_checklist_gives_ten_steps_with_outputs():
    steps = brief_state.load_steps()
    assert sorted(steps) == list(range(1, 11))
    assert steps[3] == ["keyword-research.md", "demand-facets.md"]
    assert steps[4] == ["competitor-gaps.md", "competitor-[n].md"]
    assert steps[5] == [] and steps[9] == []


def test_init_creates_every_step_as_pending(tmp_path, capsys):
    code, result = _run(capsys, tmp_path, "init", "--focus", FOCUS)
    assert code == 0
    assert result["created"] is True and result["next_step"] == 1
    state = _state(tmp_path)
    assert state["focus_keyword"] == FOCUS
    assert {s["status"] for s in state["steps"].values()} == {"pending"}


def test_init_refuses_a_state_file_of_another_keyword(out_dir, capsys):
    code, result = _run(capsys, out_dir, "init", "--focus", "linen pants")
    assert code == 1
    assert FOCUS in result["error"]


def test_a_step_cannot_start_before_the_step_before_it_is_done(out_dir, capsys):
    code, result = _run(capsys, out_dir, "set", "--step", "2", "--status", "in_progress")
    assert code == 1
    assert "Step 1" in result["error"]


def test_done_needs_the_step_to_be_in_progress(out_dir, capsys):
    code, result = _run(capsys, out_dir, "set", "--step", "1", "--status", "done")
    assert code == 1
    assert "in_progress" in result["error"]


def test_done_names_the_missing_output_file(out_dir, capsys):
    _run(capsys, out_dir, "set", "--step", "1", "--status", "in_progress")
    code, result = _run(capsys, out_dir, "set", "--step", "1", "--status", "done")
    assert code == 1
    assert f"{SLUG}-task-brief.md" in result["error"]


def test_done_records_the_output_files(out_dir, capsys):
    _finish(capsys, out_dir, 1, "task-brief.md")
    step = _state(out_dir)["steps"]["1"]
    assert step["status"] == "done"
    assert step["outputs"] == [str(out_dir / f"{SLUG}-task-brief.md")]


def test_numbered_output_needs_one_numbered_file(out_dir, capsys):
    for number, name in enumerate(["task-brief.md", "search-intent.md"], start=1):
        _finish(capsys, out_dir, number, name)
    _finish(capsys, out_dir, 3, "keyword-research.md", "demand-facets.md")
    _touch(out_dir, "competitor-gaps.md")
    _run(capsys, out_dir, "set", "--step", "4", "--status", "in_progress")
    code, result = _run(capsys, out_dir, "set", "--step", "4", "--status", "done")
    assert code == 1
    assert "competitor-[n].md" in result["error"]
    _touch(out_dir, "competitor-1.md")
    _touch(out_dir, "competitor-2.md")
    code, result = _run(capsys, out_dir, "set", "--step", "4", "--status", "done")
    assert code == 0
    assert len(_state(out_dir)["steps"]["4"]["outputs"]) == 3


def test_stopped_needs_a_note_and_keeps_it(out_dir, capsys):
    _run(capsys, out_dir, "set", "--step", "1", "--status", "in_progress")
    code, _ = _run(capsys, out_dir, "set", "--step", "1", "--status", "stopped")
    assert code == 1
    code, _ = _run(capsys, out_dir, "set", "--step", "1", "--status", "stopped", "--note", "Which market?")
    assert code == 0
    code, result = _run(capsys, out_dir, "init", "--focus", FOCUS)
    assert result["next_step"] == 1
    assert result["stopped"] == [{"step": 1, "note": "Which market?"}]


def test_starting_a_done_step_again_resets_the_later_steps(out_dir, capsys):
    _finish(capsys, out_dir, 1, "task-brief.md")
    _finish(capsys, out_dir, 2, "search-intent.md")
    _finish(capsys, out_dir, 3, "keyword-research.md", "demand-facets.md")
    code, result = _run(capsys, out_dir, "set", "--step", "2", "--status", "in_progress")
    assert code == 0
    assert result["reset"] == [3]
    steps = _state(out_dir)["steps"]
    assert steps["2"]["status"] == "in_progress"
    assert steps["3"] == {"status": "pending", "outputs": [], "note": "", "updated": steps["3"]["updated"]}


def test_resume_redoes_from_the_first_step_with_a_missing_file(out_dir, capsys):
    _finish(capsys, out_dir, 1, "task-brief.md")
    _finish(capsys, out_dir, 2, "search-intent.md")
    _finish(capsys, out_dir, 3, "keyword-research.md", "demand-facets.md")
    _run(capsys, out_dir, "set", "--step", "4", "--status", "in_progress")
    (out_dir / f"{SLUG}-search-intent.md").unlink()
    code, result = _run(capsys, out_dir, "init", "--focus", FOCUS)
    assert code == 0
    assert result["created"] is False
    assert result["next_step"] == 2
    assert result["reset"] == [2, 3, 4]


def test_resume_keeps_a_step_without_files_only_if_it_has_a_note(out_dir, capsys):
    files = {
        1: ["task-brief.md"], 2: ["search-intent.md"],
        3: ["keyword-research.md", "demand-facets.md"],
        4: ["competitor-gaps.md", "competitor-1.md"], 6: ["evidence-plan.md"],
        7: ["information-gain.md"], 8: ["outline.md"],
    }
    for step in range(1, 10):
        note = "Template: how-to-guide. Reason: the ranking pages are step guides." if step == 5 else None
        _finish(capsys, out_dir, step, *files.get(step, []), note=note)
    code, result = _run(capsys, out_dir, "init", "--focus", FOCUS)
    assert result["next_step"] == 9
    assert result["reset"] == [9]
    assert _state(out_dir)["steps"]["5"]["status"] == "done"


def test_file_option_replaces_the_expected_outputs(out_dir, capsys, tmp_path):
    custom = tmp_path / "elsewhere.md"
    custom.write_text("x", encoding="utf-8")
    _run(capsys, out_dir, "set", "--step", "1", "--status", "in_progress")
    code, _ = _run(capsys, out_dir, "set", "--step", "1", "--status", "done", "--file", str(custom))
    assert code == 0
    assert _state(out_dir)["steps"]["1"]["outputs"] == [str(custom)]
