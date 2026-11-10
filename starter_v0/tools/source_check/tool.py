from __future__ import annotations

from typing import Any
import requests

from tools._shared import TIMEOUT, domain, err

# Bảng phân loại nguồn tin uy tín (Domain Credibility Knowledge Base)
TRUSTED_DOMAINS: dict[str, tuple[int, str, str]] = {
    "arxiv.org": (95, "academic", "Nguồn học thuật preprint uy tín hàng đầu về AI và khoa học"),
    "nature.com": (98, "academic", "Tạp chí khoa học uy tín thế giới"),
    "science.org": (98, "academic", "Tạp chí khoa học uy tín thế giới"),
    "reuters.com": (92, "official_news", "Hãng thông tấn quốc tế chuẩn mực"),
    "apnews.com": (92, "official_news", "Hãng thông tấn Associated Press"),
    "bloomberg.com": (90, "official_news", "Kênh thông tin tài chính kinh tế hàng đầu"),
    "bbc.com": (90, "official_news", "Hãng tin tức uy tín toàn cầu"),
    "techcrunch.com": (85, "tech_media", "Chuyên trang công nghệ và khởi nghiệp"),
    "theverge.com": (85, "tech_media", "Chuyên trang công nghệ uy tín"),
    "openai.com": (90, "official_source", "Trang chính thức của tổ chức nghiên cứu OpenAI"),
    "anthropic.com": (90, "official_source", "Trang chính thức của tổ chức nghiên cứu Anthropic"),
    "github.com": (88, "code_repository", "Nền tảng mã nguồn và repository kỹ thuật"),
}

SUSPICIOUS_TLDS = {".xyz", ".top", ".buzz", ".click", ".link"}


def check_source(url: str = "", verify_dns: bool = True) -> dict[str, Any]:
    """Đánh giá độ tin cậy của URL hoặc tên miền nguồn tin và kiểm tra trạng thái hoạt động."""
    try:
        if not url or not isinstance(url, str) or not url.strip():
            return {
                "tool": "source_check",
                "error": "ValueError",
                "message": "URL must be a non-empty string",
            }

        clean_url = url.strip()
        if not (clean_url.startswith("http://") or clean_url.startswith("https://")):
            clean_url = "https://" + clean_url

        d = domain(clean_url)
        if not d:
            return {
                "tool": "source_check",
                "error": "ValueError",
                "message": f"Cannot parse domain from '{url}'",
            }

        # Đánh giá cơ sở dựa trên domain knowledge base
        trust_score = 50
        category = "general_web"
        note = "Nguồn tin thông thường, cần đối chiếu chéo thông tin"

        matched = False
        for known_domain, (score, cat, reason) in TRUSTED_DOMAINS.items():
            if d == known_domain or d.endswith("." + known_domain):
                trust_score = score
                category = cat
                note = reason
                matched = True
                break

        if not matched:
            for tld in SUSPICIOUS_TLDS:
                if d.endswith(tld):
                    trust_score = 25
                    category = "untrusted_tld"
                    note = f"Tên miền sử dụng đuôi {tld} có rủi ro cao hoặc ít phổ biến"
                    break

        rating = "HIGH" if trust_score >= 80 else ("MEDIUM" if trust_score >= 60 else "LOW")

        is_alive = None
        status_code = None
        if verify_dns:
            # Sử dụng requests.get với stream=True để kiểm tra status mà không tải toàn bộ body
            resp = requests.get(clean_url, timeout=TIMEOUT, stream=True)
            status_code = resp.status_code
            is_alive = 200 <= status_code < 400
            if not is_alive:
                trust_score = max(0, trust_score - 20)
                rating = "LOW"
                note += f" (Cảnh báo: URL trả về mã HTTP {status_code})"

        return {
            "tool": "source_check",
            "url": url,
            "domain": d,
            "trust_score": trust_score,
            "rating": rating,
            "category": category,
            "note": note,
            "is_alive": is_alive,
            "status_code": status_code,
        }
    except Exception as exc:
        return err("source_check", exc)

