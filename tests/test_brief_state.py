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


def test_checklist_gives_eleven_steps_with_outputs():
    steps = brief_state.load_steps()
    assert sorted(steps) == list(range(1, 12))
    assert steps[3] == ["keyword-research.md", "demand-facets.md"]
    assert steps[4] == ["competitor-gaps.md", "competitor-[n].md"]
    assert steps[5] == [] and steps[9] == [] and steps[11] == []


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


# The A-to-B gate (Step 11). The files below are a small brief that passes
# every check. Each fail test breaks one thing.

OUTLINE_V2 = """### Introduction
- Hook: A linen shirt looks like a summer shirt.
- Promise: The reader can pick a linen piece for a cool day.

### H2: Can You Wear Linen in Winter?
- Facets: F1
- Answer: Yes, under a warm layer.
- Evidence: 1, 3 estimated. Narrower claim: -
- Gains: I1
- Components: none

### H2: How Warm Is Linen?
- Facets: F2
- Answer: Linen alone is not warm.
- Evidence: -. Narrower claim: The post gives only the indoor range.
- Gains: -
- Components: none

### FAQ
1. Is linen fine at 70 degrees: yes, indoors. Evidence: 1

### Conclusion (100-150 words)
- Key takeaways (bulleted)
- Call to action: shop the linen shirts

### Still Open
none
"""

BRIEF_FILES = {
    "task-brief.md": """# Task Brief: x

## Page

| Item | Value |
|------|-------|
| Page this post supports | https://example.com/linen-shirts |
| Reader next step | shop the linen shirts |
""",
    "search-intent.md": """# Search Intent: x

## Decision

- Decision: continue
- Page type that fits the SERP: blog
- User choice: not needed
""",
    "keyword-research.md": "# Keyword Research: x\n",
    "demand-facets.md": """# Demand Facets: x

## Kept Facets

| ID | Reader question | Reason kept |
|----|-----------------|-------------|
| F1 | Can you wear linen in winter? | The core question. |
| F2 | Is linen warm? | A PAA question. |

## Other Facets

| ID | Reader question | Reason not kept |
|----|-----------------|-----------------|
| F3 | Can women wear linen dresses in winter? | outside business |
""",
    "competitor-gaps.md": """# Competitor Gaps: x

## Data Scope

| Item | Value |
|------|-------|
| Fetch | Firecrawl `firecrawl_scrape`, markdown, 3 fetched, 0 failed, 3 credits |
""",
    "competitor-1.md": "# Competitor 1\n",
    "evidence-plan.md": """# Evidence Plan: x

## Questions

| ID | Facet | Question | Source type | Use | Weak |
|----|-------|----------|-------------|-----|------|
| E1 | F1 | What is the clo value of a linen shirt? | paper | a range | no |
| E2 | F2 | How warm is linen at 10 C? | paper | a band | no |

## Search Plan

| Facet | Questions | Planned searches | Planned fetches | Actual searches | Actual fetches | Actual credits |
|-------|-----------|------------------|-----------------|-----------------|----------------|----------------|
| F1 | E1, E2 | 1 | 2 | 1 | 3 | 7 |
| Total | - | 1 | 2 | 1 | 3 | 7 |

## Sources

| # | Question | Source | Finding | Status | Chart |
|---|----------|--------|---------|--------|-------|
| 1 | E1 | ASHRAE 55 | 0.5 clo | adopted | no |
| 2 | E2 | A forum post | - | rejected | - |
| 3 | E1 | A lab test | 0.6 clo | adopted | yes |
""",
    "information-gain.md": """# Information Gain: x

## Gains

| ID | The ranking pages give | Gain | Name | Use | Evidence requirement |
|----|------------------------|------|------|-----|----------------------|
| I1 | A yes answer | a table | Piece table | Rows of pieces, so the reader can pick one. | 1, 3 estimated |

## First-Party Evidence

none supplied.
""",
    "outline.md": """# Outline: x

## Outline V1

Title: Can You Wear Linen in Winter?

| # | H2 | Facets | Gains | Core answer |
|---|----|--------|-------|-------------|
| 1 | Can You Wear Linen in Winter? | F1 | I1 | Yes, under a layer. |
| 2 | How Warm Is Linen? | F2 | - | Not warm alone. |

- FAQ: Is linen fine at 70 degrees?
- Decision framework: H2 1
- Calculator: none. No adopted source gives a formula.

## Self-Review

| Check | Finding | Changes |
|-------|---------|---------|
| Intent | The order fits. | none |

## Outline V2

Title: Can You Wear Linen in Winter?

""" + OUTLINE_V2,
    "brief.md": """# Content Brief: Can You Wear Linen in Winter?

## Template
**Recommended**: how-to-guide: the ranking pages are guides.

## Content Outline
**Outline file**: `briefs/linen-winter-outline.md`

""" + OUTLINE_V2 + """
## Statistics to Include

| # | Statistic | Source | Year |
|---|-----------|--------|------|
| 1 | 0.5 clo | ASHRAE 55 | 2023 |
""",
}

