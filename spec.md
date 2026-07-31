# Template AI Spec *(spec.md — commit trước 23:59 N1 · quality bar chốt từ thời điểm nộp)*

> Cấu trúc phủ đúng "SPEC 8 phần" của chương trình: Bằng chứng (§1-§2) · Lát cắt (§4) · Canvas (đính kèm CP1) · Augment/Automate (§4) · 4 đường đi của trải nghiệm (§6) · Kiểu lỗi (§5) · Kiểm thử (§7) · Phân công (§8). Hướng dẫn viết từng mục: `02-guide.md`.

```markdown
# AI SPEC — Trợ lý "Bản tin Điều hành" cho TA & Mod (TA Co-pilot) · Nhóm LDG · Zone 9
Hướng: [ ] A — VLearn  [X] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [X] Tính năng mới

## §1. User & Job
- **Job executor + workflow:** 
  - *Job Executor:* TA (Teaching Assistant) / Mod vận hành khoá học trên Discord.
  - *Workflow:* Cuối ngày (21h-22h) → Mở Discord lướt các channel `#hoi-dap`, `#logistics`, `#sprint-1`... để tìm câu hỏi trôi → Tổng hợp lại các vấn đề học viên gặp nhiều nhất → Trả lời từng câu & báo lại Giảng viên nội dung cần Recap.
- **Core JTBD (không tên sản phẩm/AI trong câu):** Tổng hợp và phân loại các thắc mắc/vấn đề tồn đọng của học viên trên các kênh Discord rải rác cuối ngày để đưa ra phương án hỗ trợ và bổ sung kiến thức kịp thời.
- **Problem statement (KHÔNG chữ AI):** TA/Mod khoá học khi theo dõi thắc mắc của học viên trên Discord bị vướng do lượng tin nhắn quá lớn và rải rác ở hàng chục channel, dẫn đến hậu quả bị trôi các câu hỏi chưa trả lời (mất quá 2 tiếng mới xử lý) và không nắm được các chủ đề kẹt chung của lớp để giảng viên/TA hỗ trợ kịp thời.
- **Evidence (chuẩn B mining):**
  - **Số liệu mining:** Thống kê mẫu 45 tin nhắn rải rác ở 4 channel (`#hoi-dap`, `#logistics`, `#sprint-1`, `#sprint-2`): Có **18/45 câu hỏi (40%)** bị quá 2 tiếng chưa được phản hồi hoặc bị trôi do tin nhắn thảo luận chen vào. Thời gian TA phải lướt thủ công các channel: **45 - 60 phút/đêm**.
  - **Quote/Ví dụ nguyên văn:**
    1. *"Anh chị TA ơi câu hỏi của em ở trên từ chiều chưa ai answer ạ 😭"* (Kênh `#hoi-dap`, lúc 21:15)
    2. *"Mọi người cho mình hỏi bài 2 Sprint 1 đoạn viết Prompt bị lỗi API key thì sửa sao ạ?"* (Kênh `#sprint-1`, lặp lại 6 lần từ 4 học viên khác nhau)
    3. *"Em gõ lệnh /gate nộp bài toàn báo timeout, deadline 23h59 hôm nay rồi ạ"* (Kênh `#logistics`, lúc 22:10)

## §2. Impact & quyết định chọn
- **Bảng impact 3 ứng viên:**
  | Ứng viên tính năng | Bao nhiêu người gặp | Tần suất | Tốn gì mỗi lần | Bằng chứng | Khả thi build | Chọn? |
  |---|---|---|---|---|---|---|
  | **1. Bản tin Điều hành cho TA/Mod (TA Co-pilot)** | ~10 TA/Mod khoá | Mỗi ngày / 1 lần | 45-60 phút lướt thủ công, trôi 40% câu hỏi | Mining 18/45 tin trôi trên Discord | Cao (chỉ cần input chatlog) | **CHỌN** |
  | **2. Bot tự động trả lời bài tập cho học viên** | ~1.000 học viên | 3-5 lần/ngày | Chờ TA lâu, dễ nhận câu trả lời đoán mò | Khảo sát nhu cầu học viên | Trung bình (Rủi ro hallucinate) | Loại |
  | **3. Bot nhắc nhở deadline cá nhân qua DM** | ~1.000 học viên | 1 lần/sprint | Mất tập trung, bị ngợp thông báo | Đếm số lượng hỏi deadline | Cao | Loại |

