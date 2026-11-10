---
name: sentiment_analysis
track: bonus
kind: local_formatter
provider: Sentiment Classifier
requires_env: []
inputs: [text, language]
outputs: [sentiment, score, positive_signals, negative_signals, signal_count]
side_effect: false
---
# sentiment_analysis

Phân tích cảm xúc và sắc thái thái độ (tích cực, tiêu cực, trung lập) của một đoạn văn bản, dòng tweet hoặc bình luận dư luận.

## Khi nào dùng
- Khi người dùng hỏi về phản ứng, cảm xúc hoặc dư luận mạng xã hội đối với một chủ đề (ví dụ: "Người dùng đang khen hay chê mô hình mới?", "Sắc thái của bài viết này là gì?").
- Khi cần đánh giá điểm cảm xúc (sentiment polarity score từ -1.0 đến +1.0) của một tweet hoặc đoạn trích.

## Khi nào KHÔNG dùng
- Khi người dùng muốn tìm kiếm thêm tweet (dùng `social_search`).
- Khi người dùng chỉ muốn tóm tắt thông tin thuần túy mà không quan tâm cảm xúc (dùng `format` hoặc LLM).

