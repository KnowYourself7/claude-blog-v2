"""Tests for the blog-brief keyword pool script (Step 3 mechanical work)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "blog-brief" / "scripts"))

import keyword_pool  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures"


def _items():
    data = json.loads((FIXTURES / "keyword_pool_suggestions.json").read_text(encoding="utf-8"))
    return keyword_pool.items_from_response(data)


def test_items_from_response_collects_items_and_cost():
    data = json.loads((FIXTURES / "keyword_pool_suggestions.json").read_text(encoding="utf-8"))
    items = keyword_pool.items_from_response(data)
    assert [i["keyword"] for i in items][:2] == ["linen pants outfit", "linen pant outfit"]
    assert keyword_pool.response_cost(data) == 0.0102


def test_dedupe_ignores_letter_case_and_keeps_first():
    items = _items()
    kept = keyword_pool.dedupe(items)
    keywords = [i["keyword"] for i in kept]
    assert "Linen Pants Outfit" not in keywords
    assert keywords.count("linen pants outfit") == 1


def test_group_by_core_puts_pointing_keywords_with_their_core():
    rows = keyword_pool.build_pool(keyword_pool.dedupe(_items()), seed_index=3)
    main = {row["main"]: row for row in rows}
    assert "linen pants outfit" in main
    assert sorted(main["linen pants outfit"]["variants"]) == ["linen pant outfit", "outfit with linen pants"]
    assert main["black linen pants outfit"]["variants"] == []


def test_main_keyword_is_highest_volume_then_core_spelling():
    items = [
        {"keyword": "a shirt", "keyword_info": {"search_volume": 100, "monthly_searches": []}, "keyword_properties": {"core_keyword": "shirt a"}, "search_intent_info": None},
        {"keyword": "shirt a", "keyword_info": {"search_volume": 100, "monthly_searches": []}, "keyword_properties": {"core_keyword": None}, "search_intent_info": None},
    ]
    rows = keyword_pool.build_pool(items, seed_index=1)
    assert rows[0]["main"] == "shirt a"


def test_pool_sorted_by_volume_desc_with_null_last_and_call_order_kept():
    rows = keyword_pool.build_pool(keyword_pool.dedupe(_items()), seed_index=3)
    mains = [row["main"] for row in rows]
    assert mains == ["linen pants outfit", "black linen pants outfit"]
    assert rows[0]["volume"] == 1000 and rows[1]["volume"] == 1000


def test_peak_month_picks_highest_and_reports_ties():
    assert keyword_pool.peak_month([{"year": 2026, "month": 6, "search_volume": 1900}, {"year": 2026, "month": 7, "search_volume": 1900}, {"year": 2026, "month": 8, "search_volume": 1000}]) == "Jul 2026: 1900 (2 tied)"
    assert keyword_pool.peak_month([{"year": 2026, "month": 5, "search_volume": 1300}]) == "May 2026: 1300"
    assert keyword_pool.peak_month([]) == "null"
    assert keyword_pool.peak_month(None) == "null"


def test_pool_row_fields_use_null_not_zero():
    rows = keyword_pool.build_pool(keyword_pool.dedupe(_items()), seed_index=3)
    row = rows[0]
    assert row["kd"] == 12
    assert row["intent"] == "informational"
    assert row["other_intents"] == ["commercial"]
    assert row["source"] == "suggestions (seed 3)"
    assert row["peak_month"] == "Jul 2026: 1900 (2 tied)"


def test_other_sources_excludes_keywords_already_in_pool():
    rows = keyword_pool.build_pool(keyword_pool.dedupe(_items()), seed_index=1)
    evidence = {"paa": ["What to wear with linen pants?"], "related": ["Linen Pant Outfit", "linen pants for work"]}
    other = keyword_pool.other_sources(evidence, rows)
    assert [o["keyword"] for o in other] == ["What to wear with linen pants?", "linen pants for work"]
    assert other[0]["source"] == "PAA"
    assert other[1]["source"] == "related search"


def test_render_pool_table_has_template_columns():
    rows = keyword_pool.build_pool(keyword_pool.dedupe(_items()), seed_index=3)
    text = keyword_pool.render_pool_table(rows)
    header = text.splitlines()[0]
    assert header == "| # | Main keyword | Variants | Search volume | Peak month | KD | Intent | Other intents | Source |"
    assert "| 1 | linen pants outfit | linen pant outfit, outfit with linen pants | 1000 | Jul 2026: 1900 (2 tied) | 12 | informational | commercial | suggestions (seed 3) |" in text
    assert "| 2 | black linen pants outfit | none | 1000 | May 2026: 1300 | 0 | transactional | none | suggestions (seed 3) |" in text


def test_rank_facets_sorts_by_evidence_types_then_volume_and_keeps_nine():
    pool = [
        {"n": 1, "main": "shoes with linen pants", "volume": 1000, "kd": 0, "intent": "informational"},
        {"n": 2, "main": "linen pants men", "volume": 1000, "kd": 2, "intent": "transactional"},
        {"n": 3, "main": "wide leg linen pants outfit", "volume": 320, "kd": 0, "intent": "informational"},
    ]
    facets = [
        {"question": "Which shoes go with linen pants?", "evidence": [2, 13], "evidence_parts": ["PAA", "related search"], "rows": [1], "business": "in"},
        {"question": "What do men wear with linen pants?", "evidence": [8], "evidence_parts": ["Autocomplete"], "rows": [2], "business": "in"},
        {"question": "What do women wear with linen pants?", "evidence": [9], "evidence_parts": ["PAA"], "rows": [], "business": "out"},
        {"question": "What goes with wide-leg linen pants?", "evidence": [], "evidence_parts": [], "rows": [3], "business": "in"},
    ]
    kept, other, note = keyword_pool.rank_facets(facets, pool, keep=9, refill_below=5)
    assert [f["id"] for f in kept] == ["F1", "F2", "F3"]
    assert kept[0]["question"].startswith("Which shoes")
    assert kept[0]["evidence_types"] == 3
    assert kept[0]["representative"] == "shoes with linen pants"
    assert kept[2]["representative"] == "wide leg linen pants outfit"
    assert other[0]["reason"] == "outside business"
    assert note == "fewer than 5 facets kept"


def test_rank_facets_lower_rank_after_nine_and_dash_last():
    pool = [{"n": i, "main": f"kw {i}", "volume": 100 - i, "kd": 1, "intent": "informational"} for i in range(1, 12)]
    facets = [{"question": f"Q{i}?", "evidence": [i], "evidence_parts": ["PAA"], "rows": [i], "business": "in"} for i in range(1, 12)]
    facets.append({"question": "No keyword?", "evidence": [1, 2, 3], "evidence_parts": ["PAA", "AI Overview", "related search"], "rows": [], "business": "in"})
    kept, other, note = keyword_pool.rank_facets(facets, pool, keep=9, refill_below=5)
    assert len(kept) == 9
    assert kept[0]["question"] == "No keyword?"
    assert kept[0]["representative"] == "-"
    assert [o["reason"] for o in other] == ["lower rank", "lower rank", "lower rank"]
    assert note == ""


def test_request_uses_basic_auth_and_json_body(monkeypatch):
    seen = {}

    def fake_urlopen(req, timeout=0):
        seen["url"] = req.full_url
        seen["auth"] = req.get_header("Authorization")
        seen["body"] = json.loads(req.data.decode("utf-8"))

        class R:
            def read(self):
                return b'{"cost": 0.01, "tasks": [{"cost": 0.01, "result": [{"items": []}]}]}'
            def __enter__(self):
                return self
            def __exit__(self, *a):
                return False
        return R()

    monkeypatch.setattr(keyword_pool.urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setenv("DATAFORSEO_LOGIN", "user")
    monkeypatch.setenv("DATAFORSEO_PASSWORD", "pass")
    data = keyword_pool.call_api("dataforseo_labs/google/keyword_suggestions/live", [{"keyword": "x", "location_code": 2840, "language_code": "en", "limit": 300}])
    assert seen["url"] == "https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live"
    assert seen["auth"] == "Basic dXNlcjpwYXNz"
    assert seen["body"][0]["limit"] == 300
    assert data["cost"] == 0.01


def test_missing_credentials_is_a_clear_error(monkeypatch):
    monkeypatch.delenv("DATAFORSEO_LOGIN", raising=False)
    monkeypatch.delenv("DATAFORSEO_PASSWORD", raising=False)
    with pytest.raises(keyword_pool.KeywordPoolError, match="DATAFORSEO_LOGIN"):
        keyword_pool.call_api("dataforseo_labs/google/keyword_overview/live", [{}])


def test_rank_facets_representative_can_come_from_other_sources():
    pool = [{"n": 1, "main": "linen pants outfit", "volume": 90, "kd": 1, "intent": "informational"}]
    other = [{"n": 1, "keyword": "how to style linen pants for work", "source": "related search", "volume": 320, "kd": 4, "intent": "informational"},
             {"n": 2, "keyword": "Can I wear linen to work?", "source": "PAA", "volume": None, "kd": None, "intent": None}]
    facets = [{"question": "Can I wear linen pants to work?", "evidence": [1], "evidence_parts": ["PAA"], "rows": [1], "other": [1, 2], "business": "in"}]
    kept, _, _ = keyword_pool.rank_facets(facets, pool, other=other, keep=9, refill_below=5)
    assert kept[0]["representative"] == "how to style linen pants for work"
    assert kept[0]["volume"] == 320
    assert kept[0]["evidence_types"] == 2


def test_username_env_name_is_accepted_too(monkeypatch):
    monkeypatch.delenv("DATAFORSEO_LOGIN", raising=False)
    monkeypatch.setenv("DATAFORSEO_USERNAME", "user")
    monkeypatch.setenv("DATAFORSEO_PASSWORD", "pass")
    assert keyword_pool.credentials() == ("user", "pass")


def test_cli_pool_remove_rank_writes_files(tmp_path, monkeypatch):
    suggestions = json.loads((FIXTURES / "keyword_pool_suggestions.json").read_text(encoding="utf-8"))
    overview = {"cost": 0.004, "tasks": [{"cost": 0.004, "result": [{"items": [
        {"keyword": "linen pants for work", "keyword_info": {"search_volume": 320, "monthly_searches": [{"year": 2026, "month": 4, "search_volume": 390}]}, "keyword_properties": {"keyword_difficulty": 3}, "search_intent_info": {"main_intent": "informational"}}
    ]}]}]}
    calls = []

    def fake_call(endpoint, payload):
        calls.append(endpoint)
        return suggestions if "suggestions" in endpoint else overview

    monkeypatch.setattr(keyword_pool, "call_api", fake_call)
    (tmp_path / "evidence.json").write_text(json.dumps({"paa": ["What to wear with linen pants?"], "related": ["linen pants for work", "linen pants no data"]}), encoding="utf-8")
    out = tmp_path / "briefs"

    assert keyword_pool.main(["pool", "--slug", "t", "--focus", "linen pants outfit", "--seed", "linen pants outfit", "--evidence", str(tmp_path / "evidence.json"), "--out", str(out)]) == 0
    assert calls == ["dataforseo_labs/google/keyword_suggestions/live", "dataforseo_labs/google/keyword_overview/live"]
    pool_md = (out / "t-keyword-pool.md").read_text(encoding="utf-8")
    assert "| 1 | linen pants outfit |" in pool_md
    assert "| 2 | linen pants for work | related search | 320 | Apr 2026: 390 | 3 | informational |" in pool_md
    assert "- linen pants no data (related search)" in pool_md

    (tmp_path / "removed.json").write_text(json.dumps([{"n": 2, "table": "pool", "class": "other task", "reason": "asks for a product, not an outfit"}]), encoding="utf-8")
    assert keyword_pool.main(["remove", "--slug", "t", "--removed", str(tmp_path / "removed.json"), "--out", str(out)]) == 0
    pool_md = (out / "t-keyword-pool.md").read_text(encoding="utf-8")
    assert "| 2 | black linen pants outfit | other task |" in pool_md
    assert "| 2 | black linen pants outfit | none |" not in pool_md

    (tmp_path / "facets.json").write_text(json.dumps([
        {"question": "What goes with linen pants?", "values": [], "evidence": [1], "evidence_parts": ["PAA"], "rows": [1], "other": [], "business": "in", "reason_kept": "the focus question"},
        {"question": "Can I wear linen pants to work?", "values": [], "evidence": [2], "evidence_parts": ["related search"], "rows": [], "other": [2], "business": "in", "reason_kept": "a product line"},
        {"question": "What do women wear?", "values": [], "evidence": [3], "evidence_parts": ["PAA"], "rows": [], "other": [], "business": "out", "reason_kept": ""},
    ]), encoding="utf-8")
    assert keyword_pool.main(["rank-facets", "--slug", "t", "--facets", str(tmp_path / "facets.json"), "--out", str(out)]) == 0
    tables = (out / "t-facet-tables.md").read_text(encoding="utf-8")
    assert "| F1 | What goes with linen pants? |" in tables
    assert "| F2 | Can I wear linen pants to work? | - | 2 | 2 | linen pants for work | 320 | 3 | informational | - | a product line |" in tables
    assert "| F3 | What do women wear? | 3 | - | outside business |" in tables