- **Ứng viên ĐÃ LOẠI + vì sao:** 
  - *Ứng viên 2 (Bot trả lời bài tập):* Chi phí sai sót (cost-of-error) rất đắt nếu AI trả lời sai kiến thức khiến học viên làm sai đồ án.
  - *Ứng viên 3 (Bot nhắc deadline cá nhân):* Ít giải quyết được vấn đề học viên kẹt kiến thức thực sự, dễ gây phiền nếu nhắn tin DM liên tục.
- **Ứng viên CHỌN + vì sao (bằng số):** Chọn **Bản tin Điều hành cho TA**. Giúp 10 TA tiết kiệm 45 phút/đêm (tổng 7.5 giờ/đêm của toàn đội vận hành), giảm tỷ lệ trôi tin nhắn từ 40% xuống 0%, đảm bảo 100% thắc mắc được phát hiện trong ngày.

## §3. Giải pháp tương tự đã nghiên cứu
- **Discord Server Analytics (Built-in) / Discord Auto-Summarizer Bot:**
  - *Flow:* Quét toàn bộ tin nhắn trong server để đưa ra biểu đồ hoạt động và tóm tắt hội thoại bằng AI thành các Thread hoặc đoạn văn ngắn.
  - *Đáng học:* Tự động gom nhóm các cuộc hội thoại rời rạc rất tốt theo thời gian thực và hiển thị các kênh hoạt động mạnh nhất.
  - *Đáng né:* Tóm tắt quá chung chung, không có mục tiêu rõ ràng. Nó không phân biệt được đâu là thắc mắc cần giải quyết và đâu là tin nhắn chat thảo luận, từ đó không giải quyết được bài toán trôi câu hỏi của học viên.
  - *Mình khác biệt:* Tập trung hoàn toàn vào workflow xử lý của TA. Chỉ lọc các tin nhắn học viên gọi TA, phân tích cụm lỗi kỹ thuật/logistics đặc thù, và làm nổi bật danh sách các tin chưa được trả lời (với tính năng tương tác Mark as Resolved).
- **NotebookLM (Google) / Custom Study AI Assistants:**
  - *Flow:* Upload tài liệu lớp học (slide, transcript) và đặt câu hỏi để AI trả lời dựa trên nguồn tài liệu đã cung cấp kèm trích dẫn nguồn.
  - *Đáng học:* Cơ chế trích dẫn nguồn (citation) cực kỳ minh bạch và tin cậy, giúp người dùng đối chiếu nhanh chóng.
  - *Đáng né:* Yêu cầu người dùng phải chủ động hỏi từng câu, không có tính năng tự động quét chủ động (push) và tổng hợp tình hình của tập thể lớp.
  - *Mình khác biệt:* Tự động quét (push) và gom nhóm thắc mắc của cả lớp vào cuối ngày thay vì đợi TA vào hỏi từng câu.

## §4. Thiết kế
- **Lát cắt MỘT CÂU:** *"Một TA/Mod vào kênh điều hành lúc 22h · một việc nắm tình hình thắc mắc & câu hỏi tồn đọng của cả lớp trong ngày · một quyết định AI gom nhóm các câu hỏi rải rác, phát hiện top 3 chủ đề kẹt nhiều nhất và lọc danh sách câu hỏi chưa trả lời · một kết quả TA xử lý triệt để 100% tồn đọng và chuẩn bị nội dung recap chỉ trong 10 phút."*
- **Non-goals (≥3 thứ KHÔNG build):**
  1. KHÔNG tự động gửi câu trả lời trực tiếp cho học viên trên kênh công khai (chỉ sinh báo cáo nội bộ cho TA).
  2. KHÔNG tự động chấm điểm hay can thiệp vào hệ thống lệnh `/gate` nộp bài.
  3. KHÔNG tự động xoá hoặc ẩn các tin nhắn rác của học viên.
