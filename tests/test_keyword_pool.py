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


def _response(items, cost=0.01):
    return {"cost": cost, "tasks": [{"cost": cost, "result": [{"items": items}]}]}


AUTOCOMPLETE = _response([
    {"type": "autocomplete", "suggestion": "can you wear linen in winter"},
    {"type": "autocomplete", "suggestion": "can you wear linen pants in winter"},
    {"type": "autocomplete", "suggestion": "Is linen warm?"},
], cost=0.002)

SERP = _response([
    {"type": "organic", "title": "x", "url": "https://a.example"},
    {"type": "people_also_ask", "items": [
        {"type": "people_also_ask_element", "title": "Is linen warm?"},
        {"type": "people_also_ask_element", "title": "How do you layer linen in winter?", "seed_question": "Is linen warm?"},
    ]},
    {"type": "related_searches", "items": ["linen in winter outfit", "can you wear linen pants in winter"]},
], cost=0.006)

RELATED = _response([
    {"keyword_data": {"keyword": "linen in winter outfit", "keyword_info": {"search_volume": 320, "monthly_searches": [{"year": 2026, "month": 1, "search_volume": 500}]}, "keyword_properties": {"keyword_difficulty": 4}, "search_intent_info": {"main_intent": "informational"}}},
    {"keyword_data": {"keyword": "winter linen shirt", "keyword_info": {"search_volume": None, "monthly_searches": []}, "keyword_properties": {"keyword_difficulty": None}, "search_intent_info": None}},
], cost=0.01)

OVERVIEW = _response([
    {"keyword": "is linen warm", "keyword_info": {"search_volume": 1300, "monthly_searches": [{"year": 2025, "month": 12, "search_volume": 1900}]}, "keyword_properties": {"keyword_difficulty": 12}, "search_intent_info": {"main_intent": "informational"}},
], cost=0.004)

AI = _response([
    {"keyword": "is linen warm", "ai_search_volume": 210, "ai_monthly_searches": [{"year": 2026, "month": 9, "ai_search_volume": 210}]},
], cost=0.003)


def test_items_from_response_collects_items_and_cost():
    data = json.loads((FIXTURES / "keyword_pool_suggestions.json").read_text(encoding="utf-8"))
    items = keyword_pool.items_from_response(data)
    assert [i["keyword"] for i in items][:2] == ["linen pants outfit", "linen pant outfit"]
    assert keyword_pool.response_cost(data) == 0.0102


def test_questions_from_suggestions_keep_keyword_metrics():
    data = json.loads((FIXTURES / "keyword_pool_suggestions.json").read_text(encoding="utf-8"))
    found = keyword_pool.questions_from_suggestions(data)
    assert [q["text"] for q in found][:2] == ["linen pants outfit", "linen pant outfit"]
    assert {q["source"] for q in found} == {"keyword suggestion"}
    assert found[0]["volume"] == 1000 and found[0]["kd"] == 12 and found[0]["intent"] == "informational"


def test_normalize_ignores_case_spaces_and_end_punctuation():
    assert keyword_pool.normalize("  Is linen  Warm? ") == "is linen warm"
    assert keyword_pool.normalize("is linen warm") == keyword_pool.normalize("Is linen warm?")


def test_questions_are_read_from_each_response_type():
    assert [q["text"] for q in keyword_pool.questions_from_autocomplete(AUTOCOMPLETE)][:2] == ["can you wear linen in winter", "can you wear linen pants in winter"]
    serp = keyword_pool.questions_from_serp(SERP)
    assert [(q["text"], q["source"]) for q in serp] == [
        ("Is linen warm?", "PAA"),
        ("How do you layer linen in winter?", "PAA"),
        ("linen in winter outfit", "related search"),
        ("can you wear linen pants in winter", "related search"),
    ]
    related = keyword_pool.questions_from_related(RELATED)
    assert related[0]["volume"] == 320 and related[0]["peak_month"] == "Jan 2026: 500"
    assert related[1]["volume"] is None and related[1]["kd"] is None


