---
name: text_stats
track: bonus
kind: local_formatter
provider: Local Analytics
requires_env: []
inputs: [text, top_k]
outputs: [word_count, char_count, reading_time_minutes, language, top_keywords]
side_effect: false
---
# text_stats

Phân tích số liệu định lượng của một đoạn văn bản nghiên cứu: đếm số từ, độ dài ký tự, ước tính thời gian đọc, nhận diện ngôn ngữ và trích xuất top từ khóa quan trọng nhất.

## Khi nào dùng
- Khi người dùng yêu cầu thống kê số từ, độ dài, thời gian đọc của bài viết hoặc đoạn trích.
- Khi người dùng muốn trích xuất các từ khóa nổi bật (top keywords) của tài liệu.
- Khi cần phân tích định lượng nội dung văn bản.

## Khi nào KHÔNG dùng
- Khi người dùng muốn tóm tắt ý nghĩa bài viết (dùng `fetch` hoặc LLM).
- Khi người dùng muốn tìm kiếm thêm thông tin trên mạng (dùng `lookup`).

