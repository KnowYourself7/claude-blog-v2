"""Checks that the blog-brief workflow checklist matches the step files."""

from __future__ import annotations

import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "blog-brief"
STEP_LINE = re.compile(r"^- \[ \] Step (\d+): ([^.]+)\. (.+)$")
BRIEF_FILE = re.compile(r"briefs/\[slug\]-([\w\[\]-]+\.md)")


def _skill_text() -> str:
    return (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")


def _checklist() -> dict[int, dict]:
    """Parse the Brief Progress block into {step number: fields}."""
    block = re.search(r"```\nBrief Progress:\n(.*?)```", _skill_text(), re.S)
    assert block, "SKILL.md has no Brief Progress checklist"
    steps: dict[int, dict] = {}
    for line in block.group(1).splitlines():
        match = STEP_LINE.match(line)
        assert match, f"checklist line does not match the format: {line}"
        step_number, step_name, rest = match.groups()
        sentences = rest.split(". ")
        read_target = sentences[0].removeprefix("Read ")
        uses_sentence = next((s for s in sentences if s.startswith("Uses ")), "")
        output_sentence = next(s for s in sentences if s.startswith("Output: "))
        steps[int(step_number)] = {
            "name": step_name,
            "step_file": read_target if read_target.endswith(".md") else None,
            "uses": {int(n) for n in re.findall(r"Step (\d+)", uses_sentence)},
            "outputs": set(re.findall(r"[\w\[\]-]+\.md", output_sentence)),
        }
    return steps


def _section(step_file: str, heading: str) -> str:
    text = (SKILL_DIR / "references" / step_file).read_text(encoding="utf-8")
    match = re.search(rf"^#### {heading}\n(.*?)(?=^#### |\Z)", text, re.S | re.M)
    assert match, f"{step_file} has no {heading} section"
    return match.group(1)


CHECKLIST = _checklist() if "Brief Progress:" in _skill_text() else {}
STEPS_WITH_FILES = sorted(n for n, s in CHECKLIST.items() if s["step_file"])


def test_checklist_lists_every_step_in_order() -> None:
    assert sorted(CHECKLIST) == list(range(1, 12))


@pytest.mark.parametrize("step_number", STEPS_WITH_FILES)
def test_step_file_heading_matches_checklist(step_number: int) -> None:
    step = CHECKLIST[step_number]
    first_line = (SKILL_DIR / "references" / step["step_file"]).read_text(
        encoding="utf-8"
    ).splitlines()[0]
    assert first_line == f"### Step {step_number}: {step['name']}"


@pytest.mark.parametrize("step_number", STEPS_WITH_FILES)
def test_checklist_outputs_are_in_step_file_outputs(step_number: int) -> None:
    step = CHECKLIST[step_number]
    outputs_section = _section(step["step_file"], "Outputs")
    assert step["outputs"] <= set(BRIEF_FILE.findall(outputs_section))


@pytest.mark.parametrize("step_number", STEPS_WITH_FILES)
def test_checklist_uses_match_step_file_inputs(step_number: int) -> None:
    step = CHECKLIST[step_number]
    producer_of = {
        output: number
        for number, other in CHECKLIST.items()
        for output in other["outputs"]
    }
    inputs_section = _section(step["step_file"], "Inputs")
    needed = {producer_of[name] for name in BRIEF_FILE.findall(inputs_section)}
    needed |= {int(n) for n in re.findall(r"Step (\d+)", inputs_section)}
    assert step["uses"] == needed


def test_save_step_output_is_in_its_section() -> None:
    save_section = _skill_text().split("### Step 10: Save the Brief", 1)[1]
    for output in CHECKLIST[10]["outputs"]:
        assert f"briefs/[slug]-{output}" in save_section
