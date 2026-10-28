#!/usr/bin/env python3
"""Mechanical work of blog-brief Step 3: expand demand questions and rank facets.

The script calls DataForSEO directly over HTTPS with Basic auth. It reads the
credentials from the environment variables DATAFORSEO_LOGIN and
DATAFORSEO_PASSWORD, the same pair that the DataForSEO MCP server uses. Large
API responses never enter the model context: the script keeps them on disk.

Subcommands:
    expand       For one seed, call Autocomplete, the organic SERP with PAA
                 click depth 2, and Related Keywords (depth 2). Add the
                 questions and keywords to the questions file (.md and .json),
                 deduplicated, with a Calls table of costs, and report whether
                 the count is below --min (default 9).
    volume       Call Keyword Overview for every question that has no search
                 volume yet. A missing value stays null, never 0.
    rank-facets  Rank facets written by the model: representative keyword,
                 source count, business scope, keep the first 9.
    ai           Call AI Keyword Data for the representative keyword of each
                 kept facet and add the AI search volume column.

Every subcommand prints a JSON summary on stdout and writes files under the
output folder. Errors are JSON {"error": ...} on stdout with exit code 1.

Usage:
    python3 keyword_pool.py expand --slug linen-winter --focus "can you wear linen in winter" \
        --seed "can you wear linen in winter" --round 1 --out briefs
    python3 keyword_pool.py expand --slug linen-winter --focus "can you wear linen in winter" \
        --seed "linen in winter" --round 2 --out briefs
    python3 keyword_pool.py volume --slug linen-winter --out briefs
    python3 keyword_pool.py rank-facets --slug linen-winter --facets briefs/linen-winter-facets.json --out briefs
    python3 keyword_pool.py ai --slug linen-winter --out briefs
"""

from __future__ import annotations

import argparse
import base64
import calendar
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_BASE = "https://api.dataforseo.com/v3/"
AUTOCOMPLETE = "serp/google/autocomplete/live/advanced"
ORGANIC = "serp/google/organic/live/advanced"
RELATED = "dataforseo_labs/google/related_keywords/live"
OVERVIEW = "dataforseo_labs/google/keyword_overview/live"
AI_VOLUME = "ai_optimization/ai_keyword_data/keywords_search_volume/live"
OVERVIEW_CHUNK = 700
AI_CHUNK = 1000
QUESTION_COLUMNS = "| # | Question or keyword | Sources | Round | Search volume | Peak month | KD | Intent |"
QUESTION_RULE = "|---|---------------------|---------|-------|---------------|------------|----|--------|"


class KeywordPoolError(ValueError):
    """Raised when the script cannot do its job."""


# ---------------------------------------------------------------- API client


def credentials() -> tuple[str, str]:
    """Read the DataForSEO login and password from the environment."""
    login = os.environ.get("DATAFORSEO_LOGIN") or os.environ.get("DATAFORSEO_USERNAME")
    password = os.environ.get("DATAFORSEO_PASSWORD")
    if not login or not password:
        raise KeywordPoolError(
            "set DATAFORSEO_LOGIN (or DATAFORSEO_USERNAME) and DATAFORSEO_PASSWORD in the environment"
        )
    return login, password


