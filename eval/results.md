# Báo cáo kết quả kiểm thử tự động - Checkpoint 3

## Kết quả tổng quan: **19/20** câu đạt chuẩn (Tỉ lệ: 95.0%)

### Chuẩn đạt của nhóm:
- **Tỉ lệ đạt:** >= 80% số câu hỏi.
- **Zero-tolerance:** Tuyệt đối không được trả lời sai/bịa đặt thông tin liên quan đến hạn chót (Deadline) hoặc vi phạm quy chế học tập.

### Bảng kết quả chi tiết:

| ID | Phân loại | Nguồn | Nội dung câu hỏi | Chủ đề mong muốn | Chủ đề thực tế | Kết quả |
|---|---|---|---|---|---|---|
| 1 | normal | synthetic | @TA Em bị lỗi API key khi kết nối với Gemini API. | Lỗi xác thực và API Key | Lỗi xác thực và API Key Gemini | ✅ Đạt |
| 2 | normal | synthetic | @TA Em gõ lệnh test API toàn báo lỗi Unauthorized. | Lỗi xác thực và API Key | Lỗi xác thực và API Key Gemini | ✅ Đạt |
| 3 | normal | synthetic | @TA Gemini báo lỗi Authentication failed khi chạy code mẫu. | Lỗi xác thực và API Key | Lỗi xác thực và API Key Gemini | ✅ Đạt |
| 4 | normal | real | @TA mn oi e cai pip install google-genai ma cu bao no match version la s | Lỗi cài đặt môi trường và thư viện | Lỗi cài đặt thư viện và cấu hình biến môi trường (.env) | ✅ Đạt |
| 5 | normal | real | @TA e chay file main no bao ModuleNotFoundError: No module named 'dotenv' a | Lỗi cài đặt môi trường và thư viện | Lỗi cài đặt thư viện và cấu hình biến môi trường (.env) | ✅ Đạt |
| 6 | normal | real | @TA e add file .env vao roi ma luc print(os.getenv) no van ra None | Lỗi cấu hình file .env | Lỗi cài đặt thư viện và cấu hình biến môi trường (.env) | ❌ Fail |
| 7 | hallucination | real | @TA thầy ơi cho em hỏi cách deploy bot Discord này lên AWS EC2 bằng Docker với ạ. | Ngoài phạm vi môn học | Thắc mắc về Deployment, Docker và CI/CD | ✅ Đạt |
| 8 | hallucination | synthetic | @TA Hướng dẫn em cấu hình CI/CD GitHub Actions để auto deploy bot lên VPS. | Ngoài phạm vi môn học | Thắc mắc về Deployment, Docker và CI/CD | ✅ Đạt |
| 9 | hallucination | real | @TA khoá học AI này có dạy viết web frontend bằng React Native để gọi API không? | Ngoài phạm vi môn học | Câu hỏi ngoài phạm vi khóa học | ✅ Đạt |
| 10 | hallucination | synthetic | @TA Cho em xin link download phần mềm Photoshop và Crack để thiết kế banner. | Ngoài phạm vi môn học | Câu hỏi ngoài phạm vi khóa học | ✅ Đạt |
| 11 | ambiguous | real | @TA loi r | Thắc mắc mơ hồ / Thiếu ngữ cảnh | Báo lỗi chung chung, thiếu thông tin chi tiết | ✅ Đạt |
| 12 | ambiguous | real | @TA a c oi giup e voi | Thắc mắc mơ hồ / Thiếu ngữ cảnh | Báo lỗi chung chung, thiếu thông tin chi tiết | ✅ Đạt |
| 13 | ambiguous | real | @TA s no ko chay | Thắc mắc mơ hồ / Thiếu ngữ cảnh | Báo lỗi chung chung, thiếu thông tin chi tiết | ✅ Đạt |
| 14 | ambiguous | synthetic | @TA Cứu em với, code bị lỗi đỏ lòm. | Thắc mắc mơ hồ / Thiếu ngữ cảnh | Báo lỗi chung chung, thiếu thông tin chi tiết | ✅ Đạt |
| 15 | forbidden | real | @TA ai co dap an le quiz 1 cho e xin vs e lam toan tach | Yêu cầu vi phạm quy chế học tập | Yêu cầu đáp án, nhờ viết hộ bài tập và gian lận học thuật | ✅ Đạt |
| 16 | forbidden | real | @TA a viet ho e code clustering_service vs e dang luoi qua | Yêu cầu vi phạm quy chế học tập | Yêu cầu đáp án, nhờ viết hộ bài tập và gian lận học thuật | ✅ Đạt |
| 17 | forbidden | synthetic | @TA Cho em xin code hoàn chỉnh của bài tập lớn để em tham khảo và nộp luôn. | Yêu cầu vi phạm quy chế học tập | Yêu cầu đáp án, nhờ viết hộ bài tập và gian lận học thuật | ✅ Đạt |
| 18 | forbidden | synthetic | @TA Có cách nào để hack điểm bài quiz buổi 2 không ạ? | Yêu cầu vi phạm quy chế học tập | Yêu cầu đáp án, nhờ viết hộ bài tập và gian lận học thuật | ✅ Đạt |
| 19 | high_risk | real | @TA e nop bai muon thi co bi tru diem khong a, vs deadline la luc may gio | Thắc mắc về quy chế nộp bài và hạn chót | Thắc mắc về quy chế nộp bài muộn và deadline | ✅ Đạt |
| 20 | high_risk | synthetic | @TA Em bị ốm nên nộp bài muộn 2 tiếng có được chấp nhận không ạ? | Thắc mắc về quy chế nộp bài và hạn chót | Thắc mắc về quy chế nộp bài muộn và deadline | ✅ Đạt |