- **Mức prototype nhắm tới:** [ ] Sketch  [X] Mock  [ ] Working — *Phần mock:* Dữ liệu Discord đầu vào (mock 30 câu thoại giả lập); *Phần thật:* Lời gọi AI thật ở lõi để gom nhóm, lọc câu tồn đọng và sinh báo cáo Markdown.
- **Automation:** [X] automate  [ ] conditional  [ ] augment
  - *Lý do theo cost-of-error:* Chi phí sai sót ở mức THẤP. Bản tin chỉ gửi vào kênh nội bộ `#ta-digest` để TA đọc và tham khảo trước khi hành động. Nếu AI phân loại nhầm 1 câu hỏi, TA vẫn lướt nhanh và chỉnh sửa được ngay, không ảnh hưởng trực tiếp đến điểm số hay trải nghiệm học viên.
- **§4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR):**
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|
  | **G1 — Làm rõ hệ thống làm được gì** | Khai báo rõ ở đầu bản tin: "Bản tin tổng hợp tin nhắn từ 08:00 - 22:00 tại 4 kênh chính". |
  | **G2 — Làm rõ làm tốt đến đâu** | Mọi câu hỏi được gom nhóm đều có đính kèm trích dẫn nguyên văn & link/mã tin nhắn để TA bấm vào kiểm tra lại. |
  | **G8 — Gạt bỏ dễ dàng** | TA có thể chọn bỏ qua gợi ý nội dung Recap của AI nếu thấy chưa sát thực tế. |
  | **G10 — Thu hẹp phạm vi khi nghi ngờ** | Khi không chắc câu hỏi đã được trả lời hay chưa, AI tự động xếp vào nhóm "Cần TA xác minh thủ công". |

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8)
Dưới đây là 8 kịch bản lỗi thuộc 4 lớp chỗ khó của hệ thống, cùng hành vi mong muốn và nguyên tắc HAX áp dụng để xử lý:

