from __future__ import annotations

from typing import Any
from tools._shared import fold_text, domain, err


def filter_research_items(
    items: list[dict[str, Any]] | None = None,
    keyword: str = "",
    exclude_domain: str = "",
    dedup_by: str = "url",
) -> dict[str, Any]:
    """Lọc, loại bỏ trùng lặp và phân loại danh sách các bài viết / tweet đã thu thập."""
    try:
        if items is None or not isinstance(items, list):
            return {
                "tool": "filter_items",
                "error": "ValueError",
                "message": "Items must be a valid list of objects",
            }

        input_count = len(items)
        if input_count == 0:
            return {
                "tool": "filter_items",
                "input_count": 0,
                "output_count": 0,
                "removed_count": 0,
                "items": [],
            }

        filtered: list[dict[str, Any]] = []
        seen_keys: set[str] = set()
        clean_kw = fold_text(keyword.strip()) if keyword else ""
        clean_exclude_domain = exclude_domain.strip().lower()

        for item in items:
            if not isinstance(item, dict):
                continue

            item_url = str(item.get("url") or "").strip()
            item_title = str(item.get("title") or "").strip()
            item_summary = str(item.get("summary") or "").strip()
            item_source = str(item.get("source") or domain(item_url)).lower()

            # 1. Lọc theo exclude_domain nếu có
            if clean_exclude_domain and (clean_exclude_domain in item_source or clean_exclude_domain in item_url.lower()):
                continue

            # 2. Lọc theo keyword nếu có
            if clean_kw:
                combined_text = fold_text(f"{item_title} {item_summary}")
                if clean_kw not in combined_text:
                    continue

            # 3. Lọc trùng lặp (deduplication)
            if dedup_by == "url" and item_url:
                normalized_url = item_url.rstrip("/").lower()
                if normalized_url in seen_keys:
                    continue
                seen_keys.add(normalized_url)
            elif dedup_by == "title" and item_title:
                normalized_title = fold_text(item_title)
                if normalized_title in seen_keys:
                    continue
                seen_keys.add(normalized_title)

            filtered.append(item)

        output_count = len(filtered)
        removed_count = input_count - output_count

        return {
            "tool": "filter_items",
            "input_count": input_count,
            "output_count": output_count,
            "removed_count": removed_count,
            "items": filtered,
        }
    except Exception as exc:
        return err("filter_items", exc)

