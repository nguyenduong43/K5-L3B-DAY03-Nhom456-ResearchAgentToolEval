# Báo cáo cá nhân — Nguyễn Ngọc Vinh (2A202603877)

## 1. Thông tin thành viên

- Họ tên: Nguyễn Ngọc Vinh
- MSSV: 2A202603877
- Email: vinh6543210@gmail.com

## 2. Phần việc phụ trách

- Tham gia CP4 — xây dựng bộ 10 eval case của nhóm, gồm 5 case single-turn (`query`) và 5 case multi-turn (`turns`).
- Đảm bảo bộ case có tình huống kiểm tra routing tới tool mới, truyền arguments, giữ ngữ cảnh qua nhiều lượt và trường hợp không cần gọi tool.
- Chạy eval nhóm với provider OpenRouter, version v3; cập nhật kết quả vào bảng B3 của báo cáo nhóm.

## 3. Đóng góp cụ thể

1. Bổ sung 10 case G01–G10 vào `starter_v0/data/eval_group.json`. Các case kiểm tra `source_check`, `text_stats`, `filter_items`, `sentiment_analysis`, `fetch` và hành vi không gọi tool khi có thể trả lời trực tiếp.
2. Tạo cả tình huống multi-turn để kiểm tra agent có giữ URL, văn bản, danh sách item và chuyển đúng tool khi yêu cầu thay đổi hay không.
3. Chạy eval nhóm bằng `openai/gpt-4o-mini`; kết quả ghi nhận 10/10 case PASS, không có provider error.
4. Điền bảng B3 và ghi thông tin run cùng các metric vào `report/team/group_report.md`.

## 4. Bằng chứng

- File:
  - `starter_v0/data/eval_group.json`
  - `starter_v0/runs/v3_B_group_openrouter_20261110T211006130700.json`
  - `report/team/group_report.md` (mục B3)
- Kết quả run: 10/10 case đo được; `case_accuracy`, `tool_routing_accuracy`, `argument_accuracy`, `multiturn_accuracy` đều 1.00; `provider_error_cases` = 0.
- AI/công cụ đã dùng: ChatGPT hỗ trợ lên cấu trúc và soạn case, cũng như tổng hợp kết quả vào báo cáo. Kết quả được đối chiếu với run JSON do eval tạo ra; run cho thấy đủ 10 case và không có provider error.

## 5. Tự đánh giá

- Hoàn thành phần eval nhóm CP4 và có run JSON làm bằng chứng. Bộ case bao gồm cả single-turn, multi-turn và routing tới tool mới.
- Kết quả 10/10 PASS cho thấy model vượt qua các case đã thiết kế; đây không phải bằng chứng rằng agent luôn đúng với mọi yêu cầu thực tế. Cần tiếp tục bổ sung case nếu phát hiện thêm lỗi trong live chat.
