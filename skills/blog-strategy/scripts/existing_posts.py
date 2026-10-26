#!/usr/bin/env python3
"""Existing posts and new posts of one blog strategy, written as one plan CSV.

Files, all in the --out folder (default strategy/):
    [site]-existing-posts.json  The posts from the user's CSV, numbered E1, E2, ...
                                Only this script writes it.
    [site]-assignments.jsonl    Claude writes it. One JSON object on each line:
                                the pillar, role, and action of each existing
                                post, and each new post (N1, N2, ...).
    [site]-plan.csv             This script writes it from the two files above.

Subcommands:
    init   Read the user's CSV (columns url, title, lastmod) and write the
           existing-posts file, with the ids E1, E2, ... in URL order. Skip a
           row with no title, a URL that does not start with http:// or
           https://, or a URL that came before. Without --posts, the site has
           no existing posts.
    list   Print one line for each existing post: id | title | lastmod.
    check  Validate the assignments file against the existing posts and the
           pillars. With no error, write the plan CSV and print the counts.

Every subcommand prints JSON on stdout. Errors are JSON {"error": ...} or
{"errors": [...]} on stdout with exit code 1.

Usage:
    python3 existing_posts.py init --site coofandy --posts sitemap-posts.csv --out strategy
    python3 existing_posts.py list --site coofandy --out strategy
    python3 existing_posts.py check --site coofandy --pillars "Linen Care" "Linen Style" --out strategy
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "blog" / "templates"
SCHEMA_VERSION = 1
SITE_SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DUPLICATE_ACTION = re.compile(r"^possible duplicate of (E\d+)$")
POST_ID = re.compile(r"\b[EN]\d+\b")
ROLES = ("pillar", "spoke")
NEW_POST_FIELDS = ("title", "template", "target_keyword", "word_count", "internal_links")
PLAN_COLUMNS = [
    "id", "status", "pillar", "role", "title", "url", "lastmod",
    "template", "target_keyword", "word_count", "internal_links", "action",
]


class PlanError(Exception):
    """A request that the script cannot accept."""


def load_templates(template_dir: Path = TEMPLATE_DIR) -> set[str]:
    """Return the names of the content templates, for example how-to-guide."""
    return {path.stem for path in template_dir.glob("*.md")}


def file_paths(out_dir: Path, site: str) -> dict[str, Path]:
    return {
        "posts": out_dir / f"{site}-existing-posts.json",
        "assignments": out_dir / f"{site}-assignments.jsonl",
        "plan": out_dir / f"{site}-plan.csv",
    }


def write_atomic(path: Path, text: str, encoding: str = "utf-8") -> None:
    """Write through a temporary file, so an interruption never leaves half a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(handle, "w", encoding=encoding, newline="") as stream:
        stream.write(text)
    os.replace(temporary, path)


def read_existing_posts(path: Path) -> list[dict]:
    if not path.is_file():
        raise PlanError(f"{path} does not exist. Run init first")
    return json.loads(path.read_text(encoding="utf-8"))["posts"]


