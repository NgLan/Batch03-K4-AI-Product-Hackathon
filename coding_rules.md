# Quy tắc phát triển & Kiến trúc Code (TA Co-pilot)

Tài liệu này lưu trữ các quy tắc kiến trúc và tiêu chuẩn viết mã nguồn bắt buộc cho toàn bộ dự án, đồng thời tự kiểm tra mức độ tuân thủ của các file hiện tại.

---

## 1. Các quy tắc bắt buộc tuân thủ

1. **Clean Code & SRP (Single Responsibility Principle):**
   * Mỗi file và mỗi hàm chỉ làm đúng 1 nhiệm vụ duy nhất.
   * Chia nhỏ logic xử lý phức tạp thành các hàm trợ giúp (helpers) hoặc dịch vụ riêng lẻ (services).

2. **Giới hạn độ dài:**
   * Một file **KHÔNG QUÁ 100 dòng** code.
   * Một hàm **KHÔNG QUÁ 20 dòng** code (tính cả chữ ký hàm và docstring nếu gộp chung dòng).

3. **Không vi phạm DRY (Don't Repeat Yourself):**
   * Tái sử dụng các đoạn logic trùng lặp (ví dụ: hàm định dạng thời gian, hàm parse JSON).

4. **Type Hints & Docstrings:**
   * Mọi hàm đều phải có chú thích kiểu dữ liệu truyền vào/trả về (`type hints`).
   * Viết tài liệu giải thích (`docstring`) bằng tiếng Việt ngắn gọn, súc tích và dễ hiểu.

---

## 2. Thống kê mức độ tuân thủ của Dự án

Dưới đây là bảng tự đánh giá của toàn bộ các file nguồn trong thư mục [codebase/](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase):

| Tên file nguồn | Nhiệm vụ chính (SRP) | Tổng số dòng | Hàm dài nhất (Dòng) | Tình trạng tuân thủ |
|---|---|---|---|---|
| [main.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/main.py) | Khởi chạy Bot Discord, xử lý lệnh Slash với cache và View. | ~90 dòng | `process_messages_and_send` (13 dòng) | **Đạt** |
| [discord_fetcher.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/discord_fetcher.py) | Kéo lịch sử tin nhắn của các kênh cấu hình để test. | ~51 dòng | `process_channel` (19 dòng) | **Đạt** |
| [main_pipeline.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/main_pipeline.py) | Kết hợp và lọc các tin nhắn đã được giải quyết thủ công. | ~42 dòng | `filter_resolved_from_results` (16 dòng) | **Đạt** |
| [services/discord_service.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/services/discord_service.py) | Truy xuất và chuyển đổi cấu trúc tin nhắn Discord. | ~76 dòng | `transform_message` (12 dòng) | **Đạt** |
| [services/llm_client.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/services/llm_client.py) | Quản lý kết nối và gửi yêu cầu tới Google GenAI API. | ~39 dòng | `get_genai_client` (9 dòng) | **Đạt** |
| [services/unanswered_service.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/services/unanswered_service.py) | Lọc các tin nhắn chưa được trả lời của học viên. | ~40 dòng | `filter_unanswered_messages` (16 dòng) | **Đạt** |
| [services/clustering_service.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/services/clustering_service.py) | Gom nhóm câu hỏi bằng Gemini LLM và làm sạch dữ liệu. | ~61 dòng | `clean_json_text` (18 dòng) | **Đạt** |
| [services/resolve_service.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/services/resolve_service.py) | Lưu trữ và đọc ID các tin nhắn đã đánh dấu giải quyết thủ công. | ~38 dòng | `save_resolved_id` (11 dòng) | **Đạt** |
| [services/cache_service.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/services/cache_service.py) | Caching kết quả phân tích trong vòng 10 phút để giảm token. | ~45 dòng | `get_cached_analysis` (19 dòng) | **Đạt** |
| [services/ui_service.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/services/ui_service.py) | Phân trang tương tác và nút "Mark as Resolved" của Bot. | ~95 dòng | `resolve_button` (14 dòng) | **Đạt** |
| [prompts/clustering_prompt.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/prompts/clustering_prompt.py) | Lưu trữ System Prompt định dạng XML bảo mật cho LLM. | ~44 dòng | Không chứa hàm | **Đạt** |
| [run_pipeline_example.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/codebase/run_pipeline_example.py) | Script kiểm thử tích hợp (Integration Test) dữ liệu giả lập. | ~94 dòng | `create_mock_messages` (16 dòng) | **Đạt** |
| [eval/run_eval.py](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/eval/run_eval.py) | Script đánh giá tự động (Evaluation Run) cho Checkpoint 3. | ~67 dòng | `verify_match` (18 dòng) | **Đạt** |
