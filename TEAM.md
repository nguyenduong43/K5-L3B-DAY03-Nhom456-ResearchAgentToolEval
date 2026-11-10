# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Tùng Dương | 2A202603850 | 26ai.duongnt10@vinuni.edu.vn | nguyenduong43 | Team Leader & Prompt/Tool Optimization Lead (CP1, CP2) |
|   2 | Đỗ Duy Tùng | 2A202603844 |26ai.tungdd@vinuni.edu.vn  |Presceltooo  | Tool & Unit Test Developer (CP3) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## NguyenTungDuong-2A202603850

### Phần việc phụ trách

- **Vai trò Team Leader:** Khởi tạo và quản lý repository nhóm, phân công nhiệm vụ cụ thể cho các thành viên, điều phối và theo dõi tiến độ hoàn thành các Checkpoint (CP1 đến CP5).
- Chịu trách nhiệm trực tiếp kỹ thuật CP1 (Setup & Baseline v0) và CP2 (Tối ưu Prompt & Tool Declaration v1).
- Quản lý branch `NguyenTungDuong`, rà soát tích hợp mã nguồn và hỗ trợ tổng hợp báo cáo nhóm.

### Đóng góp cụ thể

- **Tổ chức và điều phối nhóm:** Phân chia công việc rõ ràng theo thế mạnh của từng thành viên (giao phụ trách tool mới và unit test CP3, bộ eval nhóm CP4), thiết lập quy trình làm việc theo nhánh Git và merge PR vào `main`.
- Thiết lập môi trường chạy Gemini (`gemini-3.5-flash-lite`), bổ sung dependency `streamlit` vào `starter_v0/requirements.txt`.
- Chạy baseline v0 đạt 0.65 (13/20 pass), bóc tách nguyên nhân 7 ca thất bại (R03, R10, R11, R12, R13, M02, M06).
- Tối ưu hóa toàn diện `system_prompt.md` (xóa bỏ chỉ dẫn xấu, thiết lập boundary clarify/send, routing rules, multi-turn context) và `tools.yaml` (mô tả chi tiết khi nào dùng/không dùng, chuẩn hóa quy ước tham số).
- Chạy eval bản v1 đạt điểm số tuyệt đối 1.00 (20/20 test cases pass).
- Commit và push kết quả lên branch `NguyenTungDuong`.

### Bằng chứng

- Báo cáo cá nhân: `report/team/2A202603850_NguyenTungDuong.md`
- Prompt & Tools: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`
- Log thí nghiệm: `starter_v0/runs/v0_B_base_gemini_20261110T175614772210.json` (0.65) và `starter_v0/runs/v1_B_base_gemini_20261110T184407163680.json` (1.00)
- Commit: `3cbf2df feat: complete CP1 baseline v0 and optimize prompt and tools v1` (branch `NguyenTungDuong`)

## DoDuyTung-2A202603844

### Phần việc phụ trách

- Chịu trách nhiệm CP3 (Tool mới và Unit Test) và Bonus Challenge: Hơn 3 tool mới (≥ 4 tool do nhóm tự viết).

### Đóng góp cụ thể

- Xây dựng 4 tool mới hoàn chỉnh: `source_check`, `text_stats`, `filter_items`, `sentiment_analysis` (mỗi tool có `tool.py`, `TOOL.md`).
- Đăng ký cả 4 tool trong `tools/__init__.py` và `artifacts/tools.yaml`.
- Viết 12 unit tests trong `tests/test_tools_todo.py` (3 test/tool), kiểm thử offline với `fake_http`.
- Điền mục A2, B5a và B5 Bonus trong `report/team/group_report.md`.

### Bằng chứng

- Báo cáo cá nhân: `report/team/2A202603844_DoDuyTung.md`
- Code: `starter_v0/tools/source_check/`, `starter_v0/tools/text_stats/`, `starter_v0/tools/filter_items/`, `starter_v0/tools/sentiment_analysis/`
- Test: `starter_v0/tests/test_tools_todo.py` (12 passed, toàn bộ suite 94 passed, 0 failed)
