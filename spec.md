# Template AI Spec *(spec.md — commit trước 23:59 N1 · quality bar chốt từ thời điểm nộp)*

> Cấu trúc phủ đúng "SPEC 8 phần" của chương trình: Bằng chứng (§1-§2) · Lát cắt (§4) · Canvas (đính kèm CP1) · Augment/Automate (§4) · 4 đường đi của trải nghiệm (§6) · Kiểu lỗi (§5) · Kiểm thử (§7) · Phân công (§8). Hướng dẫn viết từng mục: `02-guide.md`.

```markdown
# AI SPEC — Trợ lý "Bản tin Điều hành" cho TA & Mod (TA Co-pilot) · Nhóm [XX] · Zone [X]
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
*(Sẽ bổ sung trong quá trình làm)*
- **Discord Server Analytics / Threads Summarizer:** Flow tóm tắt kênh chát / Đáng học: Gom nhóm tốt / Đáng né: Tóm tắt chung chung không phân loại câu tồn đọng / Mình khác: Tập trung riêng cho workflow cứu câu hỏi trôi của TA.

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
*(Sẽ bổ sung chi tiết trước CP4)*
1. Nguồn sự thật (①): AI bịa ra câu hỏi học viên không hề hỏi -> Hành vi: Chỉ trích dẫn đúng tin nhắn có thật trong log input.
2. Mơ hồ / thiếu thông tin (②): Tin nhắn học viên quá ngắn ("anh ơi", "hả") -> Hành vi: Gom vào nhóm "Tin nhắn chưa rõ ý định".
3. Ngoài phạm vi (③): Học viên hỏi xin pass wifi / thông tin cá nhân -> Hành vi: Bỏ qua không đưa vào bản tin điều hành.
4. Đặc thù domain (④): Học viên hỏi lỗi kỹ thuật bài tập nhưng AI lại gom nhầm sang lỗi Logistics -> Hành vi: Hiển thị trích dẫn gốc để TA phát hiện và chỉnh lại.

## §6. Bốn đường đi của trải nghiệm
*(Sẽ bổ sung chi tiết)*
- **Happy path:** Quét 30 tin nhắn → Sinh bản tin phân loại chuẩn 3 nhóm: Top kẹt nhiều nhất, Cảnh báo tồn >2h, Đề xuất Recap.
- **Low-confidence (②):** Nhận diện tin nhắn không rõ nội dung -> Xếp vào mục "Câu hỏi mơ hồ cần check lại".
- **Failure/không căn cứ (①):** Log input trống/không có tin nhắn mới -> Hiển thị "Không ghi nhận thắc mắc mới trong ngày".
- **Correction (user sửa):** TA bấm nút "Re-sync" hoặc gạt bỏ 1 mục phân loại sai trên giao diện.

## §7. Kiểm thử
- **Chiều chất lượng + định nghĩa kiểm chứng được:**
  - *Độ chính xác gom nhóm (Accuracy):* Các câu hỏi cùng chủ đề được gom đúng nhóm (Pass/Fail).
  - *Không bỏ sót (Recall):* 100% câu hỏi chưa trả lời quá 2 tiếng phải nằm trong danh sách Cảnh báo.
- **Golden set:** File `eval/golden_set.json` (Gồm 20 case chatlog mô phỏng các tình huống).
- **Quality bar (chốt từ 23:59 N1):** "Đạt khi ≥ 80% qua bộ golden set, và không bỏ sót câu hỏi chưa trả lời nào (Recall = 100%)."
- **Kết quả các lượt chạy:** *(Sẽ cập nhật ở CP3)*

## §8. Phân công & Kế hoạch
- **Phân công có tên:**
  - *Spec & Evidence Mining:* [Tên thành viên 1]
  - *Prompt Engineering & Golden Set:* [Tên thành viên 2]
  - *Build Prototype (App/Bot):* [Tên thành viên 3]
  - *Validation (Test với TA) & Slide:* [Tên thành viên 4]
- **Willing users (≥3 tên):**
  1. Nguyễn Văn A (TA Zone 1)
  2. Trần Thị B (TA Zone 2)
  3. Lê Văn C (Học viên đóng vai trò Mod)
- **Kế hoạch vòng validation CP5:** Chuẩn bị 1 bản tin chạy thật từ 30 tin nhắn test → Gửi cho 3 TA dùng thử → Hỏi 3 câu hỏi trải nghiệm → Log lại nhận xét.

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
|---|---|---|
| 10:00 N1 | Tạo bản spec nháp đầu tiên | Hoàn thành Checkpoint 1 Canvas |
```