STEP_FILES = {
    1: ["task-brief.md"], 2: ["search-intent.md"],
    3: ["keyword-research.md", "demand-facets.md"],
    4: ["competitor-gaps.md", "competitor-1.md"], 6: ["evidence-plan.md"],
    7: ["information-gain.md"], 8: ["outline.md"], 10: ["brief.md"],
}


def _write(out_dir: Path, name: str, text: str) -> None:
    (out_dir / f"{SLUG}-{name}").write_text(text, encoding="utf-8")


def _edit(out_dir: Path, name: str, old: str, new: str) -> None:
    path = out_dir / f"{SLUG}-{name}"
    text = path.read_text(encoding="utf-8")
    assert old in text, f"{old!r} is not in {name}"
    path.write_text(text.replace(old, new), encoding="utf-8")


def _start_gate(capsys, out_dir: Path) -> None:
    """Write the brief files, finish Step 1 to Step 10, and start Step 11."""
    for name, text in BRIEF_FILES.items():
        _write(out_dir, name, text)
    for step in range(1, 11):
        note = "Template: how-to-guide. Reason: the ranking pages are guides." if step == 5 else None
        _run(capsys, out_dir, "set", "--step", str(step), "--status", "in_progress")
        extra = ["--note", note] if note else []
        code, result = _run(capsys, out_dir, "set", "--step", str(step), "--status", "done", *extra)
        assert code == 0, result
    code, _ = _run(capsys, out_dir, "set", "--step", "11", "--status", "in_progress")
    assert code == 0


def _gate(capsys, out_dir: Path) -> dict:
    code, result = _run(capsys, out_dir, "gate")
    assert code == 0, result
    return result


def _items(result: dict, outcome: str) -> list[dict]:
    return [item for item in result["gate"]["items"] if item["result"] == outcome]


def test_gate_needs_step_11_in_progress(out_dir, capsys):
    code, result = _run(capsys, out_dir, "gate")
    assert code == 1
    assert "Step 11" in result["error"]


def test_gate_passes_a_clean_brief_and_finishes_step_11(out_dir, capsys):
    _start_gate(capsys, out_dir)
    result = _gate(capsys, out_dir)
    gate = result["gate"]
    assert gate["result"] == "pass", gate["items"]
    assert gate["attempt"] == 0 and gate["redo_from"] is None
    assert gate["credits"] == {"step_4": 3, "step_6": 7}
    assert {item["check"] for item in _items(result, "not built")} == {
        "Competitive opportunity", "Semantic baseline",
    }
    state = _state(out_dir)
    assert state["gate"] == gate
    assert state["steps"]["11"]["status"] == "done"
    assert state["steps"]["11"]["note"] == "Gate: pass"
    assert result["next_step"] is None


def test_gate_warns_and_lists_the_open_items(out_dir, capsys):
    _start_gate(capsys, out_dir)
    _edit(out_dir, "task-brief.md", "https://example.com/linen-shirts", "missing")
    _edit(out_dir, "evidence-plan.md", "| a band | no |", "| a band | yes |")
    for name in ("outline.md", "brief.md"):
        _edit(out_dir, name, "### Still Open\nnone", "### Still Open\n- H2 2: no outdoor range.")
    result = _gate(capsys, out_dir)
    assert result["gate"]["result"] == "warn", result["gate"]["items"]
    details = " ".join(item["detail"] for item in _items(result, "warn"))
    assert "E2" in details and "H2 2: no outdoor range." in details
    assert {item["check"] for item in _items(result, "warn")} == {
        "Page this post supports", "Weak questions", "Still Open",
    }
    assert _state(out_dir)["steps"]["11"]["status"] == "done"


def _stop_at_step_2(out_dir: Path) -> None:
    _edit(out_dir, "search-intent.md", "- Decision: continue", "- Decision: stop")


def _drop_facet(out_dir: Path) -> None:
    _edit(out_dir, "outline.md", "- Facets: F2", "- Facets: F1")


def _add_other_facet(out_dir: Path) -> None:
    _edit(out_dir, "outline.md", "- Facets: F2", "- Facets: F2, F3")


def _drop_gain(out_dir: Path) -> None:
    _edit(out_dir, "outline.md", "- Gains: I1", "- Gains: -")