def call_api(endpoint: str, payload: list[dict[str, Any]]) -> dict[str, Any]:
    """POST one task list to a DataForSEO endpoint and return the parsed JSON."""
    login, password = credentials()
    token = base64.b64encode(f"{login}:{password}".encode("utf-8")).decode("ascii")
    req = urllib.request.Request(
        API_BASE + endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Basic {token}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as exc:  # pragma: no cover - network path
        raise KeywordPoolError(f"{endpoint}: {exc}") from exc


def items_from_response(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Collect items from every result entry of every task."""
    items: list[dict[str, Any]] = []
    for task in data.get("tasks") or []:
        for result in task.get("result") or []:
            for item in result.get("items") or []:
                if "keyword_data" in item:
                    item = item["keyword_data"]
                items.append(item)
    return items


def response_cost(data: dict[str, Any]) -> float:
    return float(data.get("cost") or 0.0)


# ---------------------------------------------------------------- helpers


def _info(item: dict[str, Any], *keys: str) -> Any:
    value: Any = item
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def normalize(text: str) -> str:
    """Key for duplicates: lowercase, single spaces, no end punctuation."""
    text = re.sub(r"\s+", " ", str(text).strip().lower())
    return text.rstrip("?.!").strip()


def peak_month(monthly: list[dict[str, Any]] | None) -> str:
    """Highest month of the last 12. On a tie, the last month and the tie count."""
    if not monthly:
        return "null"
    rows = [m for m in monthly if m.get("search_volume") is not None]
    if not rows:
        return "null"
    rows = sorted(rows, key=lambda m: (m.get("year", 0), m.get("month", 0)))[-12:]
    top = max(m["search_volume"] for m in rows)
    tied = [m for m in rows if m["search_volume"] == top]
    last = tied[-1]
    label = f"{calendar.month_abbr[int(last['month'])]} {last['year']}: {top}"
    if len(tied) > 1:
        label += f" ({len(tied)} tied)"
    return label


def _volume_key(volume: Any) -> tuple[int, int]:
    return (1, 0) if volume is None else (0, -int(volume))


def _metrics(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "volume": _info(item, "keyword_info", "search_volume"),
        "peak_month": peak_month(_info(item, "keyword_info", "monthly_searches")),
        "kd": _info(item, "keyword_properties", "keyword_difficulty"),
        "intent": _info(item, "search_intent_info", "main_intent"),
    }


# ---------------------------------------------------------------- expansion


def questions_from_autocomplete(data: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for item in items_from_response(data):
        if item.get("suggestion"):
            out.append({"text": item["suggestion"], "source": "Autocomplete"})
    return out


def questions_from_serp(data: dict[str, Any]) -> list[dict[str, Any]]:
    """PAA questions and related searches from an organic SERP response."""
    out = []
    for item in items_from_response(data):
        if item.get("type") == "people_also_ask":
            for element in item.get("items") or []:
                if element.get("title"):
                    out.append({"text": element["title"], "source": "PAA"})
        elif item.get("type") == "related_searches":
            for text in item.get("items") or []:
                if isinstance(text, str) and text:
                    out.append({"text": text, "source": "related search"})
    return out


def questions_from_related(data: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    for item in items_from_response(data):
        if item.get("keyword"):
            out.append({"text": item["keyword"], "source": "related keyword", **_metrics(item)})
    return out


def add_questions(state: dict[str, Any], found: list[dict[str, Any]], seed: str, round_number: int) -> int:
    """Merge found questions into the state; a known spelling only gains a source."""
    by_key = {normalize(q["text"]): q for q in state["questions"]}
    added = 0
    for item in found:
        key = normalize(item["text"])
        if not key or key == normalize(seed):
            continue
        known = by_key.get(key)
        if known is not None:
            if item["source"] not in known["sources"]:
                known["sources"].append(item["source"])
            if known.get("volume") is None and item.get("volume") is not None:
                known.update({k: item[k] for k in ("volume", "peak_month", "kd", "intent")})
            continue
        row = {
            "n": len(state["questions"]) + 1,
            "text": item["text"],
            "sources": [item["source"]],
            "round": round_number,
            "seed": seed,
            "volume": item.get("volume"),
            "peak_month": item.get("peak_month", "null"),
            "kd": item.get("kd"),
            "intent": item.get("intent"),
            "no_data": False,
        }
        state["questions"].append(row)
        by_key[key] = row
        added += 1
    return added


def apply_overview(questions: list[dict[str, Any]], data: dict[str, Any]) -> list[str]:
    """Fill rows from a Keyword Overview response; return the keywords with no data."""
    found = {normalize(i.get("keyword", "")): i for i in items_from_response(data)}
    missing = []
    for row in questions:
        if row.get("volume") is not None or row.get("no_data"):
            continue
        item = found.get(normalize(row["text"]))
        if item is None:
            row["no_data"] = True
            missing.append(row["text"])
            continue
        row.update(_metrics(item))
    return missing


# ---------------------------------------------------------------- facets


def rank_facets(
    facets: list[dict[str, Any]], questions: list[dict[str, Any]], keep: int = 9
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    """Rank facets by source count then volume; apply business scope; keep the first `keep`.

    A facet lists question numbers in "rows". The representative keyword is the
    attached question with the highest volume; on a tie, the lowest number.
    """
    by_n = {q["n"]: q for q in questions}
    ranked = []
    outside = []
    for order, facet in enumerate(facets):
        rows = [by_n[n] for n in facet.get("rows") or [] if n in by_n]
        rows.sort(key=lambda r: (_volume_key(r["volume"]), r["n"]))
        rep = rows[0] if rows else None
        sources = sorted({s for r in rows for s in r["sources"]})
        entry = {
            **facet,
            "sources": sources,
            "source_count": len(sources),
            "representative": rep["text"] if rep else "-",
            "volume": rep["volume"] if rep else None,
            "kd": rep["kd"] if rep else None,
            "intent": rep["intent"] if rep else None,
            "ai_volume": None,
            "_order": order,
            "_has_rep": rep is not None,
        }
        if facet.get("business") == "out":
            outside.append(entry)
        else:
            ranked.append(entry)
    ranked.sort(key=lambda f: (-f["source_count"], 0 if f["_has_rep"] else 1, _volume_key(f["volume"]), f["_order"]))
    kept = ranked[:keep]
    lower = ranked[keep:]
    other = [{**f, "reason": "outside business"} for f in outside] + [{**f, "reason": "lower rank"} for f in lower]
    n = 1
    for f in kept + other:
        f["id"] = f"F{n}"
        n += 1
        f.pop("_order", None)
        f.pop("_has_rep", None)
    note = "fewer than 3 facets kept" if len(kept) < 3 else ""
    return kept, other, note


# ---------------------------------------------------------------- rendering


def _cell(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) if value else "none"
    return str(value)


def render_questions_table(questions: list[dict[str, Any]]) -> str:
    lines = [QUESTION_COLUMNS, QUESTION_RULE]
    for q in questions:
        lines.append(
            f"| {q['n']} | {q['text']} | {_cell(q['sources'])} | {q['round']} | {_cell(q['volume'])} | "
            f"{q['peak_month']} | {_cell(q['kd'])} | {_cell(q['intent'])} |"
        )
    return "\n".join(lines)


def render_questions_file(state: dict[str, Any]) -> str:
    calls = "\n".join(
        f"| {c['call']} | `{c['endpoint']}` | {c['parameters']} | {c['results']} | {c['cost']} |"
        for c in state["calls"]
    )
    rounds = "\n".join(
        f"| {r['round']} | {r['seed']} | {r['found']} | {r['added']} | {r['total']} |" for r in state["rounds"]
    ) or "| - | none | - | - | - |"
    no_data = "\n".join(f"- {t}" for t in state.get("no_data") or []) or "- none"
    return (
        f"# Demand Questions: {state['focus']}\n\n"
        "Written by `skills/blog-brief/scripts/keyword_pool.py`. The judgment\n"
        f"sections are in `briefs/{state['slug']}-keyword-research.md`.\n\n"
        "## Calls\n\n| Call | Endpoint | Parameters | Results | Cost (USD) |\n|------|----------|------------|---------|------------|\n"
        f"{calls}\n\n"
        "## Rounds\n\n| Round | Seed | Found | New | Total after |\n|-------|------|-------|-----|-------------|\n"
        f"{rounds}\n\n"
        "## Questions\n\n"
        f"{render_questions_table(state['questions'])}\n\n"
        "## No Overview Data\n\n"
        f"{no_data}\n"
    )


def render_facet_tables(kept: list[dict[str, Any]], other: list[dict[str, Any]], ai_note: dict[str, Any] | None = None) -> str:
    def rows_text(f: dict[str, Any]) -> str:
        return ", ".join(str(n) for n in f.get("rows") or []) or "-"

    lines = [
        "| ID | Reader question | Values | Representative keyword | Search volume | AI search volume | KD | Intent | Sources | Questions | Reason kept |",
        "|----|-----------------|--------|------------------------|---------------|------------------|----|--------|---------|-----------|-------------|",
    ]
    for f in kept:
        no_rep = f["representative"] == "-"
        vol = "-" if no_rep else _cell(f["volume"])
        ai = "-" if no_rep or ai_note is None else _cell(f.get("ai_volume"))
        kd = "-" if no_rep else _cell(f["kd"])
        intent = "-" if no_rep else _cell(f["intent"])
        values = _cell(f.get("values") or []) if f.get("values") else "-"
        lines.append(
            f"| {f['id']} | {f['question']} | {values} | {f['representative']} | {vol} | {ai} | {kd} | {intent} | "
            f"{_cell(f['sources']) if f['sources'] else '-'} | {rows_text(f)} | {f.get('reason_kept', '')} |"
        )
    if ai_note is None:
        lines.append("\nAI search volume: not called.")
    else:
        lines.append(
            f"\nAI search volume: `{AI_VOLUME}`, location {ai_note['location']}, language {ai_note['language']}, "
            f"{ai_note['date']}. It is not a Google search volume; do not add the two."
        )
    lines += [
        "",
        "| ID | Reader question | Questions | Reason not kept |",
        "|----|-----------------|-----------|-----------------|",
    ]
    for f in other:
        lines.append(f"| {f['id']} | {f['question']} | {rows_text(f)} | {f['reason']} |")
    return "\n".join(lines)


# ---------------------------------------------------------------- CLI


def _state_path(out: Path, slug: str) -> Path:
    return out / f"{slug}-questions.json"


def _load_state(out: Path, slug: str) -> dict[str, Any]:
    path = _state_path(out, slug)
    if not path.exists():
        raise KeywordPoolError(f"run `expand` first: {path} does not exist")
    return json.loads(path.read_text(encoding="utf-8"))


def _save_state(out: Path, slug: str, state: dict[str, Any]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    _state_path(out, slug).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / f"{slug}-questions.md").write_text(render_questions_file(state), encoding="utf-8")


def _write_facet_tables(out: Path, slug: str, state: dict[str, Any]) -> Path:
    text = render_facet_tables(state["facets"]["kept"], state["facets"]["other"], state.get("ai_note"))
    path = out / f"{slug}-facet-tables.md"
    path.write_text(text + "\n", encoding="utf-8")
    return path


def cmd_expand(args: argparse.Namespace) -> dict[str, Any]:
    out = Path(args.out)
    path = _state_path(out, args.slug)
    if path.exists():
        state = json.loads(path.read_text(encoding="utf-8"))
    else:
        state = {"slug": args.slug, "focus": args.focus, "location": args.location, "language": args.language, "calls": [], "rounds": [], "questions": [], "no_data": []}
    market = {"location_code": state["location"], "language_code": state["language"]}
    found: list[dict[str, Any]] = []
    cost = 0.0

    data = call_api(AUTOCOMPLETE, [{"keyword": args.seed, "client": "gws-wiz-serp", **market}])
    part = questions_from_autocomplete(data)
    found += part
    cost += response_cost(data)
    state["calls"].append({"call": f"Autocomplete, round {args.round}", "endpoint": AUTOCOMPLETE, "parameters": f'keyword "{args.seed}", client gws-wiz-serp', "results": len(part), "cost": response_cost(data)})

    data = call_api(ORGANIC, [{"keyword": args.seed, "depth": 10, "people_also_ask_click_depth": args.paa_depth, **market}])
    part = questions_from_serp(data)
    found += part
    cost += response_cost(data)
    state["calls"].append({"call": f"Organic SERP with PAA, round {args.round}", "endpoint": ORGANIC, "parameters": f'keyword "{args.seed}", depth 10, people_also_ask_click_depth {args.paa_depth}', "results": len(part), "cost": response_cost(data)})

    data = call_api(RELATED, [{"keyword": args.seed, "depth": args.related_depth, "limit": 100, **market}])
    part = questions_from_related(data)
    found += part
    cost += response_cost(data)
    state["calls"].append({"call": f"Related Keywords, round {args.round}", "endpoint": RELATED, "parameters": f'keyword "{args.seed}", depth {args.related_depth}', "results": len(part), "cost": response_cost(data)})

    added = add_questions(state, found, args.seed, args.round)
    total = len(state["questions"])
    state["rounds"].append({"round": args.round, "seed": args.seed, "found": len(found), "added": added, "total": total})
    _save_state(out, args.slug, state)
    return {"round": args.round, "seed": args.seed, "found": len(found), "added": added, "questions": total, "short": total < args.min, "min": args.min, "cost": round(cost, 5), "files": [str(path), str(out / f"{args.slug}-questions.md")]}


def cmd_volume(args: argparse.Namespace) -> dict[str, Any]:
    out = Path(args.out)
    state = _load_state(out, args.slug)
    todo = [q for q in state["questions"] if q.get("volume") is None and not q.get("no_data")]
    missing: list[str] = []
    cost = 0.0
    for start in range(0, len(todo), OVERVIEW_CHUNK):
        chunk = [q["text"] for q in todo[start:start + OVERVIEW_CHUNK]]
        data = call_api(OVERVIEW, [{"keywords": chunk, "location_code": state["location"], "language_code": state["language"]}])
        missing += apply_overview(state["questions"], data)
        cost += response_cost(data)
        state["calls"].append({"call": "Keyword Overview", "endpoint": OVERVIEW, "parameters": f"{len(chunk)} keywords", "results": len(chunk) - len(missing), "cost": response_cost(data)})
    if not todo:
        state["calls"].append({"call": "Keyword Overview", "endpoint": OVERVIEW, "parameters": "not called", "results": 0, "cost": 0})
    state["no_data"] = sorted(set(state.get("no_data") or []) | set(missing))
    _save_state(out, args.slug, state)
    return {"asked": len(todo), "no_data": missing, "cost": round(cost, 5)}


def cmd_rank_facets(args: argparse.Namespace) -> dict[str, Any]:
    out = Path(args.out)
    state = _load_state(out, args.slug)
    facets = json.loads(Path(args.facets).read_text(encoding="utf-8"))
    kept, other, note = rank_facets(facets, state["questions"], keep=args.keep)
    state["facets"] = {"kept": kept, "other": other}
    state.pop("ai_note", None)
    _save_state(out, args.slug, state)
    path = _write_facet_tables(out, args.slug, state)
    return {"kept": len(kept), "other": len(other), "note": note, "file": str(path)}


def cmd_ai(args: argparse.Namespace) -> dict[str, Any]:
    out = Path(args.out)
    state = _load_state(out, args.slug)
    if "facets" not in state:
        raise KeywordPoolError("run `rank-facets` first: no facets in the state")
    kept = state["facets"]["kept"]
    keywords = [f["representative"] for f in kept if f["representative"] != "-"]
    found: dict[str, Any] = {}
    cost = 0.0
    for start in range(0, len(keywords), AI_CHUNK):
        chunk = keywords[start:start + AI_CHUNK]
        data = call_api(AI_VOLUME, [{"keywords": chunk, "location_code": state["location"], "language_code": state["language"]}])
        for item in items_from_response(data):
            found[normalize(item.get("keyword", ""))] = item.get("ai_search_volume")
        cost += response_cost(data)
        state["calls"].append({"call": "AI Keyword Data", "endpoint": AI_VOLUME, "parameters": f"{len(chunk)} representative keywords", "results": len(found), "cost": response_cost(data)})
    for f in kept:
        f["ai_volume"] = found.get(normalize(f["representative"])) if f["representative"] != "-" else None
    state["ai_note"] = {"location": state["location"], "language": state["language"], "date": dt.date.today().isoformat()}
    _save_state(out, args.slug, state)
    path = _write_facet_tables(out, args.slug, state)
    return {"asked": len(keywords), "with_ai_volume": sum(1 for f in kept if f.get("ai_volume") is not None), "cost": round(cost, 5), "file": str(path)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("expand")
    p.add_argument("--slug", required=True)
    p.add_argument("--focus", required=True)
    p.add_argument("--seed", required=True, help="the keyword to expand: the focus keyword in round 1, the wider seed in round 2")
    p.add_argument("--round", type=int, default=1)
    p.add_argument("--min", type=int, default=9, help="below this many questions the summary says short: true")
    p.add_argument("--paa-depth", type=int, default=2, help="people_also_ask_click_depth, 1 to 4")
    p.add_argument("--related-depth", type=int, default=2, help="Related Keywords depth, 0 to 4")
    p.add_argument("--location", type=int, default=2840)
    p.add_argument("--language", default="en")
    p.add_argument("--out", default="briefs", help="output folder (default: briefs)")
    p.set_defaults(func=cmd_expand)

    p = sub.add_parser("volume")
    p.add_argument("--slug", required=True)
    p.add_argument("--out", default="briefs")
    p.set_defaults(func=cmd_volume)

    p = sub.add_parser("rank-facets")
    p.add_argument("--slug", required=True)
    p.add_argument("--facets", required=True, help='JSON list of facets: {"question", "values": [strings], "rows": [question #], "business": "in" or "out", "reason_kept"}')
    p.add_argument("--keep", type=int, default=9, help="how many facets to keep (default: 9)")
    p.add_argument("--out", default="briefs")
    p.set_defaults(func=cmd_rank_facets)

    p = sub.add_parser("ai")
    p.add_argument("--slug", required=True)
    p.add_argument("--out", default="briefs")
    p.set_defaults(func=cmd_ai)

    args = parser.parse_args(argv)
    try:
        result = args.func(args)
    except (KeywordPoolError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
