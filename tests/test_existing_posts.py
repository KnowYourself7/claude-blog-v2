"""Tests for the blog-strategy existing-post script (one plan CSV)."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "blog-strategy" / "scripts"))

import existing_posts  # noqa: E402

SITE = "coofandy"
PILLARS = ["Linen Care", "Linen Style"]

POSTS_CSV = """url,title,lastmod
https://example.com/blog/wash-linen,How to Wash Linen,2024-05-02
https://example.com/blog/linen-sneakers,"Linen Pants | With Sneakers",2025-03-14T08:00:00+00:00
https://example.com/blog/iron-linen,How to Iron Linen,
https://example.com/blog/wash-linen,How to Wash Linen (copy),2024-06-01
/blog/relative-url,A relative URL,2024-01-01
https://example.com/blog/no-title,,2024-01-01
https://example.com/blog/dresses,Linen Dresses for Women,2023-08-09
"""


def _run(capsys, out_dir: Path, *args: str) -> tuple[int, dict]:
    code = existing_posts.main([args[0], "--site", SITE, "--out", str(out_dir), *args[1:]])
    return code, json.loads(capsys.readouterr().out)


def _write_posts(tmp_path: Path, text: str = POSTS_CSV) -> Path:
    path = tmp_path / "posts.csv"
    path.write_text(text, encoding="utf-8")
    return path


def _assign(out_dir: Path, rows: list[dict]) -> None:
    lines = "\n".join(json.dumps(row) for row in rows)
    (out_dir / f"{SITE}-assignments.jsonl").write_text(lines + "\n", encoding="utf-8")


def _check(capsys, out_dir: Path) -> tuple[int, dict]:
    return _run(capsys, out_dir, "check", "--pillars", *PILLARS)


@pytest.fixture
def out_dir(tmp_path: Path, capsys) -> Path:
    out = tmp_path / "strategy"
    code, _ = _run(capsys, out, "init", "--posts", str(_write_posts(tmp_path)))
    assert code == 0
    return out


# After init, the posts sorted by URL are:
# E1 dresses, E2 iron-linen, E3 linen-sneakers, E4 wash-linen.
GOOD_ROWS = [
    {"id": "E1", "pillar": "none", "role": "-", "action": "outside business scope: women's clothing"},
    {"id": "E2", "pillar": "Linen Care", "role": "spoke", "action": "possible duplicate of E4"},
    {"id": "E3", "pillar": "Linen Style", "role": "pillar", "action": "keep"},
    {"id": "E4", "pillar": "Linen Care", "role": "spoke", "action": "keep"},
    {"id": "N1", "pillar": "Linen Care", "role": "pillar", "title": "The Linen Care Guide",
     "template": "pillar-page", "target_keyword": "linen care", "word_count": "3,000-4,000",
     "internal_links": "E2, E4, N2"},
    {"id": "N2", "pillar": "Linen Care", "role": "spoke", "title": "How to Remove Wrinkles, \"Fast\"",
     "template": "how-to-guide", "target_keyword": "how to get wrinkles out of linen",
     "word_count": "1,500-2,500", "internal_links": "N1, E4"},
]


def test_init_numbers_the_posts_and_lists_what_it_skipped(tmp_path, capsys):
    out = tmp_path / "strategy"
    code, result = _run(capsys, out, "init", "--posts", str(_write_posts(tmp_path)))
    assert code == 0
    assert result["total"] == 4 and result["no_date"] == 1
    reasons = {item["reason"] for item in result["skipped"]}
    assert reasons == {"duplicate url, row 2 is kept", "url does not start with http:// or https://", "no title"}
    data = json.loads((out / f"{SITE}-existing-posts.json").read_text(encoding="utf-8"))
    assert [post["id"] for post in data["posts"]] == ["E1", "E2", "E3", "E4"]
    assert data["posts"][2] == {
        "id": "E3", "url": "https://example.com/blog/linen-sneakers",
        "title": "Linen Pants | With Sneakers", "lastmod": "2025-03-14T08:00:00+00:00",
    }


def test_init_reads_a_csv_saved_by_excel(tmp_path, capsys):
    path = tmp_path / "posts.csv"
    path.write_text("URL,Title,LastMod\nhttps://example.com/a,A,\n", encoding="utf-8-sig")
    code, result = _run(capsys, tmp_path / "strategy", "init", "--posts", str(path))
    assert code == 0 and result["total"] == 1


def test_init_names_a_missing_column(tmp_path, capsys):
    path = _write_posts(tmp_path, "url,lastmod\nhttps://example.com/a,2024-01-01\n")
    code, result = _run(capsys, tmp_path / "strategy", "init", "--posts", str(path))
    assert code == 1
    assert "title" in result["error"]


def test_init_refuses_to_overwrite_without_force(out_dir, tmp_path, capsys):
    code, result = _run(capsys, out_dir, "init", "--posts", str(_write_posts(tmp_path)))
    assert code == 1
    assert "--force" in result["error"]
    code, _ = _run(capsys, out_dir, "init", "--posts", str(_write_posts(tmp_path)), "--force")
    assert code == 0


def test_init_refuses_a_bad_site_slug(tmp_path, capsys):
    code = existing_posts.main(["init", "--site", "../Coofandy", "--out", str(tmp_path)])
    result = json.loads(capsys.readouterr().out)
    assert code == 1
    assert "site" in result["error"]


def test_list_gives_one_line_for_each_post(out_dir, capsys):
    code, result = _run(capsys, out_dir, "list")
    assert code == 0
    assert result["posts"][0] == "E1 | Linen Dresses for Women | 2023-08-09"
    assert result["posts"][1] == "E2 | How to Iron Linen | -"


def test_check_writes_one_plan_csv_in_order(out_dir, capsys):
    _assign(out_dir, GOOD_ROWS)
    code, result = _check(capsys, out_dir)
    assert code == 0, result
    assert result["pillars"] == {
        "Linen Care": {"existing": 2, "new": 2, "possible_duplicates": 1},
        "Linen Style": {"existing": 1, "new": 0, "possible_duplicates": 0},
    }
    assert result["none"] == 1
    plan = out_dir / f"{SITE}-plan.csv"
    assert plan.read_bytes().startswith(b"\xef\xbb\xbf")
    with plan.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    assert list(rows[0]) == existing_posts.PLAN_COLUMNS
    assert [row["id"] for row in rows] == ["N1", "E2", "E4", "N2", "E3", "E1"]
    assert rows[3]["title"] == 'How to Remove Wrinkles, "Fast"'
    assert rows[4]["title"] == "Linen Pants | With Sneakers"
    assert rows[4]["status"] == "existing" and rows[4]["template"] == "-"
    assert rows[1]["lastmod"] == "-" and rows[3]["url"] == "-"


def test_check_without_existing_posts_plans_only_new_posts(tmp_path, capsys):
    out = tmp_path / "strategy"
    code, result = _run(capsys, out, "init")
    assert code == 0 and result["total"] == 0
    new_rows = [row for row in GOOD_ROWS if row["id"].startswith("N")]
    new_rows += [{"id": "N3", "pillar": "Linen Style", "role": "pillar", "title": "Linen Style Guide",
                  "template": "pillar-page", "target_keyword": "linen style", "word_count": "3,000-4,000",
                  "internal_links": "N1"}]
    for row in new_rows:
        row["internal_links"] = row["internal_links"].replace("E2, E4, ", "").replace(", E4", "")
    _assign(out, new_rows)
    code, result = _check(capsys, out)
    assert code == 0, result
    assert result["none"] == 0


def _replace(row_id: str, **changes) -> list[dict]:
    return [{**row, **changes} if row["id"] == row_id else row for row in GOOD_ROWS]


@pytest.mark.parametrize(
    ("rows", "message"),
    [
        ([row for row in GOOD_ROWS if row["id"] != "E4"], "E4 has no row"),
        (GOOD_ROWS + [GOOD_ROWS[0]], "E1 has more than one row"),
        (GOOD_ROWS + [{**GOOD_ROWS[5], "id": "N1"}], "N1 has more than one row"),
        (GOOD_ROWS + [{"id": "E9", "pillar": "none", "role": "-", "action": "old"}], "E9 is not in"),
        (_replace("E4", pillar="Linen Fit"), "not one of the pillars"),
        (_replace("N2", pillar="none"), "a new post needs a pillar"),
        (_replace("E4", role="hub"), "role"),
        (_replace("E3", role="spoke"), "Linen Style has no pillar row"),
        (_replace("E4", role="pillar"), "Linen Care has more than one pillar row"),
        (_replace("E2", action="possible duplicate of E2"), "duplicate of itself"),
        (_replace("E2", action="possible duplicate of E8"), "E8 does not exist"),
        (_replace("E4", action="update"), "action"),
        (_replace("E1", action=""), "needs a reason"),
        (_replace("E1", role="spoke"), "role must be -"),
        (_replace("N2", template="guide"), "template"),
        (_replace("N2", target_keyword=""), "target_keyword"),
        (_replace("N2", internal_links="N1, N7"), "N7 does not exist"),
        (GOOD_ROWS + [{"id": "X1"}], "id must be"),
    ],
)
def test_check_names_each_error(out_dir, capsys, rows, message):
    _assign(out_dir, rows)
    code, result = _check(capsys, out_dir)
    assert code == 1
    assert any(message in error for error in result["errors"]), result["errors"]
    assert not (out_dir / f"{SITE}-plan.csv").exists()


def test_check_names_the_line_that_is_not_json(out_dir, capsys):
    path = out_dir / f"{SITE}-assignments.jsonl"
    _assign(out_dir, GOOD_ROWS)
    path.write_text(path.read_text(encoding="utf-8") + '{"id": "E1",\n', encoding="utf-8")
    code, result = _check(capsys, out_dir)
    assert code == 1
    assert any(error.startswith("line 7:") for error in result["errors"])


def test_templates_come_from_the_blog_templates_folder():
    names = {path.stem for path in (ROOT / "skills" / "blog" / "templates").glob("*.md")}
    assert existing_posts.load_templates() == names
    assert len(names) == 12


def test_blog_cluster_reads_the_plan_csv_columns():
    cluster = (ROOT / "skills" / "blog-cluster" / "SKILL.md").read_text(encoding="utf-8")
    strategy_import = cluster.split("## Strategy Import", 1)[1].split("\n---", 1)[0]
    assert "-plan.csv" in strategy_import
    for column in existing_posts.PLAN_COLUMNS:
        assert f"`{column}`" in strategy_import, column
