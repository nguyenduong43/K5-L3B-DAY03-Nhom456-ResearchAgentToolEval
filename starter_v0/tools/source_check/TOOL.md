---
name: source_check
track: bonus
kind: live_api
provider: HTTP / Domain Knowledge
requires_env: []
inputs: [url, verify_dns]
outputs: [domain, trust_score, rating, category, is_alive]
side_effect: false
---
# source_check

Đánh giá độ tin cậy của một địa chỉ URL hoặc tên miền nguồn tin và kiểm tra trạng thái hoạt động của liên kết.

## Khi nào dùng
- Khi người dùng muốn đánh giá độ tin cậy của một nguồn tin, website hoặc bài báo.
- Khi người dùng hỏi "link này có uy tín/tin cậy không?", "nguồn này thuộc phân loại nào?".
- Khi cần kiểm tra xem một trang web hay URL có đang hoạt động (HTTP status 200) hay không trước khi trích xuất.

## Khi nào KHÔNG dùng
- Khi người dùng muốn đọc toàn bộ nội dung chi tiết bài viết (dùng `fetch`).
- Khi người dùng muốn tìm kiếm từ khóa chung trên Google/web (dùng `lookup`).

