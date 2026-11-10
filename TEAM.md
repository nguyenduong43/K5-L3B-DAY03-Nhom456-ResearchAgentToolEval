# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Tùng Dương | 2A202603850 | nguyenduong342003@gmail.com |  | Team Leader & Prompt/Tool Optimization Lead (CP1, CP2) |
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

- Chịu trách nhiệm chung vai trò Team Leader, quản lý repo, cấu hình môi trường.
- Chủ trì CP1 (Setup & Baseline v0) và CP2 (Tối ưu Prompt & Tool Declaration v1–v3).
- Điều phối tích hợp hệ thống và chủ trì soạn thảo Báo cáo nhóm (`group_report.md`).

### Đóng góp cụ thể

- Thiết lập provider Gemini và xử lý cơ chế fallback model tự động khi gặp lỗi 503 Overload.
- Thực hiện chạy baseline v0 và phân loại chi tiết nguyên nhân 6 ca thất bại trong Bảng B2 Failure Analysis.
- Tiến hành 3 vòng lặp tối ưu hóa Prompt và Tool Declaration dựa trên log thực nghiệm (`v1`, `v2`, `v3`), đưa độ chính xác từ 0.70 lên 1.00 (20/20 test cases pass tuyệt đối).
- Ghi nhận đầy đủ nhật ký thí nghiệm trong `artifacts/version_log.csv` và hoàn thiện Bảng B1, B2 trong `group_report.md`.
- Rà soát tính toàn vẹn của hợp đồng tool (`pytest tests/test_tool_contract.py`).

### Bằng chứng

- Báo cáo cá nhân: `report/team/2A202603850_NguyenTungDuong.md`
- Prompt & Tools: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`
- Log thí nghiệm: `starter_v0/artifacts/version_log.csv`, `starter_v0/runs/v0_*.json` đến `v3_*.json`
- Commit: `106f4a0 CP1-CP2: baseline v0 and prompt/tool optimization v1-v3 (Gemini)`

## DoDuyTung-2A202603844

### Phần việc phụ trách

- Chịu trách nhiệm CP3 (Tool mới và Unit Test).

### Đóng góp cụ thể

- Xây dựng tool mới `source_check` (`tools/source_check/tool.py`, `TOOL.md`).
- Đăng ký tool trong `tools/__init__.py` và `artifacts/tools.yaml`.
- Viết 3 unit tests trong `tests/test_tools_todo.py`, kiểm thử offline với `fake_http`.
- Điền mục B5a trong `report/team/group_report.md`.

### Bằng chứng

- Báo cáo cá nhân: `report/team/2A202603844_DoDuyTung.md`
- Code: `starter_v0/tools/source_check/`
- Test: `starter_v0/tests/test_tools_todo.py` (3 passed, toàn bộ suite 70 passed, 0 failed)