def _empty_calculator(out_dir: Path) -> None:
    _edit(out_dir, "outline.md", "- Calculator: none. No adopted source gives a formula.",
          "- Calculator: [main, section, or none]")


def _change_brief(out_dir: Path) -> None:
    _edit(out_dir, "brief.md", "- Answer: Linen alone is not warm.", "- Answer: Linen is warm.")


def _cite_rejected(out_dir: Path) -> None:
    _edit(out_dir, "outline.md", "- Evidence: 1, 3 estimated.", "- Evidence: 1, 2.")


def _faq_cites_unknown(out_dir: Path) -> None:
    _edit(out_dir, "outline.md", "indoors. Evidence: 1", "indoors. Evidence: 9")


def _no_evidence_and_no_claim(out_dir: Path) -> None:
    _edit(out_dir, "outline.md", "Narrower claim: The post gives only the indoor range.", "Narrower claim: -")


def _delete_search_intent(out_dir: Path) -> None:
    (out_dir / f"{SLUG}-search-intent.md").unlink()


def _no_outline_v2(out_dir: Path) -> None:
    _edit(out_dir, "outline.md", "## Outline V2", "## Outline Two")


@pytest.mark.parametrize(
    ("breaks", "check", "redo"),
    [
        (_stop_at_step_2, "SERP decision", 2),
        (_drop_facet, "Kept facets in Outline V2", 8),
        (_add_other_facet, "Kept facets in Outline V2", 8),
        (_drop_gain, "Gains in Outline V2", 8),
        (_empty_calculator, "Calculator", 8),
        (_change_brief, "Content Outline", 9),
        (_cite_rejected, "Adopted sources", 8),
        (_faq_cites_unknown, "Adopted sources", 8),
        (_no_evidence_and_no_claim, "Evidence or narrower claim", 8),
        (_delete_search_intent, "Output files", 2),
        (_no_outline_v2, "Kept facets in Outline V2", 8),
    ],
)
def test_gate_fails_and_names_the_step_to_redo(out_dir, capsys, breaks, check, redo):
    _start_gate(capsys, out_dir)
    breaks(out_dir)
    result = _gate(capsys, out_dir)
    gate = result["gate"]
    assert gate["result"] == "fail"
    assert gate["attempt"] == 1
    failed = {item["check"]: item["redo"] for item in _items(result, "fail")}
    assert failed.get(check) == redo, gate["items"]
    assert gate["redo_from"] == min(failed.values())
    assert _state(out_dir)["steps"]["11"]["status"] == "in_progress"


def test_a_second_fail_in_a_row_stops_step_11(out_dir, capsys):
    _start_gate(capsys, out_dir)
    _cite_rejected(out_dir)
    _gate(capsys, out_dir)
    result = _gate(capsys, out_dir)
    assert result["gate"]["attempt"] == 2
    step = _state(out_dir)["steps"]["11"]
    assert step["status"] == "stopped"
    assert "Adopted sources" in step["note"]
    assert result["stopped"] == [{"step": 11, "note": step["note"]}]


def test_redo_after_a_fail_resets_step_11_and_the_next_gate_can_pass(out_dir, capsys):
    _start_gate(capsys, out_dir)
    _cite_rejected(out_dir)
    _gate(capsys, out_dir)
    code, result = _run(capsys, out_dir, "set", "--step", "8", "--status", "in_progress")
    assert result["reset"] == [9, 10, 11]
    assert _state(out_dir)["gate"]["result"] == "fail"
    _write(out_dir, "outline.md", BRIEF_FILES["outline.md"])
    for step in (8, 9, 10, 11):
        if step != 8:
            _run(capsys, out_dir, "set", "--step", str(step), "--status", "in_progress")
        if step != 11:
            code, _ = _run(capsys, out_dir, "set", "--step", str(step), "--status", "done")
            assert code == 0
    result = _gate(capsys, out_dir)
    assert result["gate"]["result"] == "pass"
    assert result["gate"]["attempt"] == 0


def test_the_user_can_accept_a_stopped_gate(out_dir, capsys):
    _start_gate(capsys, out_dir)
    _cite_rejected(out_dir)
    _gate(capsys, out_dir)
    _gate(capsys, out_dir)
    code, _ = _run(capsys, out_dir, "set", "--step", "11", "--status", "in_progress",
                   "--note", "Write anyway. Source 2 stays.")
    assert code == 0
    code, result = _run(capsys, out_dir, "set", "--step", "11", "--status", "done")
    assert code == 0
    assert _state(out_dir)["steps"]["11"]["note"] == "Write anyway. Source 2 stays."