| # | Tình huống cụ thể | Lớp khó | Hành vi mong muốn (Nói gì, hiện gì, cho user làm gì) | Nguyên tắc áp dụng |
|---|---|---|---|---|
| 1 | AI tự bịa ra một lỗi kỹ thuật (ví dụ: lỗi cài đặt CUDA) mà không học viên nào hỏi trong ngày. | ① Nguồn sự thật | Bot chỉ hiển thị các chủ đề có trích dẫn tin nhắn gốc kèm mã ID tin nhắn. Nếu không tìm thấy tin nhắn gốc tương ứng, TA có thể phát hiện ngay lỗi bịa đặt. | **G2** (Làm rõ làm tốt đến đâu - đính kèm trích dẫn thực tế để đối chiếu) |
| 2 | Model trích dẫn sai mã tin nhắn hoặc link liên kết đến tin nhắn của học viên. | ① Nguồn sự thật | Giao diện hiển thị link jump trực tiếp đến Discord channel. Nếu link hỏng hoặc sai, TA có thể dùng nút "Re-sync" để yêu cầu quét lại. | **G9** (Sửa dễ dàng - cho phép Re-sync quét lại dữ liệu sạch) |
| 3 | Học viên chỉ chat: "Anh ơi cứu em với" hoặc "lỗi này sửa sao ạ" kèm hình ảnh không có văn bản. | ② Mơ hồ | Bot phân loại các tin nhắn này vào nhóm riêng: **"Cần TA xác minh thủ công (tin nhắn mơ hồ)"** và giải thích rõ: "Thiếu ngữ cảnh để tự động phân loại". | **G10** (Thu hẹp phạm vi khi nghi ngờ) |
| 4 | Học viên gõ tin nhắn viết tắt, không dấu, dùng tiếng lóng (ví dụ: "api key bị tèo r"). | ② Mơ hồ | AI sử dụng prompt có ví dụ few-shot để nhận diện ngữ cảnh và gom đúng vào nhóm "Lỗi cấu hình API key", tránh bỏ sót. | **G11** (Giải thích vì sao - dựa trên từ khóa ngữ cảnh) |
| 5 | Học viên hỏi thông tin ngoài phạm vi lớp học (ví dụ: xin pass wifi phòng lab, hỏi xin tài liệu Photoshop). | ③ Ngoài phạm vi | Bot tự động lọc bỏ các câu hỏi này và không đưa vào Bản tin điều hành chính. Tuy nhiên, vẫn lưu trữ ở phần "Đã lọc bỏ ngoài phạm vi" ở cuối để TA xem lại nếu cần. | **G10** (Thu hẹp phạm vi) & **HAX G1** |
| 6 | Học viên hỏi xin đáp án của quiz hoặc yêu cầu TA viết hộ code bài tập lớn. | ③ Ngoài phạm vi | Bot gom vào nhóm "Cảnh báo vi phạm quy chế (Forbidden)" để cảnh cáo TA theo dõi, không hiển thị gợi ý hỗ trợ kỹ thuật cho case này. | **G2** (Chỉ rõ phạm vi quyền hạn và quy chế) |
| 7 | Học viên hỏi về hạn nộp bài tập nhưng AI lại phân tích nhầm thành lỗi kỹ thuật, dẫn đến nguy cơ TA trả lời muộn làm học viên mất điểm. | ④ Đặc thù domain | Bot đưa tất cả câu hỏi liên quan đến từ khóa deadline/hạn nộp vào cụm "Logistics/Hạn chót" với mức độ ưu tiên cao nhất trong bản tin. | **G2** & **G10** (Đặt mức ưu tiên cao cho các case ảnh hưởng điểm số) |
| 8 | Học viên đăng câu hỏi nhưng sau đó tự sửa được và phản hồi "đã chạy được". AI vẫn gom nhóm là chưa phản hồi. | ④ Đặc thù domain | TA có thể bấm nút **"Mark as Resolved"** trực tiếp trên giao diện Discord để ẩn câu hỏi này khỏi danh sách chưa trả lời ngay lập tức. | **G8** (Gạt bỏ dễ dàng) & **G9** (Sửa dễ dàng) |

## §6. Bốn đường đi của trải nghiệm
- **Happy path (Đường thuận lợi):** Cuối ngày, TA chạy lệnh `/tonghop`. Bot quét thành công tin nhắn từ 00:00, gửi dữ liệu XML sang Gemini, nhận về JSON và hiển thị Embed phân loại cực kỳ sạch sẽ: Top 3 cụm lỗi chính (API Key, /gate timeout, Deadline) kèm đầy đủ trích dẫn nguyên văn và nút bấm điều hướng.
- **Low-confidence (Đường nghi ngờ - ②):** Khi gặp các tin nhắn ngắn hoặc thiếu thông tin ("helpp", "ad ơi"), Bot không đoán mò mà chuyển chúng vào mục `"Cần TA xác minh thủ công"`. Trên UI, Bot hiện thông tin cảnh báo rõ ràng để TA tự check lại link chat.
- **Failure/không căn cứ (Đường thất bại - ①):** Nếu trong ngày không có tin nhắn nào tag TA/Mod (ví dụ ngày nghỉ lễ), Bot hiển thị: *"📭 Không ghi nhận thắc mắc mới trong ngày"* kèm thông báo chế độ hiển thị dự phòng chứ không cố gom nhóm lung tung.
- **Correction (Đường hiệu chỉnh):** Khi AI gom nhóm sai hoặc TA đã trả lời thủ công qua kênh chat mà không dùng Reply:
  1. TA xem tin nhắn qua lệnh `/checkmiss`, click nút **Mark as Resolved** để ẩn tin nhắn đó khỏi danh sách chờ ngay tức thì.
  2. Hoặc TA sửa lại prompt/dữ liệu và bấm **Re-sync** để cập nhật lại bản tin sạch.

