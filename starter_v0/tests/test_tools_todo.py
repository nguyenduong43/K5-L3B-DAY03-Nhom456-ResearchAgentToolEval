"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

source_check_tool = TOOL_FUNCTIONS["source_check"]


def test_source_check_happy_path_trusted_domain(fake_http) -> None:
    calls = fake_http(FakeResponse(status_code=200))
    result = source_check_tool(url="https://arxiv.org/abs/2301.00001", verify_dns=True)

    assert result["tool"] == "source_check"
    assert result["domain"] == "arxiv.org"
    assert result["rating"] == "HIGH"
    assert result["trust_score"] >= 90
    assert result["category"] == "academic"
    assert result["is_alive"] is True
    assert len(calls) == 1
    assert calls[0]["url"] == "https://arxiv.org/abs/2301.00001"


def test_source_check_bad_or_missing_input_returns_error_dict() -> None:
    # Model gửi chuỗi rỗng hoặc None -> bắt lỗi trả về error dict, không crash
    res_empty = source_check_tool(url="")
    assert res_empty["error"] == "ValueError"
    assert "URL must be a non-empty string" in res_empty["message"]

    res_none = source_check_tool(url=None)
    assert res_none["error"] == "ValueError"

    res_spaces = source_check_tool(url="   ")
    assert res_spaces["error"] == "ValueError"


def test_source_check_network_failure_returns_error_dict(fake_http) -> None:
    import requests
    fake_http(requests.exceptions.ConnectionError("Failed to resolve host"))
    result = source_check_tool(url="https://reuters.com/world", verify_dns=True)

    assert result["tool"] == "source_check"
    assert result["error"] == "ConnectionError"
    assert "Failed to resolve host" in result["message"]


# ---------------- text_stats ----------------
text_stats_tool = TOOL_FUNCTIONS["text_stats"]


def test_text_stats_happy_path() -> None:
    text = "Trí tuệ nhân tạo đang phát triển rất nhanh. AI mang lại nhiều bước đột phá cho công nghệ và nghiên cứu khoa học."
    result = text_stats_tool(text=text, top_k=3)

    assert result["tool"] == "text_stats"
    assert result["word_count"] >= 15
    assert result["char_count"] > 50
    assert result["reading_time_minutes"] > 0
    assert result["language"] == "vi"
    assert len(result["top_keywords"]) <= 3


def test_text_stats_bad_input_returns_error_dict() -> None:
    res_empty = text_stats_tool(text="")
    assert res_empty["error"] == "ValueError"
    assert "Text must be a non-empty string" in res_empty["message"]

    res_none = text_stats_tool(text=None)
    assert res_none["error"] == "ValueError"

    res_spaces = text_stats_tool(text="    ")
    assert res_spaces["error"] == "ValueError"


def test_text_stats_edge_case_only_punctuation_and_large_top_k() -> None:
    result = text_stats_tool(text="... !!! ??? --- @@@", top_k=10)
    assert result["tool"] == "text_stats"
    assert result["word_count"] == 0
    assert result["top_keywords"] == []


# ---------------- filter_items ----------------
filter_items_tool = TOOL_FUNCTIONS["filter_items"]


def test_filter_items_happy_path_deduplication() -> None:
    items = [
        {"title": "Bài viết 1", "url": "https://example.com/ai-1", "summary": "Nội dung AI 1"},
        {"title": "Bài viết 1 trùng", "url": "https://example.com/ai-1/", "summary": "Nội dung AI 1 trùng"},
        {"title": "Bài viết 2", "url": "https://example.com/ai-2", "summary": "Nội dung AI 2"},
        {"title": "Bài viết 3", "url": "https://example.com/ai-3", "summary": "Nội dung AI 3"},
    ]
    result = filter_items_tool(items=items, dedup_by="url")

    assert result["tool"] == "filter_items"
    assert result["input_count"] == 4
    assert result["output_count"] == 3
    assert result["removed_count"] == 1
    urls = [it["url"].rstrip("/").lower() for it in result["items"]]
    assert len(urls) == len(set(urls))


def test_filter_items_bad_input_returns_error_dict() -> None:
    res_str = filter_items_tool(items="not_a_list")  # type: ignore[arg-type]
    assert res_str["error"] == "ValueError"

    res_none = filter_items_tool(items=None)
    assert res_none["error"] == "ValueError"


def test_filter_items_by_keyword_and_exclude_domain() -> None:
    items = [
        {"title": "Robotics breakthrough", "url": "https://techcrunch.com/robot", "summary": "Good robot"},
        {"title": "AI in healthcare", "url": "https://nature.com/health", "summary": "Health AI"},
        {"title": "Robotics spam", "url": "https://spam.xyz/bad", "summary": "Spam robot news"},
    ]
    result = filter_items_tool(items=items, keyword="robotics", exclude_domain="spam.xyz")

    assert result["tool"] == "filter_items"
    assert result["output_count"] == 1
    assert result["items"][0]["title"] == "Robotics breakthrough"


# ---------------- sentiment_analysis ----------------
sentiment_analysis_tool = TOOL_FUNCTIONS["sentiment_analysis"]


def test_sentiment_analysis_happy_path_positive() -> None:
    text = "Mô hình này là một bước đột phá tuyệt vời, rất thành công, ấn tượng và xuất sắc!"
    result = sentiment_analysis_tool(text=text)

    assert result["tool"] == "sentiment_analysis"
    assert result["sentiment"] == "POSITIVE"
    assert result["score"] >= 0.2
    assert len(result["positive_signals"]) > 0


def test_sentiment_analysis_happy_path_negative() -> None:
    text = "Hệ thống gặp nhiều lỗi nghiêm trọng, chạy rất tệ, gây thất vọng lớn và rủi ro cao."
    result = sentiment_analysis_tool(text=text)

    assert result["tool"] == "sentiment_analysis"
    assert result["sentiment"] == "NEGATIVE"
    assert result["score"] <= -0.2
    assert len(result["negative_signals"]) > 0


def test_sentiment_analysis_bad_input_returns_error_dict() -> None:
    res_empty = sentiment_analysis_tool(text="")
    assert res_empty["error"] == "ValueError"
    assert "Text must be a non-empty string" in res_empty["message"]

    res_none = sentiment_analysis_tool(text=None)
    assert res_none["error"] == "ValueError"
