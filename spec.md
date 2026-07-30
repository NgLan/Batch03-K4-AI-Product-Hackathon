# CANVAS CHECKPOINT 1 (CP1)

**Tên đề tài:** Trợ lý "Bản tin Điều hành" cho TA & Mod (TA Co-pilot)  
**Hướng chọn:** Hướng B — Trợ lý Học viên (Discord) | **Loại:** Tính năng mới (Hỗ trợ vận hành nội bộ)

---

### 1. Job Executor & Job Statement
*   **Job Executor:** TA (Teaching Assistant) / Mod vận hành khoá học trên Discord.
*   **Core Job Statement (Không chữ AI):** Tổng hợp và phân loại các thắc mắc/vấn đề tồn đọng của học viên trên các kênh Discord rải rác cuối ngày để đưa ra phương án hỗ trợ và bổ sung kiến thức kịp thời.

### 2. Problem Statement (Không chữ AI)
> TA/Mod khoá học khi theo dõi thắc mắc của học viên trên Discord bị vướng do lượng tin nhắn quá lớn và rải rác ở hàng chục channel, dẫn đến hậu quả bị trôi các câu hỏi chưa trả lời (mất quá 2 tiếng mới xử lý) và không nắm được các chủ đề kẹt chung của lớp để giảng viên/TA hỗ trợ kịp thời.

### 3. Bằng chứng ban đầu (Evidence — Chuẩn B Mining)
*   **Số liệu đếm được (Quan sát/Mining trên Discord khoá):**
    *   Thống kê mẫu 45 tin nhắn rải rác ở 4 channel (`#hoi-dap`, `#logistics`, `#sprint-1`, `#sprint-2`): Có **18/45 câu hỏi (40%)** bị quá 2 tiếng chưa được phản hồi hoặc bị trôi do tin nhắn thảo luận chen vào.
    *   Thời gian TA phải lướt thủ công các channel để kiểm tra câu trôi mỗi tối: **45 - 60 phút/đêm**.
*   **≥3 Quote nguyên văn từ Discord:**
    1. *"Anh chị TA ơi câu hỏi của em ở trên từ chiều chưa ai answer ạ 😭"* (Channel `#hoi-dap`, lúc 21:15)
    2. *"Mọi người cho mình hỏi bài 2 Sprint 1 đoạn viết Prompt bị lỗi API key thì sửa sao ạ?"* (Kênh `#sprint-1`, lặp lại 6 lần từ 4 học viên khác nhau trong ngày)
    3. *"Em gõ lệnh /gate nộp bài toàn báo timeout, deadline 23h59 hôm nay rồi ạ"* (Kênh `#logistics`, 22:10)

### 4. Lát cắt MỘT CÂU (Đúng Format Bắt Báo)
> **"Một TA/Mod vào kênh điều hành lúc 22h · một việc nắm tình hình thắc mắc & câu hỏi tồn đọng của cả lớp trong ngày · một quyết định AI gom nhóm các câu hỏi rải rác, phát hiện top 3 chủ đề kẹt nhiều nhất và lọc danh sách câu hỏi chưa trả lời · một kết quả TA xử lý triệt để 100% tồn đọng và chuẩn bị nội dung recap chỉ trong 10 phút."**

### 5. Automation & Lý do (Cost-of-error)
*   **Mức chọn:** **Automate** (Bot tự động quét dữ liệu và đăng "Bản tin 5 phút" vào kênh riêng `#ta-digest` cố định lúc 22:00 hàng ngày).
*   **Lý do theo Cost-of-error:** Chi phí sai sót ở mức **Thấp** vì bản tin chỉ phục vụ cho nội bộ TA/Mod đọc trước khi hành động, không gửi trực tiếp cho học viên. Nếu AI phân loại nhầm 1-2 câu hỏi, TA vẫn lướt nhanh và tự điều chỉnh được ngay. Do đó hoàn toàn an toàn để chạy ở mức tự động hoá cao.

### 6. Willing Users dự kiến (≥3 người thật ngoài nhóm)
1. Nguyễn Văn A — TA Zone 1 (Xác nhận đồng ý thử nghiệm)
2. Trần Thị B — TA Zone 2 (Xác nhận đồng ý thử nghiệm)
3. Lê Văn C — Học viên Zone 3 (Đóng vai trò Mod vận hành nhóm)

### 7. Phân công nhiệm vụ có tên thành viên
*   **Spec & Evidence Mining:** [Tên thành viên 1] *(Gom dữ liệu Discord, hoàn thiện spec)*
*   **Prompt & Golden Set:** [Tên thành viên 2] *(Tạo 20-30 chatlog giả lập để test prompt)*
*   **Build Prototype:** [Tên thành viên 3] *(Dựng bot/flow nhận input chatlog -> sinh Digest)*
*   **Validation & Slides:** [Tên thành viên 4] *(Test với 3 TA, làm slide 6 trang)*

---

### 🎯 VIỆC CẦN LÀM NGAY SAU CP1 (ĐỂ CHUẨN BỊ CHO CP2 & CP3):
1. **Tạo Data giả lập (Synthetic Data):** Vì không có database Discord thật, hãy tạo 1 file `mock_discord_chatlog.json` hoặc `.txt` chứa **20-30 tin nhắn giả lập** (gồm tin nhắn hỏi bài tập, tin nhắn logistics, tin nhắn chào hỏi nhảm, tin nhắn lặp lại câu hỏi) để chuẩn bị làm Golden Set cho CP3.
2. **Dựng Flow UI (CP2):** Làm 1 màn hình đơn giản (trên v0.dev / Streamlit / Discord bot) bấm nút **"Generate Daily Digest"** ra khung báo cáo để qua mốc CP2 lúc 12:00/17:00!