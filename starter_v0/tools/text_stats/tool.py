from __future__ import annotations

import re
from typing import Any
from tools._shared import fold_text, terms, err


def analyze_text_stats(text: str = "", top_k: int = 5) -> dict[str, Any]:
    """Phân tích số liệu thống kê văn bản: số từ, số ký tự, thời gian đọc, top từ khóa."""
    try:
        if not isinstance(text, str) or not text.strip():
            return {
                "tool": "text_stats",
                "error": "ValueError",
                "message": "Text must be a non-empty string",
            }

        clean_text = text.strip()
        words = re.findall(r"\b\w+\b", clean_text)
        word_count = len(words)
        char_count = len(clean_text)

        # Ước tính thời gian đọc (trung bình 200 từ / phút)
        reading_time_min = round(max(0.1, word_count / 200.0), 2)

        # Trích xuất top từ khóa nổi bật (bỏ stop words thông qua terms)
        term_set = terms(clean_text)
        word_freq: dict[str, int] = {}
        for w in words:
            folded = fold_text(w)
            if folded in term_set:
                word_freq[folded] = word_freq.get(folded, 0) + 1

        # Sắp xếp theo tần suất giảm dần
        sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        effective_top_k = max(1, int(top_k or 5))
        top_keywords = [{"keyword": kw, "count": cnt} for kw, cnt in sorted_keywords[:effective_top_k]]

        # Nhận diện ngôn ngữ sơ bộ
        vn_markers = {"va", "cua", "la", "trong", "cho", "duoc", "khong", "cac", "nguoi"}
        folded_lower = fold_text(clean_text)
        tokens = set(re.findall(r"\b[a-z0-9]+\b", folded_lower))
        has_vn = bool(tokens & vn_markers) or any(ord(c) > 127 for c in clean_text)
        language = "vi" if has_vn else "en"

        return {
            "tool": "text_stats",
            "word_count": word_count,
            "char_count": char_count,
            "reading_time_minutes": reading_time_min,
            "language": language,
            "top_keywords": top_keywords,
        }
    except Exception as exc:
        return err("text_stats", exc)

