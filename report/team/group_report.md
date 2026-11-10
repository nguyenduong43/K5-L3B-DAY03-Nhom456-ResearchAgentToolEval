# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3:

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
| timeline | lấy bài đăng gần đây của tài khoản Twitter/X | không |
| social_search | tìm kiếm bài đăng theo từ khóa | không |
| lookup | tra cứu tin tức/thông tin trên internet | không |
| fetch | đọc nội dung bài viết từ một URL cụ thể | không |
| format | trình bày các item thành bản tin markdown | không |
| send | gửi bản tin lên Telegram khi đã xác nhận | không |
| policy | tra cứu chính sách công ty nội bộ | không |
| papers | tìm paper học thuật trên arXiv | không |
| paper_text | tải và đọc nội dung PDF của arXiv paper | không |
| source_check | đánh giá độ tin cậy của URL/domain và kiểm tra tính khả dụng | có |
| text_stats | thống kê số từ, ký tự, thời gian đọc và trích xuất top từ khóa | có |
| filter_items | khử trùng lặp (dedup), lọc danh sách item theo từ khóa hoặc loại trừ domain | có |
| sentiment_analysis | phân tích sắc thái cảm xúc (tích cực/tiêu cực/trung lập) và điểm polarity | có |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi của prompt/tools starter chưa sửa | — | 0.70 | `runs/v0_B_base_gemini_20261110T173451886731.json` |
| v1 | `system_prompt.md` | Lỗi R08/R10/R11/R12/R13 do prompt khuyến khích đoán, gửi không xác nhận, ép một tool → bỏ các chỉ dẫn đó sẽ sửa được | 0.70 | 0.65 | `runs/v1_B_base_gemini_20261110T180027611008.json` |
| v2 | `system_prompt.md` | Prompt v1 thiếu rule chọn tool → model hỏi account thừa cho tweet theo chủ đề, gọi `policy` thừa; thêm routing rule rõ ràng sẽ sửa R02/R06/R07/R12/R13 | 0.65 | 0.75 | `runs/v2_B_base_gemini_20261110T180610493163.json` |
| v3 | `tools.yaml` | Lỗi còn lại ở v2 đều là lỗi argument (tên người → handle, query thừa chữ) do `tools.yaml` không mô tả convention; ghi rõ convention sẽ sửa R01/R05/R03/R13/M02 | 0.75 | 1.00 | `runs/v3_B_base_gemini_20261110T181259488297.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

Run v0: `starter_v0/runs/v0_B_base_gemini_20261110T173451886731.json` (gemini-3.8-flash, 14/20 pass, `case_accuracy` 0.70, `provider_error_cases` 0).

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | `wrong_arg_value` | `lookup(query="AI news today", topic="news", timeframe="day")` | `query: expected 'AI', got 'AI news today'` — model nhồi "news today" vào query dù `topic`/`timeframe` đã thể hiện | `tools.yaml`: description `lookup` ghi rõ `query` chỉ chứa chủ đề cốt lõi; thời gian/loại tin dùng `timeframe`/`topic` |
| R08_out_of_scope | `out_of_scope` | `lookup(query="nguyên hàm của x^2")` | `expected no tool call` — câu toán ngoài phạm vi research nhưng agent vẫn gọi tool | `system_prompt.md`: khai báo phạm vi research; yêu cầu ngoài phạm vi thì từ chối, không gọi tool |
| R10_missing_handle | `missing_info` | `timeline(screenname="sama", limit=5)` | `missing tool call clarify`, `extra tool call timeline` — tự đoán account Sam Altman | `system_prompt.md`: bỏ chỉ dẫn "pick a well-known account"; thiếu handle thì gọi `clarify(response_type="text")` |
| R11_missing_url | `missing_info` | `fetch(url="https://blog.samaltman.com/the-intelligence-age")` | `missing tool call clarify`, `extra tool call fetch` — bịa URL cho "bài viết này" | `system_prompt.md`: bỏ chỉ dẫn "assume a likely URL"; thiếu URL thì gọi `clarify(response_type="text")` |
| R12_confirm_before_send | `wrong_boundary` | `send(confirmed=true, text="📢 BẢN TIN CÔNG NGHỆ & AI…")` | `missing tool call clarify`, `extra tool call send` — tự bịa nội dung bản tin và tự đặt `confirmed=true` (nghiêm trọng nhất) | `system_prompt.md`: bỏ "just go ahead and do it"; trước khi gửi phải `clarify(response_type="yes_no")`. `tools.yaml`: `send` chỉ `confirmed=true` sau khi user xác nhận |
| R13_parallel_web_and_tweets | `wrong_tool` | `lookup(query="tin tức AI hôm nay", topic="news", timeframe="day")` | `missing tool call social_search`; `query: expected 'AI', got 'tin tức AI hôm nay'` — chỉ gọi 1 tool | `system_prompt.md`: bỏ "Pick one tool / single step", cho phép gọi nhiều tool khi yêu cầu có nhiều phần; query xử lý như R03 |

Nhận xét: 5/6 lỗi (R08, R10, R11, R12, R13) bắt nguồn trực tiếp từ chỉ dẫn xấu trong `system_prompt.md` của starter (đoán thay vì hỏi, gửi không cần xác nhận, ép một bước). R03 là lỗi convention argument, thuộc `tools.yaml`.

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
| Tool mới (`tools/`) | `starter_v0/tools/` (`source_check`, `text_stats`, `filter_items`, `sentiment_analysis`) | Xây dựng 4 tool chuyên sâu cho Research Agent: kiểm tra độ tin cậy nguồn, thống kê văn bản, khử trùng lặp danh sách item, phân tích cảm xúc dư luận. | Bắt buộc kiểm tra kiểu dữ liệu đầu vào; bọc try/catch toàn bộ để luôn trả về error dict khi gặp lỗi. |
| Unit test tool mới (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` | 12/12 test pass (mỗi tool 3 test: happy path, bad input, failure/edge cases). `pytest` suite đạt 94 passed, 0 failed. | Sử dụng `fake_http` mock offline, không gọi mạng thật và không rò rỉ key. |
| UI (lệnh chạy + link dùng thử) |  |  |  |

