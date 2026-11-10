# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: Nhom456
- Lớp: L3B
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: Gemini (gemini-2.5-flash) / OpenRouter

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research Agent hỗ trợ tự động hóa chu trình nghiên cứu công nghệ: tìm kiếm bài báo khoa học (arXiv) và tin tức mạng xã hội/web (Twitter/X, Tavily), đọc nội dung bài viết/URL (Firecrawl), tra cứu chính sách công ty (Policy RAG), định dạng báo cáo tổng hợp (digest), và chỉ thực hiện hành động gửi đi (Telegram) sau khi người dùng đã xác nhận rõ ràng.

**Cách chạy UI:**

1. Cài đặt thư viện: `pip install -r starter_v0/requirements.txt`
2. Chạy ứng dụng web:
```bash
cd starter_v0
streamlit run app.py
```

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL: https://exit-jackets-zoo-java.trycloudflare.com

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| `clarify` | Hỏi lại người dùng khi thiếu thông tin hoặc yêu cầu mơ hồ | không |
| `timeline` | Lấy các bài đăng gần đây của một tài khoản Twitter/X cụ thể theo handle | không |
| `social_search` | Tìm kiếm bài viết/tin tức trên mạng xã hội (Twitter/X) theo từ khóa | không |
| `lookup` | Tra cứu thông tin trên internet qua Tavily (hỗ trợ phân loại news/general) | không |
| `fetch` | Trích xuất nội dung văn bản sạch từ một địa chỉ URL trang web qua Firecrawl | không |
| `format` | Định dạng danh sách các tin/nguồn tìm được thành bản tin digest theo khuôn mẫu | không |
| `send` | Gửi tin nhắn đến kênh Telegram (chỉ kích hoạt khi user đã xác nhận) | không |
| `policy` | Tra cứu quy định nội bộ công ty (sử dụng AI, bản quyền, trích dẫn nguồn) | không |
| `papers` | Tìm kiếm các bài báo khoa học trên arXiv theo từ khóa | không |
| `paper_text` | Trích xuất toàn văn nội dung tài liệu PDF/bài báo arXiv | không |
| *(Tool mới CP3)* | *(Đang cập nhật bởi thành viên phụ trách CP3)* | Có |

### A3. Câu hỏi mẫu để thử

1. **Research tin tức công nghệ (Gọi tool `social_search` hoặc `lookup`):**
   > *"Tìm các bài đăng và tin tức mới nhất về DeepSeek-V3 trên mạng xã hội hôm nay."*
2. **Yêu cầu thiếu thông tin (Trigger hành vi làm rõ `clarify`):**
   > *"Hãy tóm tắt và phân tích bài báo này giúp tôi."* *(Quan sát agent sẽ hỏi lại bài báo nào / xin URL/ID thay vì bịa)*
3. **Tra cứu quy định nội bộ (Gọi tool `policy`):**
   > *"Công ty có quy định gì về việc sử dụng AI trong nghiên cứu và bảo mật dữ liệu không?"*
4. **Hành động nhạy cảm cần xác nhận (Kiểm tra boundary của `send`):**
   > *"Gửi bản tin tổng hợp vừa rồi lên kênh Telegram thông báo của nhóm."* *(Quan sát agent phải hỏi xin xác nhận chứ không gửi ngay)*

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`, link `https://exit-jackets-zoo-java.trycloudflare.com` | Streamlit chat tương tác mượt mà, trực quan hóa tool call log, tự động ghi transcript | Link Cloudflare tunnel phụ thuộc phiên terminal; cần giữ tiến trình chạy trong buổi showdown |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