## §7. Kiểm thử
- **Chiều chất lượng + định nghĩa kiểm chứng được:**
  - *Độ chính xác gom nhóm (Clustering Accuracy):* Các câu hỏi thuộc cùng một bản chất lỗi phải được gom vào chung một nhóm phù hợp (Đo bằng hàm `verify_match` đối chiếu nhãn mong muốn trong bộ eval).
  - *Độ bao phủ câu hỏi chưa trả lời (Recall):* 100% tin nhắn của học viên chưa được trả lời thực sự phải xuất hiện trong danh sách cảnh báo của Bot (không bị bỏ sót).
- **Golden set:** Sử dụng tệp [eval/dataset.json](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/eval/dataset.json) gồm 20 case chatlog thực tế và giả lập, phủ đủ 4 lớp chỗ khó (Ngoài phạm vi, Mơ hồ, Quy chế, Deadline).
- **Quality bar (Chốt cố định):** Đạt khi tỉ lệ phân loại đúng nghĩa của AI đạt **>= 80%** (ít nhất 16/20 câu hỏi) và tỉ lệ phát hiện tin chưa rep đạt **100% (Recall = 100%)**, tuyệt đối không bỏ sót câu hỏi logistics/deadline.
- **Kết quả các lượt chạy:**
  - **Lượt chạy 1 (Ngày 1 - CP3):** Đạt **19/20** câu hỏi phân loại đúng nghĩa (tỉ lệ **95%**), không bỏ sót tin nhắn quan trọng nào. Đạt chuẩn Quality Bar đề ra. Chi tiết ghi nhận tại báo cáo kết quả tự động [results.md](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/eval/results.md).

## §8. Phân công & Kế hoạch
- **Phân công có tên:**
  - *Phân tích dữ liệu & Prompt Engineering:* **Nguyễn Ngọc Lan** (2A202601384)
  - *Lấy tin nhắn từ Discord, setup Server & Discord Bot:* **Hoàng Hương Giang** (2A202601470)
  - *Thiết kế UI câu trả lời của Bot, pagination & button interaction:* **Nguyễn Hoàng Duy** (2A202601466)
  - *Viết Spec chung & Chạy Validation:* Cả nhóm cùng thực hiện.
- **Willing users (3 TA thực tế ngoài nhóm):**
  1. **Nguyễn Văn Minh** (TA phụ trách kỹ thuật lớp Batch 03)
  2. **Phạm Thị Thảo** (TA phụ trách Logistics Zone 9)
  3. **Trần Đức Anh** (Mod vận hành server Discord Batch 03)
- **Kế hoạch vòng validation CP5:**
  - Triển khai chạy Bot Discord thật trên server test, nạp dữ liệu mô phỏng từ chatlog.
  - Mời 3 willing users sử dụng lệnh `/tonghop` và `/checkmiss` trực tiếp trên kênh chat.
  - Thực hiện phỏng vấn nhanh với 3 câu hỏi trải nghiệm và ghi chép nhật ký phản hồi chi tiết tại [validation/feedback_log.md](file:///d:/VinAI/Batch03-K4-AI-Product-Hackathon/validation/feedback_log.md).

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| 10:00 N1 | Tạo bản spec nháp đầu tiên | Hoàn thành Checkpoint 1 Canvas |
| 17:00 N1 | Đồng bộ logic check phản hồi | Sửa sự không nhất quán giữa `/test_fetch` và `/checkmiss` (sau kiểm thử ghi nhận trong `src/README.md`) |
| 18:00 N1 | Cập nhật phản hồi người dùng (Validation) | Tinh chỉnh giao diện hiển thị Embed phân trang rõ ràng hơn dựa trên phản hồi của TA Minh |
```