def test_add_questions_dedupes_across_sources_and_skips_the_seed():
    state = {"questions": []}
    found = keyword_pool.questions_from_autocomplete(AUTOCOMPLETE) + keyword_pool.questions_from_serp(SERP) + keyword_pool.questions_from_related(RELATED)
    added = keyword_pool.add_questions(state, found, "can you wear linen in winter", 1)
    texts = [q["text"] for q in state["questions"]]
    assert added == 5
    assert "can you wear linen in winter" not in texts
    warm = next(q for q in state["questions"] if q["text"] == "Is linen warm?")
    assert warm["sources"] == ["Autocomplete", "PAA"]
    pants = next(q for q in state["questions"] if q["text"] == "can you wear linen pants in winter")
    assert pants["sources"] == ["Autocomplete", "related search"]
    outfit = next(q for q in state["questions"] if q["text"] == "linen in winter outfit")
    assert outfit["sources"] == ["related search", "related keyword"] and outfit["volume"] == 320


def test_peak_month_picks_highest_and_reports_ties():
    assert keyword_pool.peak_month([{"year": 2026, "month": 6, "search_volume": 1900}, {"year": 2026, "month": 7, "search_volume": 1900}, {"year": 2026, "month": 8, "search_volume": 1000}]) == "Jul 2026: 1900 (2 tied)"
    assert keyword_pool.peak_month([]) == "null"
    assert keyword_pool.peak_month(None) == "null"


def test_apply_overview_fills_rows_and_keeps_null_for_missing():
    questions = [
        {"n": 1, "text": "Is linen warm?", "sources": ["PAA"], "volume": None, "peak_month": "null", "kd": None, "intent": None, "no_data": False},
        {"n": 2, "text": "winter linen shirt", "sources": ["related keyword"], "volume": None, "peak_month": "null", "kd": None, "intent": None, "no_data": False},
        {"n": 3, "text": "linen in winter outfit", "sources": ["related keyword"], "volume": 320, "peak_month": "Jan 2026: 500", "kd": 4, "intent": "informational", "no_data": False},
    ]
    missing = keyword_pool.apply_overview(questions, OVERVIEW)
    assert missing == ["winter linen shirt"]
    assert questions[0]["volume"] == 1300 and questions[0]["kd"] == 12 and questions[0]["peak_month"] == "Dec 2025: 1900"
    assert questions[1]["volume"] is None and questions[1]["no_data"] is True
    assert questions[2]["volume"] == 320


def test_rank_facets_sorts_by_source_count_then_volume_and_keeps_nine():
    questions = [
        {"n": 1, "text": "shoes with linen pants", "sources": ["PAA", "related search"], "volume": 1000, "kd": 0, "intent": "informational"},
        {"n": 2, "text": "linen pants men", "sources": ["Autocomplete"], "volume": 1000, "kd": 2, "intent": "transactional"},
        {"n": 3, "text": "wide leg linen pants outfit", "sources": ["related keyword"], "volume": 320, "kd": 0, "intent": "informational"},
        {"n": 4, "text": "Which shoes go with linen pants?", "sources": ["PAA"], "volume": None, "kd": None, "intent": None},
    ]
    facets = [
        {"question": "Which shoes go with linen pants?", "rows": [1, 4], "business": "in"},
        {"question": "What do men wear with linen pants?", "rows": [2], "business": "in"},
        {"question": "What do women wear with linen pants?", "rows": [], "business": "out"},
        {"question": "What goes with wide-leg linen pants?", "rows": [3], "business": "in"},
    ]
    kept, other, note = keyword_pool.rank_facets(facets, questions, keep=9)
    assert [f["id"] for f in kept] == ["F1", "F2", "F3"]
    assert kept[0]["question"].startswith("Which shoes")
    assert kept[0]["source_count"] == 2 and kept[0]["representative"] == "shoes with linen pants"
    assert kept[2]["representative"] == "wide leg linen pants outfit"
    assert other[0]["reason"] == "outside business" and other[0]["id"] == "F4"
    assert note == ""


def test_rank_facets_lower_rank_after_nine_dash_last_and_note_below_three():
    questions = [{"n": i, "text": f"kw {i}", "sources": ["PAA"], "volume": 100 - i, "kd": 1, "intent": "informational"} for i in range(1, 12)]
    facets = [{"question": f"Q{i}?", "rows": [i], "business": "in"} for i in range(1, 12)]
    facets.append({"question": "No keyword?", "rows": [], "business": "in"})
    kept, other, note = keyword_pool.rank_facets(facets, questions, keep=9)
    assert len(kept) == 9
    assert kept[-1]["representative"] != "-"
    assert [o["reason"] for o in other] == ["lower rank", "lower rank", "lower rank"]
    assert note == ""
    kept, _, note = keyword_pool.rank_facets(facets[:2], questions, keep=9)
    assert note == "fewer than 3 facets kept"


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
    data = keyword_pool.call_api(keyword_pool.RELATED, [{"keyword": "x", "location_code": 2840, "language_code": "en", "depth": 2}])
    assert seen["url"] == "https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live"
    assert seen["auth"] == "Basic dXNlcjpwYXNz"
    assert seen["body"][0]["depth"] == 2
    assert data["cost"] == 0.01


