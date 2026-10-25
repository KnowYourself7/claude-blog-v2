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

Every subcommand prints a JSON summary on stdout. Errors are JSON
{"error": ...} on stdout with exit code 1.

Usage:
    python3 brief_state.py init --slug linen-winter --focus "can you wear linen in winter" --out briefs
    python3 brief_state.py set --slug linen-winter --step 2 --status in_progress --out briefs
    python3 brief_state.py set --slug linen-winter --step 2 --status stopped --note "Blog share is 20%. Write anyway, try another keyword, or end?" --out briefs
    python3 brief_state.py set --slug linen-winter --step 5 --status done --note "Template: how-to-guide. Reason: ..." --out briefs
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
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
