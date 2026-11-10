# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Đỗ Duy Tùng | 2A202603844 |26ai.tungdd@vinuni.edu.vn  |Presceltooo  | Tool & Unit Test Developer (CP3) |
|   2 |        |      |       |        |         |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

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