def test_missing_credentials_is_a_clear_error(monkeypatch):
    monkeypatch.delenv("DATAFORSEO_LOGIN", raising=False)
    monkeypatch.delenv("DATAFORSEO_PASSWORD", raising=False)
    with pytest.raises(keyword_pool.KeywordPoolError, match="DATAFORSEO_LOGIN"):
        keyword_pool.call_api(keyword_pool.OVERVIEW, [{}])


def test_username_env_name_is_accepted_too(monkeypatch):
    monkeypatch.delenv("DATAFORSEO_LOGIN", raising=False)
    monkeypatch.setenv("DATAFORSEO_USERNAME", "user")
    monkeypatch.setenv("DATAFORSEO_PASSWORD", "pass")
    assert keyword_pool.credentials() == ("user", "pass")


def test_cli_expand_volume_rank_ai_writes_files(tmp_path, monkeypatch):
    calls = []

    def fake_call(endpoint, payload):
        calls.append((endpoint, payload[0]))
        return {
            keyword_pool.AUTOCOMPLETE: AUTOCOMPLETE,
            keyword_pool.ORGANIC: SERP,
            keyword_pool.RELATED: RELATED,
            keyword_pool.OVERVIEW: OVERVIEW,
            keyword_pool.AI_VOLUME: AI,
        }[endpoint]

    monkeypatch.setattr(keyword_pool, "call_api", fake_call)
    out = tmp_path / "briefs"
    focus = "can you wear linen in winter"

    assert keyword_pool.main(["expand", "--slug", "t", "--focus", focus, "--seed", focus, "--round", "1", "--out", str(out)]) == 0
    assert [c[0] for c in calls] == [keyword_pool.AUTOCOMPLETE, keyword_pool.ORGANIC, keyword_pool.RELATED]
    assert calls[1][1]["people_also_ask_click_depth"] == 2 and calls[2][1]["depth"] == 2
    state = json.loads((out / "t-questions.json").read_text(encoding="utf-8"))
    assert len(state["questions"]) == 5 and state["rounds"][0]["total"] == 5
    questions_md = (out / "t-questions.md").read_text(encoding="utf-8")
    assert "| 1 | can you wear linen pants in winter | Autocomplete, related search | 1 | null | null | null | null |" in questions_md

    assert keyword_pool.main(["expand", "--slug", "t", "--focus", focus, "--seed", "linen in winter", "--round", "2", "--out", str(out)]) == 0
    state = json.loads((out / "t-questions.json").read_text(encoding="utf-8"))
    assert len(state["questions"]) == 6  # the seed of round 1 is a new question in round 2
    assert state["rounds"][1]["round"] == 2

    assert keyword_pool.main(["volume", "--slug", "t", "--out", str(out)]) == 0
    assert calls[-1][0] == keyword_pool.OVERVIEW
    questions_md = (out / "t-questions.md").read_text(encoding="utf-8")
    assert "| Is linen warm? | Autocomplete, PAA | 1 | 1300 | Dec 2025: 1900 | 12 | informational |" in questions_md
    assert "- winter linen shirt" in questions_md

    (tmp_path / "facets.json").write_text(json.dumps([
        {"question": "Is linen warm enough for winter?", "values": [], "rows": [2], "business": "in", "reason_kept": "the core question"},
        {"question": "How do you layer linen in winter?", "values": [], "rows": [3, 4], "business": "in", "reason_kept": "a product line"},
        {"question": "What do women wear?", "values": [], "rows": [], "business": "out", "reason_kept": ""},
    ]), encoding="utf-8")
    assert keyword_pool.main(["rank-facets", "--slug", "t", "--facets", str(tmp_path / "facets.json"), "--out", str(out)]) == 0
    tables = (out / "t-facet-tables.md").read_text(encoding="utf-8")
    assert "| F1 | How do you layer linen in winter? | - | linen in winter outfit | 320 | - | 4 | informational | PAA, related keyword, related search | 3, 4 | a product line |" in tables
    assert "| F2 | Is linen warm enough for winter? | - | Is linen warm? | 1300 | - | 12 | informational | Autocomplete, PAA | 2 | the core question |" in tables
    assert "| F3 | What do women wear? | - | outside business |" in tables
    assert "AI search volume: not called." in tables

    assert keyword_pool.main(["ai", "--slug", "t", "--out", str(out)]) == 0
    assert calls[-1][0] == keyword_pool.AI_VOLUME and calls[-1][1]["keywords"] == ["linen in winter outfit", "Is linen warm?"]
    tables = (out / "t-facet-tables.md").read_text(encoding="utf-8")
    assert "| F2 | Is linen warm enough for winter? | - | Is linen warm? | 1300 | 210 |" in tables
    assert "| F1 | How do you layer linen in winter? | - | linen in winter outfit | 320 | null |" in tables
    assert "ai_optimization/ai_keyword_data/keywords_search_volume/live" in tables


