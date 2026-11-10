from __future__ import annotations

import re
from typing import Any
from tools._shared import fold_text, err

# Từ điển sắc thái cảm xúc đa ngôn ngữ (EN + VI)
POSITIVE_LEXICON = {
    # English
    "good", "great", "excellent", "breakthrough", "amazing", "impressive", "success",
    "advance", "promising", "positive", "love", "awesome", "fast", "innovative",
    # Vietnamese
    "tot", "tuyet", "hay", "dot pha", "thanh cong", "tien bo", "an tuong",
    "xuat sac", "tich cuc", "ung y", "khen", "thich", "phat trien", "vuot troi",
}

NEGATIVE_LEXICON = {
    # English
    "bad", "terrible", "awful", "failure", "crash", "bug", "risk", "danger",
    "slow", "poor", "worse", "worst", "disappoint", "flaw", "threat", "hate",
    # Vietnamese
    "te", "xau", "that vong", "loi", "nguy hiem", "rui ro", "kem", "thut lui",
    "that bai", "dinh tre", "cham", "tieu cuc", "chi trich", "lo ngai",
}


def analyze_sentiment(text: str = "", language: str = "auto") -> dict[str, Any]:
    """Phân tích sắc thái cảm xúc (tích cực, tiêu cực, trung lập) của bài viết, tweet hoặc ý kiến."""
    try:
        if not isinstance(text, str) or not text.strip():
            return {
                "tool": "sentiment_analysis",
                "error": "ValueError",
                "message": "Text must be a non-empty string",
            }

        clean_text = text.strip()
        folded_lower = fold_text(clean_text)
        words = re.findall(r"\b[a-z0-9_]+\b", folded_lower)

        pos_matches = []
        neg_matches = []

        # Kiểm tra từ đơn
        for w in words:
            if w in POSITIVE_LEXICON:
                pos_matches.append(w)
            elif w in NEGATIVE_LEXICON:
                neg_matches.append(w)

        # Kiểm tra cụm 2 từ (bigram) cho tiếng Việt (ví dụ: dot pha, thanh cong, rui ro...)
        for i in range(len(words) - 1):
            bigram = f"{words[i]} {words[i+1]}"
            if bigram in POSITIVE_LEXICON and bigram not in pos_matches:
                pos_matches.append(bigram)
            elif bigram in NEGATIVE_LEXICON and bigram not in neg_matches:
                neg_matches.append(bigram)

        pos_count = len(pos_matches)
        neg_count = len(neg_matches)
        total = pos_count + neg_count

        if total == 0:
            score = 0.0
            sentiment = "NEUTRAL"
        else:
            score = round((pos_count - neg_count) / total, 2)
            if score >= 0.2:
                sentiment = "POSITIVE"
            elif score <= -0.2:
                sentiment = "NEGATIVE"
            else:
                sentiment = "NEUTRAL"

        return {
            "tool": "sentiment_analysis",
            "sentiment": sentiment,
            "score": score,
            "positive_signals": list(set(pos_matches)),
            "negative_signals": list(set(neg_matches)),
            "signal_count": total,
        }
    except Exception as exc:
        return err("sentiment_analysis", exc)

