# Báo cáo cá nhân — NguyenTungDuong-2A202603850

## 1. Thông tin thành viên

- Họ tên: Nguyễn Tùng Dương
- MSSV: 2A202603850
- Email: nguyenduong342003@gmail.com
- Nhánh làm việc (Branch): `NguyenTungDuong`
- Repository: `https://github.com/nguyenduong43/K5-L3B-DAY03-Nhom456-ResearchAgentToolEval/tree/NguyenTungDuong`
- Vai trò: Team Leader & Prompt/Tool Optimization Engineer (Phụ trách thiết lập môi trường, chạy baseline v0 và tối ưu hóa Prompt & Tool Declaration v1)

## 2. Phần việc phụ trách

- **Thiết lập môi trường và cấu hình:** Chuẩn bị môi trường Python ảo (`.venv`), bổ sung dependency cần thiết (`streamlit>=1.30.0` vào `requirements.txt`), cấu hình `.env` cho provider Google Gemini (`gemini-3.5-flash-lite`).
- **Thực hiện Checkpoint 1 (CP1 — Baseline v0):** Kiểm tra kết nối preflight, chạy bộ test chuẩn `data/eval_base.json` thu thập log baseline v0 chưa chỉnh sửa, phân loại các ca thất bại theo taxonomy lỗi của bài lab.
- **Thực hiện Checkpoint 2 (CP2 — Tối ưu hóa v1):** 
  - Xóa bỏ toàn bộ chỉ dẫn xấu cố ý trong starter prompt (đoán mò thay vì hỏi, gửi không cần xác nhận, ép làm trong 1 bước).
  - Tái cấu trúc `system_prompt.md` với các quy tắc ranh giới an toàn (`clarify` vs `send`), quy tắc định tuyến công cụ (routing rules) và xử lý ngữ cảnh hội thoại nhiều lượt (multi-turn carryover & correction).
  - Viết lại toàn diện `tools.yaml` với mô tả rõ ràng: chức năng, khi nào dùng, khi nào không dùng, và chuẩn hóa quy ước tham số (`screenname` không có `@`, `lookup.query` chỉ chứa từ khóa cốt lõi, `topic=news`, `timeframe`, `search_type=Top|Latest`).
- **Đánh giá kiểm thử và nộp code:** Chạy eval bản `v1` trên model `gemini-3.5-flash-lite`, đạt tỷ lệ thành công tuyệt đối 20/20 test cases (100%), commit và push mã nguồn lên nhánh cá nhân `NguyenTungDuong`.

## 3. Đóng góp cụ thể

1. **Thiết lập môi trường & Chạy Baseline v0 (CP1):**
   - Khởi tạo môi trường ảo, cài đặt đầy đủ các gói thư viện và bổ sung `streamlit` vào `starter_v0/requirements.txt`.
   - Kết nối thành công provider Gemini qua `scripts/preflight_provider.py` với model `gemini-3.5-flash-lite`.
   - Chạy eval baseline `v0` thu được kết quả tại `starter_v0/runs/v0_B_base_gemini_20261110T175614772210.json`: 
     - Tổng số case: 20, passed: 13, failed: 7 (`case_accuracy`: **0.65**).
     - Phân tích nguyên nhân 7 ca thất bại:
       - `R10_missing_handle` & `R11_missing_url`: Do prompt starter xui tự đoán tài khoản Sam Altman / tự bịa URL thay vì gọi `clarify(response_type="text")`.
       - `R12_confirm_before_send`: Do prompt xui tự gửi ngay, agent gọi thẳng `send(confirmed=true)` khi người dùng chưa xác nhận.
       - `R13_parallel_web_and_tweets`: Do prompt ép "Pick one tool", agent chỉ gọi `lookup` mà bỏ sót `social_search`.
       - `R03_web_news_routing`, `M02_carryover_timeframe`, `M06_switch_tool`: Do `tools.yaml` chưa có convention, agent nhồi nhét chữ "news today" / "latest news" vào `query` của `lookup`.

