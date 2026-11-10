---
name: filter_items
track: bonus
kind: local_formatter
provider: Local Data Processor
requires_env: []
inputs: [items, keyword, exclude_domain, dedup_by]
outputs: [input_count, output_count, removed_count, items]
side_effect: false
---
# filter_items

Lọc, tiền xử lý và loại bỏ các bài viết hoặc tweet bị trùng lặp (deduplication) trước khi định dạng digest hoặc xuất báo cáo.

## Khi nào dùng
- Khi đã thu thập được nhiều items từ các công cụ tìm kiếm (`lookup`, `social_search`, `papers`) và cần lọc bỏ các kết quả trùng lặp URL hoặc tiêu đề.
- Khi cần lọc các bài viết chỉ liên quan đến một từ khóa cụ thể.
- Khi muốn loại bỏ các nguồn tin không mong muốn (`exclude_domain`).

## Khi nào KHÔNG dùng
- Khi chưa có danh sách items nào để lọc (dùng `lookup` hoặc `social_search` trước).
- Khi muốn xuất văn bản định dạng markdown (dùng `format`).