SUGGESTIONS = _response([
    {"keyword": "how to wear linen in winter", "keyword_info": {"search_volume": 90, "monthly_searches": [{"year": 2026, "month": 1, "search_volume": 140}]}, "keyword_properties": {"keyword_difficulty": 1}, "search_intent_info": {"main_intent": "informational"}},
    {"keyword": "linen in winter outfit", "keyword_info": {"search_volume": 320, "monthly_searches": []}, "keyword_properties": {"keyword_difficulty": 4}, "search_intent_info": {"main_intent": "informational"}},
], cost=0.0102)


def test_cli_suggest_adds_one_capped_round(tmp_path, monkeypatch, capsys):
    calls = []

    def fake_call(endpoint, payload):
        calls.append((endpoint, payload[0]))
        return {
            keyword_pool.AUTOCOMPLETE: AUTOCOMPLETE,
            keyword_pool.ORGANIC: SERP,
            keyword_pool.RELATED: RELATED,
            keyword_pool.SUGGESTIONS: SUGGESTIONS,
        }[endpoint]

    monkeypatch.setattr(keyword_pool, "call_api", fake_call)
    out = tmp_path / "briefs"
    focus = "can you wear linen in winter"
    assert keyword_pool.main(["expand", "--slug", "t", "--focus", focus, "--seed", focus, "--out", str(out)]) == 0

    assert keyword_pool.main(["suggest", "--slug", "t", "--seed", "wear linen winter", "--out", str(out)]) == 0
    assert calls[-1][0] == keyword_pool.SUGGESTIONS
    assert calls[-1][1]["keyword"] == "wear linen winter" and calls[-1][1]["limit"] == 100
    assert calls[-1][1]["location_code"] == 2840 and calls[-1][1]["language_code"] == "en"
    state = json.loads((out / "t-questions.json").read_text(encoding="utf-8"))
    assert len(state["questions"]) == 6
    new = state["questions"][-1]
    assert new["text"] == "how to wear linen in winter" and new["round"] == "suggest" and new["volume"] == 90
    outfit = next(q for q in state["questions"] if q["text"] == "linen in winter outfit")
    assert outfit["sources"] == ["related search", "related keyword", "keyword suggestion"]
    assert state["rounds"][-1] == {"round": "suggest", "seed": "wear linen winter", "found": 2, "added": 1, "total": 6}
    questions_md = (out / "t-questions.md").read_text(encoding="utf-8")
    assert "| 6 | how to wear linen in winter | keyword suggestion | suggest | 90 | Jan 2026: 140 | 1 | informational |" in questions_md
    assert '| Keyword Suggestions | `dataforseo_labs/google/keyword_suggestions/live` | keyword "wear linen winter", limit 100 | 2 | 0.0102 |' in questions_md

    capsys.readouterr()
    assert keyword_pool.main(["suggest", "--slug", "t", "--seed", "linen winter", "--out", str(out)]) == 1
    assert "already ran" in capsys.readouterr().out
    assert keyword_pool.main(["suggest", "--slug", "t", "--seed", "linen winter", "--limit", "101", "--out", str(out)]) == 1
    assert "--limit must be 1 to 100" in capsys.readouterr().out
    assert len([c for c in calls if c[0] == keyword_pool.SUGGESTIONS]) == 1
