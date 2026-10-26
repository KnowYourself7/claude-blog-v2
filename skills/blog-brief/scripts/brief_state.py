#!/usr/bin/env python3
"""Step progress of one blog-brief run, kept in briefs/[slug]-state.json.

The steps and their output files come from the Brief Progress checklist in
../SKILL.md. The script does not keep its own copy of the steps.

Each step has one status:
    pending      Not started.
    in_progress  Started. On resume, the step is done again from the start.
    done         Every item of its Check is true, and its output files exist.
    stopped      The step asked the user a question. The note has the question.

Subcommands:
    init  Make the state file, or read it to resume a run. On resume, a done
          step with a missing output file goes back to pending. So does a done
          step with no output file and no note. An in_progress step goes back
          to pending. Every step after the first step that is not done goes
          back to pending.
    set   Change the status of one step. A step can start only after every
          step before it is done. Starting a step again sets every later step
          back to pending. Done needs the output files that the checklist
          lists, or the files given with --file.
    gate  The A-to-B gate (Step 11). Step 11 must be in_progress. Check
          the files of Step 1 to Step 10 against each other, and write the
          result into the "gate" section of the state file. With no fail,
          Step 11 becomes done. With a fail, redo_from names the earliest
          step to do again. A second fail in a row stops Step 11. To accept
          the brief after a gate, set Step 11 to done with --note and the
          answer of the user. That starts a new count of fails.

Every subcommand prints a JSON summary on stdout. Errors are JSON
{"error": ...} on stdout with exit code 1.

Usage:
    python3 brief_state.py init --slug linen-winter --focus "can you wear linen in winter" --out briefs
    python3 brief_state.py set --slug linen-winter --step 2 --status in_progress --out briefs
    python3 brief_state.py set --slug linen-winter --step 2 --status stopped --note "Blog share is 20%. Write anyway, try another keyword, or end?" --out briefs
    python3 brief_state.py set --slug linen-winter --step 5 --status done --note "Template: how-to-guide. Reason: ..." --out briefs
    python3 brief_state.py gate --slug linen-winter --out briefs
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from itertools import zip_longest
from pathlib import Path

SKILL_FILE = Path(__file__).resolve().parent.parent / "SKILL.md"
SCHEMA_VERSION = 1
STEP_LINE = re.compile(r"^- \[ \] Step (\d+): .*?Output: (.*)$")
OUTPUT_NAME = re.compile(r"[\w\[\]-]+\.md")
STATUSES = ("in_progress", "done", "stopped")


class StateError(Exception):
    """A request that the state file cannot accept."""


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_steps(skill_file: Path = SKILL_FILE) -> dict[int, list[str]]:
    """Read {step number: output file names} from the Brief Progress checklist."""
    text = skill_file.read_text(encoding="utf-8")
    block = re.search(r"```\nBrief Progress:\n(.*?)```", text, re.S)
    if not block:
        raise StateError(f"{skill_file} has no Brief Progress checklist")
    steps: dict[int, list[str]] = {}
    for line in block.group(1).splitlines():
        match = STEP_LINE.match(line)
        if not match:
            raise StateError(f"checklist line has no step number or Output: {line}")
        output_sentence = match.group(2).split(". ")[0]
        steps[int(match.group(1))] = OUTPUT_NAME.findall(output_sentence)
    return steps


def pending_step() -> dict:
    return {"status": "pending", "outputs": [], "note": "", "updated": now()}


def state_path(out_dir: Path, slug: str) -> Path:
    return out_dir / f"{slug}-state.json"


def read_state(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_state(path: Path, state: dict) -> None:
    """Write through a temporary file, so an interruption never leaves half a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(handle, "w", encoding="utf-8") as stream:
        json.dump(state, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    os.replace(temporary, path)


def find_outputs(out_dir: Path, slug: str, names: list[str]) -> tuple[list[str], list[str]]:
    """Return (found paths, missing names). `[n]` in a name matches one or more digits."""
    found: list[str] = []
    missing: list[str] = []
    for name in names:
        if "[n]" not in name:
            path = out_dir / f"{slug}-{name}"
            if path.is_file():
                found.append(str(path))
            else:
                missing.append(path.name)
            continue
        pattern = re.compile(re.escape(f"{slug}-{name}").replace(r"\[n\]", r"\d+") + "$")
        matches = sorted(str(p) for p in out_dir.iterdir() if p.is_file() and pattern.match(p.name))
        if matches:
            found.extend(matches)
        else:
            missing.append(f"{slug}-{name}")
    return found, missing


def reset_after(state: dict, step: int) -> list[int]:
    """Set every step after `step` that is not pending back to pending."""
    reset = []
    for key in sorted(state["steps"], key=int):
        if int(key) > step and state["steps"][key]["status"] != "pending":
            state["steps"][key] = pending_step()
            reset.append(int(key))
    return reset


def first_not_done(state: dict) -> int | None:
    for key in sorted(state["steps"], key=int):
        if state["steps"][key]["status"] != "done":
            return int(key)
    return None


def summary(state: dict, path: Path, **extra) -> dict:
    steps = state["steps"]
    return {
        "state_file": str(path),
        **extra,
        "next_step": first_not_done(state),
        "steps": {key: steps[key]["status"] for key in sorted(steps, key=int)},
        "stopped": [
            {"step": int(key), "note": steps[key]["note"]}
            for key in sorted(steps, key=int)
            if steps[key]["status"] == "stopped"
        ],
    }


def cmd_init(args: argparse.Namespace) -> dict:
    steps = load_steps()
    out_dir = Path(args.out)
    path = state_path(out_dir, args.slug)
    if not path.exists():
        state = {
            "schema_version": SCHEMA_VERSION,
            "slug": args.slug,
            "focus_keyword": args.focus,
            "created": now()[:10],
            "steps": {str(n): pending_step() for n in sorted(steps)},
        }
        write_state(path, state)
        return summary(state, path, created=True, reset=[])

    state = read_state(path)
    if state["focus_keyword"] != args.focus:
        raise StateError(f"{path} belongs to the focus keyword {state['focus_keyword']!r}")
    # The checklist is the list of steps. Add new steps, drop removed ones.
    state["steps"] = {str(n): state["steps"].get(str(n), pending_step()) for n in sorted(steps)}
    reset: set[int] = set()
    for key, step in state["steps"].items():
        redo = step["status"] == "in_progress"
        if step["status"] == "done":
            missing_file = any(not Path(p).is_file() for p in step["outputs"])
            no_result = not step["outputs"] and not step["note"]
            redo = missing_file or no_result
        if redo:
            state["steps"][key] = pending_step()
            reset.add(int(key))
    first = first_not_done(state)
    if first is not None:
        reset.update(reset_after(state, first))
    write_state(path, state)
    return summary(state, path, created=False, reset=sorted(reset))


def cmd_set(args: argparse.Namespace) -> dict:
    steps = load_steps()
    out_dir = Path(args.out)
    path = state_path(out_dir, args.slug)
    if not path.exists():
        raise StateError(f"{path} does not exist. Run init first")
    if args.step not in steps:
        raise StateError(f"the checklist has no Step {args.step}")
    state = read_state(path)
    key = str(args.step)
    current = state["steps"][key]
    reset: list[int] = []

    if args.status == "in_progress":
        for earlier in range(1, args.step):
            if state["steps"][str(earlier)]["status"] != "done":
                raise StateError(f"Step {earlier} is not done. Do the steps in order")
        reset = reset_after(state, args.step)
        if current["status"] == "done":
            current["outputs"] = []
    elif current["status"] != "in_progress":
        raise StateError(f"Step {args.step} is {current['status']}. Set it to in_progress first")

    if args.status == "stopped" and not args.note:
        raise StateError("stopped needs --note with the question to the user")

    if args.status == "done" and args.step == GATE_STEP:
        accept_gate(state, steps, args.note)

    if args.status == "done":
        if args.file:
            missing = [f for f in args.file if not Path(f).is_file()]
            found = [str(Path(f)) for f in args.file if Path(f).is_file()]
        else:
            found, missing = find_outputs(out_dir, args.slug, steps[args.step])
        if missing:
            raise StateError(f"Step {args.step} has no output file: {', '.join(missing)}")
        current["outputs"] = found

    current["status"] = args.status
    if args.note is not None:
        current["note"] = args.note
    current["updated"] = now()
    write_state(path, state)
    return summary(state, path, step=args.step, status=args.status, reset=reset)


# The A-to-B gate (Step 11).

GATE_STEP = 11
GATE_STOP_AFTER = 2  # fails in a row. A project rule, not a rule of the course.
NARROWER_CLAIM = re.compile(r"narrower claim:", re.I)


class GateFail(Exception):
    """A file of the brief that the gate cannot read. `step` made the file."""

    def __init__(self, step: int, message: str) -> None:
        super().__init__(message)
        self.step = step


def output_file(state: dict, step: int, suffix: str = "") -> Path:
    """Return the output file of `step` that ends with `suffix`, from the state file."""
    for name in state["steps"][str(step)]["outputs"]:
        if name.endswith(suffix):
            path = Path(name)
            if not path.is_file():
                raise GateFail(step, f"{path} does not exist")
            return path
    raise GateFail(step, f"Step {step} recorded no output file{' ending with ' + suffix if suffix else ''}")


def section(text: str, heading: str, step: int, file_name: str) -> str:
    """Return the text under `heading`, up to the next heading of the same or a higher level."""
    level = len(heading) - len(heading.lstrip("#"))
    lines = text.splitlines()
    try:
        start = lines.index(heading) + 1
    except ValueError:
        raise GateFail(step, f"{file_name} has no {heading!r} section") from None
    end = len(lines)
    for index in range(start, len(lines)):
        hashes = len(lines[index]) - len(lines[index].lstrip("#"))
        if 0 < hashes <= level and lines[index][hashes:hashes + 1] == " ":
            end = index
            break
    return "\n".join(lines[start:end])


def table_rows(text: str) -> list[dict[str, str]]:
    """Read the first Markdown table in `text` as rows of {column: cell}."""
    rows = [line for line in text.splitlines() if line.startswith("|")]
    if len(rows) < 2:
        return []
    header = table_cells(rows[0])
    return [dict(zip(header, table_cells(line))) for line in rows[2:]]


def table_cells(line: str) -> list[str]:
    """Split a table row at each `|` that is not escaped as `\\|`."""
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [cell.replace("\\|", "|").strip() for cell in cells]


def line_value(text: str, label: str) -> str | None:
    """Return the value of the first line `- label: value`."""
    match = re.search(rf"^- {re.escape(label)}:[ \t]*(.*)$", text, re.M)
    return match.group(1).strip() if match else None


def source_numbers(evidence: str) -> set[int]:
    """Return the number at the start of each comma item. Text in brackets is not a source #."""
    without_brackets = re.sub(r"\([^)]*\)", "", evidence)
    numbers = set()
    for item in without_brackets.split(","):
        match = re.match(r"\s*(\d+)\b", item)
        if match:
            numbers.add(int(match.group(1)))
    return numbers


def outline_v2_blocks(outline_v2: str) -> tuple[list[dict], str, str]:
    """Return (the H2 blocks, the FAQ text, the Still Open text) of Outline V2."""
    h2_blocks: list[dict] = []
    named: dict[str, str] = {}
    for block in re.split(r"^(?=### )", outline_v2, flags=re.M):
        title = block.splitlines()[0] if block.strip() else ""
        if title.startswith("### H2:"):
            evidence_line = line_value(block, "Evidence") or ""
            evidence, _, claim = NARROWER_CLAIM.sub("Narrower claim:", evidence_line).partition("Narrower claim:")
            h2_blocks.append({
                "heading": title.removeprefix("### H2:").strip(),
                "facets": set(re.findall(r"\bF\d+\b", line_value(block, "Facets") or "")),
                "gains": set(re.findall(r"\bI\d+\b", line_value(block, "Gains") or "")),
                "sources": source_numbers(evidence),
                "claim": claim.strip().rstrip(".").strip(),
            })
        elif title.startswith("### "):
            named[title[4:].strip()] = block.split("\n", 1)[1] if "\n" in block else ""
    return h2_blocks, named.get("FAQ", ""), named.get("Still Open", "").strip()


def comparable(text: str) -> list[str]:
    """Lines of an outline without the Title line, blank lines, and trailing spaces."""
    return [line.rstrip() for line in text.splitlines() if line.strip() and not line.startswith("Title:")]


def gate_checks(state: dict) -> tuple[list[dict], dict]:
    """Run every check of the gate. Return (items, credits)."""
    items: list[dict] = []
    files: dict[str, str] = {}

    def item(gate: str, check: str, result: str, detail: str = "", redo: int | None = None) -> None:
        items.append({"gate": gate, "check": check, "result": result, "detail": detail, "redo": redo})

    def read(step: int, suffix: str) -> str:
        if suffix not in files:
            files[suffix] = output_file(state, step, suffix).read_text(encoding="utf-8")
        return files[suffix]

    def check(gate: str, name: str, redo: int, run) -> None:
        """Run one check. run() returns (result, detail). A GateFail is a fail."""
        try:
            result, detail = run()
        except GateFail as exc:
            item(gate, name, "fail", str(exc), exc.step)
            return
        item(gate, name, result, detail, redo if result == "fail" else None)

    # Files on disk.
    missing = [
        (int(key), path)
        for key, step in sorted(state["steps"].items(), key=lambda pair: int(pair[0]))
        if int(key) < GATE_STEP
        for path in step["outputs"]
        if not Path(path).is_file()
    ]
    if missing:
        item("files", "Output files", "fail", ", ".join(path for _, path in missing), missing[0][0])
    else:
        item("files", "Output files", "pass")

    # Direction.
    def serp_decision():
        text = read(2, "-search-intent.md")
        decision, choice = line_value(text, "Decision"), line_value(text, "User choice")
        if decision == "continue" or choice == "write anyway":
            return "pass", f"Decision: {decision}. User choice: {choice}."
        return "fail", f"Decision: {decision}. User choice: {choice}."

    def supported_page():
        rows = table_rows(section(read(1, "-task-brief.md"), "## Page", 1, "task-brief.md"))
        page = next((row.get("Value", "") for row in rows if row.get("Item") == "Page this post supports"), None)
        if page is None:
            raise GateFail(1, "task-brief.md has no Page this post supports row")
        if page.lower().startswith("missing"):
            return "warn", "No page to link to. The post has no internal link."
        return "pass", page

    check("direction", "SERP decision", 2, serp_decision)
    check("direction", "Page this post supports", 1, supported_page)
    item("direction", "Competitive opportunity", "not built", "A-04 is not built yet.")

    # Structure and evidence read Outline V2.
    def outline_v2() -> str:
        return section(read(8, "-outline.md"), "## Outline V2", 8, "outline.md")

    def kept_facets():
        rows = table_rows(section(read(3, "-demand-facets.md"), "## Kept Facets", 3, "demand-facets.md"))
        kept = {row["ID"] for row in rows if row.get("ID")}
        h2_blocks, _, _ = outline_v2_blocks(outline_v2())
        used = set().union(*(block["facets"] for block in h2_blocks))
        problems = []
        if kept - used:
            problems.append(f"not in an H2: {', '.join(sorted(kept - used))}")
        if used - kept:
            problems.append(f"not a kept facet: {', '.join(sorted(used - kept))}")
        return ("fail", "; ".join(problems)) if problems else ("pass", f"{len(kept)} kept facets")

    def gains():
        rows = table_rows(section(read(7, "-information-gain.md"), "## Gains", 7, "information-gain.md"))
        listed = {row["ID"] for row in rows if row.get("ID")}
        h2_blocks, _, _ = outline_v2_blocks(outline_v2())
        used = set().union(*(block["gains"] for block in h2_blocks))
        problems = []
        if listed - used:
            problems.append(f"not in a Gains line: {', '.join(sorted(listed - used))}")
        if used - listed:
            problems.append(f"not in the gains file: {', '.join(sorted(used - listed))}")
        return ("fail", "; ".join(problems)) if problems else ("pass", f"{len(listed)} gains")

    def calculator():
        outline_v1 = section(read(8, "-outline.md"), "## Outline V1", 8, "outline.md")
        value = line_value(outline_v1, "Calculator")
        if not value or "[" in value:
            return "fail", f"Calculator line of Outline V1: {value!r}"
        return "pass", value

    def content_outline():
        v2 = outline_v2()
        brief = section(read(10, ""), "## Content Outline", 10, "brief.md")
        brief_lines = [line for line in comparable(brief) if not line.startswith("**Outline file**")]
        for brief_line, outline_line in zip_longest(brief_lines, comparable(v2), fillvalue="(no line)"):
            if brief_line != outline_line:
                return "fail", f"Outline V2 has {outline_line!r}. The brief has {brief_line!r}"
        return "pass", ""

    check("structure", "Kept facets in Outline V2", 8, kept_facets)
    check("structure", "Gains in Outline V2", 8, gains)
    check("structure", "Calculator", 8, calculator)
    check("structure", "Content Outline", 9, content_outline)

    def adopted_sources():
        rows = table_rows(section(read(6, "-evidence-plan.md"), "## Sources", 6, "evidence-plan.md"))
        adopted = {int(row["#"]) for row in rows if row.get("Status") == "adopted" and row.get("#", "").isdigit()}
        h2_blocks, faq, _ = outline_v2_blocks(outline_v2())
        cited = set().union(*(block["sources"] for block in h2_blocks))
        for line in faq.splitlines():
            if "Evidence:" in line:
                cited |= source_numbers(line.rsplit("Evidence:", 1)[1])
        not_adopted = sorted(cited - adopted)
        if not_adopted:
            return "fail", f"not adopted in the evidence plan: {', '.join(map(str, not_adopted))}"
        return "pass", f"{len(cited)} sources cited"

    def evidence_or_claim():
        h2_blocks, _, _ = outline_v2_blocks(outline_v2())
        if not h2_blocks:
            raise GateFail(8, "Outline V2 has no H2 block")
        bare = [block["heading"] for block in h2_blocks if not block["sources"] and block["claim"] in ("", "-")]
        return ("fail", f"no source and no narrower claim: {'; '.join(bare)}") if bare else ("pass", "")

    def weak_questions():
        rows = table_rows(section(read(6, "-evidence-plan.md"), "## Questions", 6, "evidence-plan.md"))
        weak = [f"{row.get('ID')}: {row.get('Question')}" for row in rows if row.get("Weak", "").lower() == "yes"]
        return ("warn", "; ".join(weak)) if weak else ("pass", "")

    def still_open():
        _, _, open_text = outline_v2_blocks(outline_v2())
        claims = [line.strip().lstrip("-").strip() for line in open_text.splitlines() if line.strip()]
        if "[" in open_text:
            return "fail", f"Still Open is not filled: {' '.join(claims)}"
        if all(claim.lower().rstrip(".") == "none" for claim in claims):
            return "pass", ""
        return "warn", " ".join(claims)

    check("evidence", "Adopted sources", 8, adopted_sources)
    check("evidence", "Evidence or narrower claim", 8, evidence_or_claim)
    check("evidence", "Weak questions", 6, weak_questions)
    check("evidence", "Still Open", 8, still_open)
    item("evidence", "Semantic baseline", "not built", "A-09 is not built yet.")

    return items, {"step_4": step_4_credits(state), "step_6": step_6_credits(state)}


def step_4_credits(state: dict) -> int | None:
    try:
        text = output_file(state, 4, "-competitor-gaps.md").read_text(encoding="utf-8")
    except GateFail:
        return None
    match = re.search(r"^\| Fetch \|.*?(\d+) credits", text, re.M)
    return int(match.group(1)) if match else None


def step_6_credits(state: dict) -> int | None:
    try:
        text = output_file(state, 6, "-evidence-plan.md").read_text(encoding="utf-8")
        rows = table_rows(section(text, "## Search Plan", 6, "evidence-plan.md"))
    except GateFail:
        return None
    total = next((row for row in rows if row.get("Facet") == "Total"), {})
    value = total.get("Actual credits", "")
    return int(value) if value.isdigit() else None


def accept_gate(state: dict, steps: dict[int, list[str]], answer: str | None) -> None:
    """Let the user accept the brief after a gate. The gate must be newer than Step 1 to Step 10."""
    gate = state.get("gate")
    last_change = max(state["steps"][str(n)]["updated"] for n in steps if n < GATE_STEP)
    if not gate or gate["checked"] < last_change:
        raise StateError(f"Step {GATE_STEP} has no gate result for the current files. Run gate first")
    if not answer:
        raise StateError(f"Step {GATE_STEP} done by hand needs --note with the answer of the user")
    gate["accepted"] = True


def cmd_gate(args: argparse.Namespace) -> dict:
    path = state_path(Path(args.out), args.slug)
    if not path.exists():
        raise StateError(f"{path} does not exist. Run init first")
    state = read_state(path)
    step = state["steps"].get(str(GATE_STEP))
    if step is None or step["status"] != "in_progress":
        status = step["status"] if step else "missing"
        raise StateError(f"Step {GATE_STEP} is {status}. Set it to in_progress first")

    items, credits = gate_checks(state)
    failed = [entry for entry in items if entry["result"] == "fail"]
    result = "fail" if failed else ("warn" if any(entry["result"] == "warn" for entry in items) else "pass")
    previous = state.get("gate") or {}
    if not failed:
        attempt = 0
    elif previous.get("result") == "fail" and not previous.get("accepted"):
        attempt = previous.get("attempt", 0) + 1
    else:
        attempt = 1
    state["gate"] = {
        "result": result,
        "checked": now(),
        "attempt": attempt,
        "redo_from": min(entry["redo"] for entry in failed) if failed else None,
        "credits": credits,
        "items": items,
    }

    if not failed:
        step.update(status="done", outputs=[], note=f"Gate: {result}")
    elif attempt >= GATE_STOP_AFTER:
        listed = "; ".join(f"{entry['check']}: {entry['detail']}" for entry in failed)
        step.update(status="stopped", note=f"The gate failed {attempt} times in a row. {listed}")
    step["updated"] = now()
    write_state(path, state)
    return summary(state, path, gate=state["gate"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init")
    p.add_argument("--slug", required=True)
    p.add_argument("--focus", required=True)
    p.add_argument("--out", default="briefs")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("set")
    p.add_argument("--slug", required=True)
    p.add_argument("--step", type=int, required=True)
    p.add_argument("--status", choices=STATUSES, required=True)
    p.add_argument("--note", help="the question to the user, the answer of the user, or the result of a step with no output file")
    p.add_argument("--file", action="append", help="an output file in another place than the checklist says; replaces the expected files")
    p.add_argument("--out", default="briefs")
    p.set_defaults(func=cmd_set)

    p = sub.add_parser("gate")
    p.add_argument("--slug", required=True)
    p.add_argument("--out", default="briefs")
    p.set_defaults(func=cmd_gate)

    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except (StateError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