def cmd_init(args: argparse.Namespace) -> dict:
    paths = file_paths(Path(args.out), args.site)
    if paths["posts"].exists() and not args.force:
        raise PlanError(f"{paths['posts']} exists. Add --force to start again")

    kept: dict[str, dict] = {}
    kept_row: dict[str, int] = {}
    skipped: list[dict] = []
    if args.posts:
        with open(args.posts, encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            columns = {name.strip().lower(): name for name in reader.fieldnames or []}
            missing = [name for name in ("url", "title") if name not in columns]
            if missing:
                raise PlanError(f"{args.posts} has no {' and no '.join(missing)} column")
            for row_number, row in enumerate(reader, start=2):
                url = (row.get(columns["url"]) or "").strip()
                title = (row.get(columns["title"]) or "").strip()
                lastmod = (row.get(columns["lastmod"]) or "").strip() if "lastmod" in columns else ""
                reason = None
                if not url.startswith(("http://", "https://")):
                    reason = "url does not start with http:// or https://"
                elif not title:
                    reason = "no title"
                elif url in kept:
                    reason = f"duplicate url, row {kept_row[url]} is kept"
                if reason:
                    skipped.append({"row": row_number, "url": url, "reason": reason})
                    continue
                kept[url] = {"url": url, "title": title, "lastmod": lastmod}
                kept_row[url] = row_number

    posts = [{"id": f"E{number}", **kept[url]} for number, url in enumerate(sorted(kept), start=1)]
    data = {
        "schema_version": SCHEMA_VERSION,
        "site": args.site,
        "source": args.posts or None,
        "created": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "posts": posts,
        "skipped": skipped,
    }
    write_atomic(paths["posts"], json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    return {
        "existing_posts_file": str(paths["posts"]),
        "total": len(posts),
        "no_date": sum(1 for post in posts if not post["lastmod"]),
        "skipped": skipped,
    }


def cmd_list(args: argparse.Namespace) -> dict:
    posts = read_existing_posts(file_paths(Path(args.out), args.site)["posts"])
    return {
        "count": len(posts),
        "posts": [f"{post['id']} | {post['title']} | {post['lastmod'] or '-'}" for post in posts],
    }


def read_assignments(path: Path) -> tuple[list[tuple[int, dict]], list[str]]:
    """Return ([(line number, row)], errors) of the assignments file."""
    if not path.is_file():
        raise PlanError(f"{path} does not exist. Write one line for each post first")
    rows: list[tuple[int, dict]] = []
    errors: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: not valid JSON ({exc.msg})")
            continue
        if not isinstance(row, dict):
            errors.append(f"line {line_number}: not a JSON object")
            continue
        rows.append((line_number, {key: str(value).strip() for key, value in row.items()}))
    return rows, errors


def validate(rows: list[tuple[int, dict]], posts: list[dict], pillars: list[str], templates: set[str]) -> list[str]:
    """Return every error of the assignments, each with its line number and id."""
    errors: list[str] = []
    existing_ids = {post["id"] for post in posts}
    seen: dict[str, int] = {}
    for line_number, row in rows:
        row_id = row.get("id", "")
        if not re.fullmatch(r"[EN]\d+", row_id):
            errors.append(f"line {line_number}: id must be E[n] or N[n], not {row_id!r}")
            continue
        if row_id in seen:
            errors.append(f"line {line_number}: {row_id} has more than one row (first on line {seen[row_id]})")
            continue
        seen[row_id] = line_number
    all_ids = existing_ids | {row_id for row_id in seen if row_id.startswith("N")}
    errors += [f"{post_id} has no row" for post_id in sorted(existing_ids - set(seen), key=lambda i: int(i[1:]))]

    pillar_rows: dict[str, list[str]] = {pillar: [] for pillar in pillars}
    for line_number, row in rows:
        row_id = row.get("id", "")
        if seen.get(row_id) != line_number:
            continue
        where = f"line {line_number}: {row_id}"
        pillar, role, action = row.get("pillar", ""), row.get("role", ""), row.get("action", "")

        if row_id.startswith("E"):
            if row_id not in existing_ids:
                errors.append(f"{where} is not in the existing posts")
                continue
            if pillar == "none":
                if role != "-":
                    errors.append(f"{where}: role must be - for pillar none")
                if not action or action == "keep" or DUPLICATE_ACTION.match(action):
                    errors.append(f"{where}: pillar none needs a reason in action")
                continue
        elif pillar == "none":
            errors.append(f"{where}: a new post needs a pillar")
            continue

        if pillar not in pillar_rows:
            errors.append(f"{where}: pillar {pillar!r} is not one of the pillars")
        if role not in ROLES:
            errors.append(f"{where}: role must be pillar or spoke, not {role!r}")
        elif role == "pillar" and pillar in pillar_rows:
            pillar_rows[pillar].append(row_id)

        if row_id.startswith("E"):
            duplicate = DUPLICATE_ACTION.match(action)
            if duplicate and duplicate.group(1) == row_id:
                errors.append(f"{where}: possible duplicate of itself")
            elif duplicate and duplicate.group(1) not in existing_ids:
                errors.append(f"{where}: {duplicate.group(1)} does not exist")
            elif action != "keep" and not duplicate:
                errors.append(f"{where}: action must be keep or possible duplicate of E[n], not {action!r}")
            continue

        for field in NEW_POST_FIELDS:
            if not row.get(field):
                errors.append(f"{where}: {field} is empty")
        if row.get("template") and row["template"] not in templates:
            errors.append(f"{where}: template {row['template']!r} is not one of {', '.join(sorted(templates))}")
        for target in POST_ID.findall(row.get("internal_links", "")):
            if target not in all_ids:
                errors.append(f"{where}: internal link {target} does not exist")

    for pillar, pillar_ids in pillar_rows.items():
        if not pillar_ids:
            errors.append(f"{pillar} has no pillar row")
        elif len(pillar_ids) > 1:
            errors.append(f"{pillar} has more than one pillar row: {', '.join(pillar_ids)}")
    return errors


def plan_rows(rows: list[tuple[int, dict]], posts: list[dict], pillars: list[str]) -> list[dict]:
    """Return the rows of the plan CSV, in pillar order, then pillar row, existing, new."""
    post_by_id = {post["id"]: post for post in posts}
    plan: list[dict] = []
    for _, row in rows:
        existing = post_by_id.get(row["id"])
        plan.append({
            "id": row["id"],
            "status": "existing" if existing else "new",
            "pillar": row["pillar"],
            "role": row["role"],
            "title": existing["title"] if existing else row["title"],
            "url": existing["url"] if existing else "-",
            "lastmod": (existing["lastmod"] or "-") if existing else "-",
            "template": "-" if existing else row["template"],
            "target_keyword": "-" if existing else row["target_keyword"],
            "word_count": "-" if existing else row["word_count"],
            "internal_links": "-" if existing else row["internal_links"],
            "action": row["action"] if existing else "-",
        })

    def order(entry: dict) -> tuple:
        group = pillars.index(entry["pillar"]) if entry["pillar"] in pillars else len(pillars)
        rank = 0 if entry["role"] == "pillar" else (1 if entry["status"] == "existing" else 2)
        return group, rank, entry["id"][0], int(entry["id"][1:])

    return sorted(plan, key=order)


def cmd_check(args: argparse.Namespace) -> dict:
    paths = file_paths(Path(args.out), args.site)
    posts = read_existing_posts(paths["posts"])
    rows, errors = read_assignments(paths["assignments"])
    errors += validate(rows, posts, args.pillars, load_templates())
    if errors:
        return {"errors": errors}

    plan = plan_rows(rows, posts, args.pillars)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=PLAN_COLUMNS)
    writer.writeheader()
    writer.writerows(plan)
    # utf-8-sig adds the byte order mark, so Excel opens the file as UTF-8.
    write_atomic(paths["plan"], buffer.getvalue(), encoding="utf-8-sig")

    counts = {pillar: {"existing": 0, "new": 0, "possible_duplicates": 0} for pillar in args.pillars}
    for entry in plan:
        if entry["pillar"] in counts:
            counts[entry["pillar"]][entry["status"]] += 1
            if entry["action"].startswith("possible duplicate"):
                counts[entry["pillar"]]["possible_duplicates"] += 1
    return {
        "plan_file": str(paths["plan"]),
        "pillars": counts,
        "none": sum(1 for entry in plan if entry["pillar"] == "none"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init")
    init_parser.add_argument("--posts", help="the user's CSV with the columns url, title, lastmod")
    init_parser.add_argument("--force", action="store_true", help="replace an existing-posts file")
    init_parser.set_defaults(func=cmd_init)

    list_parser = sub.add_parser("list")
    list_parser.set_defaults(func=cmd_list)

    check_parser = sub.add_parser("check")
    check_parser.add_argument("--pillars", nargs="+", required=True, help="the pillar names, in the order of the strategy")
    check_parser.set_defaults(func=cmd_check)

    for subparser in (init_parser, list_parser, check_parser):
        subparser.add_argument("--site", required=True, help="the site slug: lowercase letters, numbers, and hyphens")
        subparser.add_argument("--out", default="strategy")

    args = parser.parse_args(argv)
    try:
        if not SITE_SLUG.match(args.site):
            raise PlanError(f"site {args.site!r} must use only lowercase letters, numbers, and hyphens")
        result = args.func(args)
    except (PlanError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if "errors" in result else 0


if __name__ == "__main__":
    sys.exit(main())