2. **Tối ưu hóa toàn diện Prompt & Tool Declaration (CP2 — v1):**
   - **Xây dựng lại `starter_v0/artifacts/system_prompt.md`:**
     - Xóa bỏ hoàn toàn các chỉ dẫn đoán mò, ép 1 tool, gửi tự do.
     - Quy định chặt chẽ ranh giới an toàn: Thiếu handle/URL bắt buộc gọi `clarify(response_type="text")`; yêu cầu gửi Telegram bắt buộc gọi `clarify(response_type="yes_no")` để xin phép trước, chỉ gọi `send` khi người dùng đã xác nhận ở lượt sau.
     - Bổ sung quy tắc routing rõ ràng cho `timeline`, `social_search`, `lookup`, `fetch`, `policy`, `papers`, `paper_text`.
     - Cho phép gọi song song nhiều tool khi yêu cầu có nhiều nguồn dữ liệu (như case R13).
     - Hướng dẫn xử lý ngữ cảnh đa lượt: giữ nguyên ràng buộc và cập nhật sửa đổi từ lượt người dùng mới nhất.
   - **Chuẩn hóa `starter_v0/artifacts/tools.yaml`:**
     - Viết lại `description` cho toàn bộ các công cụ: nêu rõ mục đích, KHI NÀO DÙNG và KHI NÀO KHÔNG DÙNG.
     - Quy ước cụ thể từng tham số: `screenname` không có `@` kèm bảng ánh xạ tên người nổi tiếng (`sama`, `elonmusk`, `karpathy`); `lookup.query` chỉ chứa từ khóa chủ đề cốt lõi (ví dụ `"AI"`, `"robotics"`), không lặp lại các từ khóa thời gian; `search_type` nhận `Top` hoặc `Latest`.
     - Quy định boundary cho `send`: chỉ truyền `confirmed=true` sau khi người dùng đã đồng ý.

3. **Kiểm thử thực nghiệm và ghi nhận kết quả v1:**
   - Chạy eval bản `v1` trên model `gemini-3.5-flash-lite`:
     ```bash
     python run_eval.py --provider gemini --model gemini-3.5-flash-lite --version v1 --suite base --eval-cases data/eval_base.json
     ```
   - Kết quả xuất ra tại `starter_v0/runs/v1_B_base_gemini_20261110T184407163680.json`:
     - **Passed: 20/20 cases (100% pass)**
     - `case_accuracy`: **1.00** (tăng từ 0.65 lên 1.00)
     - `tool_routing_accuracy`: **1.00**
     - `argument_accuracy`: **1.00**
     - `multiturn_accuracy`: **1.00**
     - Sửa triệt để toàn bộ 7 lỗi của bản v0.

4. **Quản lý phiên bản Git:**
   - Commit toàn bộ kết quả lên branch cá nhân: `3cbf2df feat: complete CP1 baseline v0 and optimize prompt and tools v1`.
   - Push branch `NguyenTungDuong` lên GitHub repository nhóm.

## 4. Bằng chứng

- **Branch làm việc:** `NguyenTungDuong` trên repo `https://github.com/nguyenduong43/K5-L3B-DAY03-Nhom456-ResearchAgentToolEval`
- **Commit chính:**
  - Commit ID: `3cbf2dfedf17fa876198da9906a878bd8434d01f`
  - Message: `feat: complete CP1 baseline v0 and optimize prompt and tools v1`
  - Tác giả: `Nguyen Tung Duong <nguyenduong342003@gmail.com>`
- **Các file đã thực hiện chỉnh sửa / tạo mới trong commit:**
  - `starter_v0/artifacts/system_prompt.md` (tái cấu trúc toàn bộ prompt)
  - `starter_v0/artifacts/tools.yaml` (chuẩn hóa mô tả và convention tham số)
  - `starter_v0/requirements.txt` (bổ sung streamlit)
  - `starter_v0/.env.example`
  - `starter_v0/runs/v0_B_base_gemini_20261110T175614772210.json` (log baseline v0: 0.65)
  - `starter_v0/runs/v1_B_base_gemini_20261110T184407163680.json` (log kết quả v1: 1.00)
- **Công cụ đã dùng và cách tự kiểm tra:**
  - Sử dụng Python 3.15, thư viện `google-genai` kết nối Google Gemini API.
  - Sử dụng công cụ AI hỗ trợ phân tích định dạng JSON schema và cấu trúc prompt theo phương pháp Evidence-Driven.
  - Tự kiểm chứng bằng cách chạy thực tế test harness `run_eval.py` trên 20 test case độc lập, đảm bảo `provider_error_cases == 0` và đạt điểm số 20/20.

## 5. Tự đánh giá

- **Mức độ hoàn thành:** 100% phần việc phụ trách, đạt kết quả tối đa ngay ở bản tối ưu v1 (20/20 test cases pass, `case_accuracy` đạt 1.00).
- **Phương pháp làm việc:** Bám sát phương pháp tiếp cận khoa học dựa trên bằng chứng (evidence-driven): bóc tách từng case FAIL ở bản v0 để tìm gốc rễ vấn đề, sau đó sửa đúng trọng tâm vào `system_prompt.md` và `tools.yaml`.
- **Kỹ năng đạt được:** Làm chủ kỹ thuật Prompt Engineering và Tool Declaration cho LLM, hiểu sâu cơ chế Function Calling của Gemini, biết cách thiết lập Guardrails an toàn trước các hành vi có tác dụng phụ (side-effects).
