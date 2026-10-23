#!/usr/bin/env python3
"""Mechanical work of blog-brief Step 3: build the keyword pool and rank facets.

The script calls DataForSEO Labs directly over HTTPS with Basic auth. It reads
the credentials from the environment variables DATAFORSEO_LOGIN and
DATAFORSEO_PASSWORD, the same pair that the DataForSEO MCP server uses. Large
API responses never enter the model context: the script keeps them on disk.

Subcommands:
    pool         Call Keyword Suggestions for each seed, build the Keyword Pool
                 and Other Sources tables, call Keyword Overview for the related
                 searches that are not in the pool.
    remove       Move rows to Removed Keywords from a JSON list written by the
                 model (row number, class, reason).
    related      Call Related Keywords (depth 2) for the focus keyword and add
                 the keywords to the pool.
    rank-facets  Rank facets written by the model: representative keyword,
                 evidence type count, business scope, keep the first 9.

Every subcommand prints a JSON summary on stdout and writes files under the
output folder. Errors are JSON {"error": ...} on stdout with exit code 1.

Usage:
    python3 keyword_pool.py pool --slug linen-winter --focus "can you wear linen in winter" \
        --seed "can you wear linen in winter" --seed "linen in winter" \
        --evidence briefs/linen-winter-evidence.json --out briefs
    python3 keyword_pool.py remove --slug linen-winter --removed briefs/linen-winter-removed.json --out briefs
    python3 keyword_pool.py related --slug linen-winter --focus "can you wear linen in winter" --out briefs
    python3 keyword_pool.py rank-facets --slug linen-winter --facets briefs/linen-winter-facets.json --out briefs
"""

from __future__ import annotations

import argparse
import base64
import calendar
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

API_BASE = "https://api.dataforseo.com/v3/"
POOL_COLUMNS = "| # | Main keyword | Variants | Search volume | Peak month | KD | Intent | Other intents | Source |"
POOL_RULE = "|---|--------------|----------|---------------|------------|----|--------|---------------|--------|"
OTHER_COLUMNS = "| # | Keyword | Source | Search volume | Peak month | KD | Intent |"
OTHER_RULE = "|---|---------|--------|---------------|------------|----|--------|"
EVIDENCE_PARTS = ("AI Overview", "PAA", "related search", "organic title", "Autocomplete")


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


# ---------------------------------------------------------------- pool building


