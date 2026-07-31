# Phản hồi Cá nhân (Reflection) - Nguyễn Ngọc Lan (2A202601384)

## 1. Vai trò và Công việc đã làm
Trong dự án **TA Co-pilot**, tôi đảm nhận vai trò **Phân tích dữ liệu & Prompt Engineering**. Các công việc cụ thể tôi đã hoàn thành bao gồm:
*   Thiết kế System Prompt XML cô lập dữ liệu đầu vào tại `codebase/prompts/clustering_prompt.py` để hướng dẫn Gemini 3.5 Flash gom cụm câu hỏi của học viên và đề xuất nội dung recap.
*   Viết hàm xử lý logic LLM tại `codebase/services/clustering_service.py`, đóng gói dữ liệu học viên thành thẻ XML để chống Prompt Injection và làm sạch đầu ra JSON từ model.
*   Xây dựng bộ kiểm thử tự động (Evaluation System) gồm file dữ liệu Golden Set `eval/dataset.json` (20 cases phủ đủ các lớp lỗi khó) và script tự động đánh giá `eval/run_eval.py` để chấm điểm độ chính xác của AI.

## 2. Cách AI hỗ trợ trong quá trình làm việc
AI đã hỗ trợ tôi rất nhiều để tăng tốc độ phát triển sản phẩm:
*   **Sinh dữ liệu kiểm thử (Golden Set):** Tôi đã dùng AI để sinh nhanh các câu hỏi giả lập (tiếng lóng, viết tắt, không dấu) dựa trên mẫu chatlog thật để phủ đủ 4 lớp chỗ khó (ambiguous, forbidden, out-of-scope, high-risk).
*   **Thiết kế Prompt bảo mật:** AI đã gợi ý cho tôi phương pháp đóng gói dữ liệu học viên trong thẻ XML `<student_messages>` để ngăn chặn các đòn tấn công Prompt Injection từ học viên nghịch ngợm.
*   **Viết hàm bổ trợ:** Hỗ trợ viết nhanh các hàm regex lọc ký tự thừa trong chuỗi JSON trả về từ LLM (`clean_json_text`).

## 3. Bài học kinh nghiệm từ trường hợp thất bại của nhóm
Bài học lớn nhất của tôi đến từ **Câu hỏi số 6 trong lượt chạy kiểm thử đầu tiên** (về lỗi biến môi trường `.env` nhưng bị AI xếp vào lỗi cài đặt thư viện). 
*   **Vấn đề:** Mong muốn của nhóm là xếp vào chủ đề *"Lỗi cấu hình file .env"*, nhưng AI thực tế phân loại vào *"Lỗi cài đặt thư viện và cấu hình biến môi trường (.env)"*. Về mặt ngữ nghĩa, câu trả lời này hoàn toàn chấp nhận được và giúp ích cho TA, nhưng bộ code đối sánh từ khóa cứng nhắc của tôi lại đánh dấu case này là **Fail**.
*   **Bài học:** Kiểm thử chất lượng AI (Eval) không nên phụ thuộc hoàn toàn vào so khớp từ khóa thô sơ (exact keyword matching) vì ngôn ngữ tự nhiên rất phong phú. Trong các dự án tiếp theo, tôi sẽ áp dụng phương pháp **LLM-as-a-judge** (dùng một LLM khác để chấm điểm tương đồng ngữ nghĩa) để kết quả eval khách quan và thực tế hơn. Đồng thời, việc chốt Quality Bar (80%) trước khi chạy test giúp nhóm giữ được tính trung thực, không cố gắng tinh chỉnh prompt một cách mù quáng chỉ để đạt điểm số đẹp mắt trên giấy tờ.
