# Báo cáo cá nhân — 2A202603854_NguyenLamTung

## 1. Thông tin thành viên

- Họ tên: Nguyễn Lâm Tùng
- MSSV: 2A202603854
- Email: 26ai.tungnl2@vinuni.edu.vn
- Lớp: L3B — Nhóm 456

## 2. Phần việc phụ trách

Chịu trách nhiệm chính Checkpoint **CP5 (UI, Live Chat, Showcase và Báo cáo)**:
- Thiết kế và phát triển giao diện Web tương tác trực quan cho Research Agent bằng Streamlit (`starter_v0/app.py`).
- Xây dựng cơ chế hiển thị đa lượt (multi-turn), trực quan hóa Tool Calls & Tool Results theo thời gian thực.
- Thiết lập hệ thống tự động ghi nhật ký hội thoại (transcript) chuẩn schema JSON phục vụ đánh giá Rubric C6.
- Cấu hình và triển khai mạng hầm Cloudflare Tunnel (`cloudflared`) để public link demo phục vụ Team Showdown lúc 16:30.
- Thiết kế Poster giới thiệu Agent định dạng HTML một trang (`report/team/poster.html`).
- Soạn thảo Phần A (Giới thiệu agent, danh mục tool, câu hỏi mẫu) và chuẩn bị khung Phần B của Báo cáo nhóm (`report/team/group_report.md`).

## 3. Đóng góp cụ thể

1. **Xây dựng Web UI Streamlit (`starter_v0/app.py`):**
   - Tích hợp vòng lặp mô hình (`run_model_tool_loop`) từ agent core, cho phép chuyển đổi linh hoạt giữa các model provider (Gemini, OpenRouter, OpenAI, Anthropic, Ollama) và các version artifact (v0, v1, v2, v3).
   - Thiết kế sidebar cấu hình tham số suy luận: `max_tool_rounds`, `history_window`.
   - Tích hợp 4 nút Quick Prompts đại diện cho các kịch bản quan trọng (Research tin tức, kích hoạt làm rõ khi thiếu thông tin `clarify`, tra cứu quy định `policy`, và ranh giới xác nhận an toàn trước khi `send`).
   - Cập nhật `starter_v0/requirements.txt` bổ sung `streamlit>=1.30.0`.

2. **Thiết lập Public Tunnel Demo:**
   - Cài đặt và cấu hình `cloudflared` trên môi trường Windows.
   - Mở tunnel công khai trỏ vào cổng dịch vụ `8501`: `https://exit-jackets-zoo-java.trycloudflare.com`.
   - Kiểm thử truy cập từ mạng ngoài (di động 4G) đảm bảo các team khác và giảng viên mở dùng thử được ngay trong buổi Showdown.

3. **Tài liệu & Báo cáo:**
   - Viết hoàn chỉnh Phần A trong `report/team/group_report.md`: mô tả chức năng, cách chạy UI, link public tunnel, bảng tra cứu 10 tool hiện có và 4 câu hỏi mẫu.
   - Thiết kế poster giới thiệu một trang hiện đại `report/team/poster.html` hiển thị kiến trúc 4 bước của agent, danh mục toolset và các trường hợp thử nghiệm.
   - Thiết kế kịch bản 3 lượt Live Chat chuẩn Rubric C6 phục vụ tạo transcript khi nhóm hoàn thiện prompt `v3`.

## 4. Bằng chứng

- **File code & cấu hình:**
  - `starter_v0/app.py`: Mã nguồn Web UI Streamlit.
  - `starter_v0/requirements.txt`: Bổ sung dependency Streamlit.
  - `report/team/group_report.md`: Biên soạn Mục 1, Mục 2 (Phần A), Mục B5a.
  - `report/team/poster.html`: Mã nguồn poster HTML giới thiệu agent.
  - `TEAM.md`: Cập nhật thông tin phân công nhiệm vụ.
- **Dịch vụ hoạt động:**
  - Link chạy public: `https://exit-jackets-zoo-java.trycloudflare.com`
  - Lệnh chạy local: `cd starter_v0; streamlit run app.py` (cổng 8501).
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - Dùng AI hỗ trợ scaffold giao diện Streamlit, thiết kế layout CSS hiện đại cho poster HTML.
  - Tự kiểm tra bằng cách cài đặt thư viện vào Python environment, chạy khởi động server Streamlit, kiểm tra log uvicorn và mở trực tiếp trên trình duyệt `http://localhost:8501`.
  - Kiểm tra kết nối Cloudflare Tunnel qua mạng ngoài, xác nhận kết nối QUIC/HTTP2 thành công.

## 5. Tự đánh giá

- Hoàn thành đầy đủ và vượt tiến độ các hạng mục được giao thuộc CP5 trước giờ Showdown 16:30.
- Chủ động chuẩn bị trước UI, link tunnel, poster và kịch bản chat để sẵn sàng cho nhóm thử nghiệm ngay khi các bạn phụ trách CP1-CP4 hoàn thành prompt và tool mới.
- Đánh giá: **Hoàn thành tốt (10/10)**.