**Tool unit tests:**
- Số test đã viết: 12 tests bao phủ 4 tool mới:
  - `source_check`: `test_source_check_happy_path_trusted_domain`, `test_source_check_bad_or_missing_input_returns_error_dict`, `test_source_check_network_failure_returns_error_dict`.
  - `text_stats`: `test_text_stats_happy_path`, `test_text_stats_bad_input_returns_error_dict`, `test_text_stats_edge_case_only_punctuation_and_large_top_k`.
  - `filter_items`: `test_filter_items_happy_path_deduplication`, `test_filter_items_bad_input_returns_error_dict`, `test_filter_items_by_keyword_and_exclude_domain`.
  - `sentiment_analysis`: `test_sentiment_analysis_happy_path_positive`, `test_sentiment_analysis_happy_path_negative`, `test_sentiment_analysis_bad_input_returns_error_dict`.
- Ví dụ lỗi mà unit test bắt được nhưng eval không bắt được: Eval chỉ kiểm tra model có gọi đúng `tool_name` và `args` hay không (ví dụ model gọi đúng `source_check(url="...")` thì eval vẫn chấm PASS). Nhưng nếu phía tool code bị lỗi mạng (`ConnectionError`) hoặc nhận URL rỗng mà code lại `raise` exception thay vì trả về dictionary `{"error": ...}` thì agent sẽ bị crash runtime. Tương tự với `filter_items` khi model truyền `items=None` hoặc `items="string"`, unit test đảm bảo code trả về error dict mà không crash agent.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) | `starter_v0/tools/` (`source_check`, `text_stats`, `filter_items`, `sentiment_analysis`) | Viết 4 tool mới hoàn chỉnh, mỗi tool có `tool.py`, `TOOL.md`, đăng ký trong `tools/__init__.py` và `tools.yaml`, kèm 12 unit tests đạt 100% pass | Tất cả tool đều xử lý phòng thủ lỗi, kiểm tra input biên, không crash |
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