def _info(item: dict[str, Any], *keys: str) -> Any:
    value: Any = item
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def dedupe(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Drop exact duplicates; two spellings that differ only in letter case are one."""
    seen: set[str] = set()
    kept = []
    for item in items:
        key = str(item.get("keyword", "")).strip().lower()
        if key in seen:
            continue
        seen.add(key)
        kept.append(item)
    return kept


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


def build_pool(
    items: list[dict[str, Any]], seed_index: int | None = None, source: str = "suggestions"
) -> list[dict[str, Any]]:
    """Group deduplicated items by core_keyword and return pool rows in order."""
    groups: dict[str, list[dict[str, Any]]] = {}
    order: list[str] = []
    for item in items:
        core = _info(item, "keyword_properties", "core_keyword")
        key = str(core or item["keyword"]).strip().lower()
        if key not in groups:
            groups[key] = []
            order.append(key)
        groups[key].append(item)
    label = f"{source} (seed {seed_index})" if seed_index else source
    rows = []
    for key in order:
        members = groups[key]
        best = min((_info(m, "keyword_info", "search_volume") for m in members), key=_volume_key)
        candidates = [m for m in members if _info(m, "keyword_info", "search_volume") == best]
        main = next((m for m in candidates if m["keyword"].strip().lower() == key), candidates[0])
        foreign = _info(main, "search_intent_info", "foreign_intent") or []
        rows.append(
            {
                "main": main["keyword"],
                "variants": [m["keyword"] for m in members if m is not main],
                "volume": _info(main, "keyword_info", "search_volume"),
                "peak_month": peak_month(_info(main, "keyword_info", "monthly_searches")),
                "kd": _info(main, "keyword_properties", "keyword_difficulty"),
                "intent": _info(main, "search_intent_info", "main_intent"),
                "other_intents": list(foreign),
                "source": label,
            }
        )
    rows.sort(key=lambda r: _volume_key(r["volume"]))
    for n, row in enumerate(rows, start=1):
        row["n"] = n
    return rows


def merge_pools(*pools: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge pool rows from several calls, keeping the first row for a spelling."""
    seen: set[str] = set()
    merged = []
    for pool in pools:
        for row in pool:
            spellings = {row["main"].lower(), *(v.lower() for v in row["variants"])}
            if spellings & seen:
                continue
            seen |= spellings
            merged.append(dict(row))
    merged.sort(key=lambda r: _volume_key(r["volume"]))
    for n, row in enumerate(merged, start=1):
        row["n"] = n
    return merged


def other_sources(evidence: dict[str, Any], rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """PAA questions and related searches that are not in the pool."""
    in_pool = {r["main"].lower() for r in rows} | {v.lower() for r in rows for v in r["variants"]}
    out = []
    for text in evidence.get("paa") or []:
        if text.strip().lower() not in in_pool:
            out.append({"keyword": text, "source": "PAA", "volume": None, "peak_month": "-", "kd": None, "intent": None, "no_data": False})
    for text in evidence.get("related") or []:
        if text.strip().lower() not in in_pool:
            out.append({"keyword": text, "source": "related search", "volume": None, "peak_month": "null", "kd": None, "intent": None, "no_data": False})
    for n, row in enumerate(out, start=1):
        row["n"] = n
    return out


def apply_overview(other: list[dict[str, Any]], data: dict[str, Any]) -> list[str]:
    """Fill related-search rows from a Keyword Overview response; return keywords with no data."""
    found = {str(i.get("keyword", "")).lower(): i for i in items_from_response(data)}
    missing = []
    for row in other:
        if row["source"] != "related search":
            continue
        item = found.get(row["keyword"].strip().lower())
        if item is None:
            row["no_data"] = True
            missing.append(row["keyword"])
            continue
        row["volume"] = _info(item, "keyword_info", "search_volume")
        row["peak_month"] = peak_month(_info(item, "keyword_info", "monthly_searches"))
        row["kd"] = _info(item, "keyword_properties", "keyword_difficulty")
        row["intent"] = _info(item, "search_intent_info", "main_intent")
    return missing


# ---------------------------------------------------------------- rendering


def _cell(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, list):
        return ", ".join(value) if value else "none"
    return str(value)


def render_pool_table(rows: list[dict[str, Any]]) -> str:
    lines = [POOL_COLUMNS, POOL_RULE]
    for r in rows:
        lines.append(
            f"| {r['n']} | {r['main']} | {_cell(r['variants'])} | {_cell(r['volume'])} | "
            f"{r['peak_month']} | {_cell(r['kd'])} | {_cell(r['intent'])} | {_cell(r['other_intents'])} | {r['source']} |"
        )
    return "\n".join(lines)


def render_other_table(other: list[dict[str, Any]]) -> str:
    lines = [OTHER_COLUMNS, OTHER_RULE]
    for r in other:
        if r["source"] == "PAA":
            lines.append(f"| {r['n']} | {r['keyword']} | PAA | - | - | - | - |")
        else:
            lines.append(
                f"| {r['n']} | {r['keyword']} | related search | {_cell(r['volume'])} | {r['peak_month']} | {_cell(r['kd'])} | {_cell(r['intent'])} |"
            )
    return "\n".join(lines)


def render_pool_file(state: dict[str, Any]) -> str:
    calls = "\n".join(
        f"| {c['call']} | `{c['endpoint']}` | {c['parameters']} | {c['results']} | {c['cost']} |"
        for c in state["calls"]
    )
    removed = state.get("removed") or []
    removed_lines = "\n".join(
        f"| {r['n']} | {r['keyword']} | {r['class']} | {r['reason']} |" for r in removed
    ) or "| - | none | - | - |"
    not_in_overview = "\n".join(f"- {k} (related search)" for k in state.get("not_in_overview") or []) or "- none"
    return (
        f"# Keyword Pool: {state['focus']}\n\n"
        "Written by `skills/blog-brief/scripts/keyword_pool.py`. The judgment\n"
        f"sections are in `briefs/{state['slug']}-keyword-research.md`.\n\n"
        "## Calls\n\n| Call | Endpoint | Parameters | Results | Cost (USD) |\n|------|----------|------------|---------|------------|\n"
        f"{calls}\n\n"
        "## Keyword Pool\n\n"
        f"{render_pool_table(state['pool'])}\n\n"
        "## Other Sources\n\n"
        f"{render_other_table(state['other'])}\n\n"
        "## Removed Keywords\n\n| Row | Keyword | Class | Reason |\n|-----|---------|-------|--------|\n"
        f"{removed_lines}\n\n"
        "## Not in Overview\n\n"
        f"{not_in_overview}\n"
    )


# ---------------------------------------------------------------- facets


def rank_facets(
    facets: list[dict[str, Any]],
    pool: list[dict[str, Any]],
    other: list[dict[str, Any]] | None = None,
    keep: int = 9,
    refill_below: int = 5,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], str]:
    """Rank facets by evidence types then volume; apply business scope; keep the first `keep`.

    A facet lists pool rows in "rows" and Other Sources rows in "other". The
    representative keyword is the attached keyword with the highest volume;
    on a tie, the pool row that comes first, then the Other Sources row.
    """
    by_n = {r["n"]: r for r in pool}
    by_other = {r["n"]: r for r in other or []}
    ranked = []
    outside = []
    for order, facet in enumerate(facets):
        rows = [by_n[n] for n in facet.get("rows") or [] if n in by_n]
        rows += [
            {**r, "main": r["keyword"], "n": 1000 + r["n"]}
            for n in facet.get("other") or []
            if (r := by_other.get(n)) is not None
        ]
        rows.sort(key=lambda r: (_volume_key(r["volume"]), r["n"]))
        rep = rows[0] if rows else None
        types = len(set(facet.get("evidence_parts") or [])) + (1 if rows else 0)
        entry = {
            **facet,
            "evidence_types": types,
            "representative": rep["main"] if rep else "-",
            "volume": rep["volume"] if rep else None,
            "kd": rep["kd"] if rep else None,
            "intent": rep["intent"] if rep else None,
            "_order": order,
            "_has_rep": rep is not None,
        }
        if facet.get("business") == "out":
            outside.append(entry)
        else:
            ranked.append(entry)
    ranked.sort(key=lambda f: (-f["evidence_types"], 0 if f["_has_rep"] else 1, _volume_key(f["volume"]), f["_order"]))
    kept = ranked[:keep]
    lower = ranked[keep:]
    other = [{**f, "reason": "outside business"} for f in outside] + [{**f, "reason": "lower rank"} for f in lower]
    n = 1
    for f in kept + other:
        f["id"] = f"F{n}"
        n += 1
        f.pop("_order", None)
        f.pop("_has_rep", None)
    note = ""
    if len(kept) < 3:
        note = "fewer than 3 facets kept"
    elif len(kept) < refill_below:
        note = f"fewer than {refill_below} facets kept"
    return kept, other, note


def render_facet_tables(kept: list[dict[str, Any]], other: list[dict[str, Any]]) -> str:
    def rows_text(f: dict[str, Any]) -> str:
        return ", ".join(str(n) for n in f.get("rows") or []) or "-"

    def ev_text(f: dict[str, Any]) -> str:
        return ", ".join(str(n) for n in f.get("evidence") or []) or "-"

    lines = [
        "| ID | Reader question | Values | Evidence | Evidence types | Representative keyword | Search volume | KD | Intent | Rows | Reason kept |",
        "|----|-----------------|--------|----------|----------------|------------------------|---------------|----|--------|------|-------------|",
    ]
    for f in kept:
        vol = "-" if f["representative"] == "-" else _cell(f["volume"])
        kd = "-" if f["representative"] == "-" else _cell(f["kd"])
        intent = "-" if f["representative"] == "-" else _cell(f["intent"])
        lines.append(
            f"| {f['id']} | {f['question']} | {_cell(f.get('values') or []) if f.get('values') else '-'} | {ev_text(f)} | {f['evidence_types']} | "
            f"{f['representative']} | {vol} | {kd} | {intent} | {rows_text(f)} | {f.get('reason_kept', '')} |"
        )
    lines += [
        "",
        "| ID | Reader question | Evidence | Rows | Reason not kept |",
        "|----|-----------------|----------|------|-----------------|",
    ]
    for f in other:
        lines.append(f"| {f['id']} | {f['question']} | {ev_text(f)} | {rows_text(f)} | {f['reason']} |")
    return "\n".join(lines)


# ---------------------------------------------------------------- CLI


def _state_path(out: Path, slug: str) -> Path:
    return out / f"{slug}-keyword-pool.json"


def _load_state(out: Path, slug: str) -> dict[str, Any]:
    path = _state_path(out, slug)
    if not path.exists():
        raise KeywordPoolError(f"run `pool` first: {path} does not exist")
    return json.loads(path.read_text(encoding="utf-8"))


def _save_state(out: Path, slug: str, state: dict[str, Any]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    _state_path(out, slug).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / f"{slug}-keyword-pool.md").write_text(render_pool_file(state), encoding="utf-8")


def cmd_pool(args: argparse.Namespace) -> dict[str, Any]:
    evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8")) if args.evidence else {}
    calls = []
    pools = []
    for i, seed in enumerate(args.seed, start=1):
        data = call_api(
            "dataforseo_labs/google/keyword_suggestions/live",
            [{"keyword": seed, "location_code": args.location, "language_code": args.language, "limit": 300}],
        )
        items = dedupe(items_from_response(data))
        pools.append(build_pool(items, seed_index=i))
        calls.append({"call": f"Keyword Suggestions, seed {i}", "endpoint": "keyword_suggestions/live", "parameters": f'keyword "{seed}", limit 300', "results": len(items), "cost": response_cost(data)})
    pool = merge_pools(*pools)
    other = other_sources(evidence, pool)
    not_in_overview: list[str] = []
    related = [o["keyword"] for o in other if o["source"] == "related search"]
    if related:
        data = call_api(
            "dataforseo_labs/google/keyword_overview/live",
            [{"keywords": related, "location_code": args.location, "language_code": args.language}],
        )
        not_in_overview = apply_overview(other, data)
        calls.append({"call": "Keyword Overview", "endpoint": "keyword_overview/live", "parameters": f"{len(related)} related searches", "results": len(related) - len(not_in_overview), "cost": response_cost(data)})
    else:
        calls.append({"call": "Keyword Overview", "endpoint": "keyword_overview/live", "parameters": "not called", "results": 0, "cost": 0})
    state = {"slug": args.slug, "focus": args.focus, "location": args.location, "language": args.language, "seeds": list(args.seed), "calls": calls, "pool": pool, "other": other, "removed": [], "not_in_overview": not_in_overview}
    _save_state(Path(args.out), args.slug, state)
    return {"pool_rows": len(pool), "other_rows": len(other), "not_in_overview": not_in_overview, "cost": round(sum(c["cost"] for c in calls), 5), "files": [str(_state_path(Path(args.out), args.slug)), str(Path(args.out) / f"{args.slug}-keyword-pool.md")]}


def cmd_remove(args: argparse.Namespace) -> dict[str, Any]:
    state = _load_state(Path(args.out), args.slug)
    removed = json.loads(Path(args.removed).read_text(encoding="utf-8"))
    by_n = {r["n"]: r for r in state["pool"]}
    other_by_n = {r["n"]: r for r in state["other"]}
    for entry in removed:
        table = entry.get("table", "pool")
        source = by_n if table == "pool" else other_by_n
        row = source.get(entry["n"])
        if row is None:
            raise KeywordPoolError(f"no row {entry['n']} in {table}")
        state["removed"].append({"n": entry["n"], "table": table, "keyword": row.get("main") or row.get("keyword"), "class": entry["class"], "reason": entry["reason"]})
        row["removed"] = True
    state["pool"] = [r for r in state["pool"] if not r.get("removed")]
    state["other"] = [r for r in state["other"] if not r.get("removed")]
    _save_state(Path(args.out), args.slug, state)
    return {"removed": len(removed), "pool_rows": len(state["pool"]), "other_rows": len(state["other"])}


def cmd_related(args: argparse.Namespace) -> dict[str, Any]:
    state = _load_state(Path(args.out), args.slug)
    data = call_api(
        "dataforseo_labs/google/related_keywords/live",
        [{"keyword": args.focus, "location_code": state["location"], "language_code": state["language"], "depth": 2}],
    )
    items = dedupe(items_from_response(data))
    new_rows = build_pool(items, source="related")
    before = len(state["pool"])
    state["pool"] = merge_pools(state["pool"], new_rows)
    state["calls"].append({"call": "Related Keywords", "endpoint": "related_keywords/live", "parameters": f'keyword "{args.focus}", depth 2', "results": len(items), "cost": response_cost(data)})
    _save_state(Path(args.out), args.slug, state)
    return {"added_rows": len(state["pool"]) - before, "pool_rows": len(state["pool"]), "cost": response_cost(data)}


def cmd_rank_facets(args: argparse.Namespace) -> dict[str, Any]:
    state = _load_state(Path(args.out), args.slug)
    facets = json.loads(Path(args.facets).read_text(encoding="utf-8"))
    kept, other, note = rank_facets(facets, state["pool"], other=state.get("other"), keep=args.keep, refill_below=5)
    text = render_facet_tables(kept, other)
    path = Path(args.out) / f"{args.slug}-facet-tables.md"
    path.write_text(text + "\n", encoding="utf-8")
    return {"kept": len(kept), "other": len(other), "note": note, "file": str(path)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("pool")
    p.add_argument("--slug", required=True)
    p.add_argument("--focus", required=True)
    p.add_argument("--seed", action="append", required=True)
    p.add_argument("--location", type=int, default=2840)
    p.add_argument("--language", default="en")
    p.add_argument("--evidence", help='JSON object {"paa": [questions], "related": [related searches]} from the Step 2 response')
    p.add_argument("--out", default="briefs")
    p.set_defaults(func=cmd_pool)

    p = sub.add_parser("remove")
    p.add_argument("--slug", required=True)
    p.add_argument("--removed", required=True, help='JSON list of {"n": row number, "table": "pool" or "other", "class": removal class, "reason": one sentence}')
    p.add_argument("--out", default="briefs")
    p.set_defaults(func=cmd_remove)

    p = sub.add_parser("related")
    p.add_argument("--slug", required=True)
    p.add_argument("--focus", required=True)
    p.add_argument("--out", default="briefs")
    p.set_defaults(func=cmd_related)

    p = sub.add_parser("rank-facets")
    p.add_argument("--slug", required=True)
    p.add_argument("--facets", required=True, help='JSON list of facets: {"question", "values": [strings], "evidence": [Question Evidence #], "evidence_parts": [part names], "rows": [pool #], "other": [Other Sources #], "business": "in" or "out", "reason_kept"}')
    p.add_argument("--keep", type=int, default=9)
    p.add_argument("--out", default="briefs")
    p.set_defaults(func=cmd_rank_facets)

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
