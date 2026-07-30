# Codebase — TA Co-pilot (Bản tin Điều hành)

Prototype mức **Mock** cho CP2 — flow chính bấm đi hết được, chưa cần AI thật.

## Chạy thử

Mở trực tiếp `codebase/index.html` bằng trình duyệt (double-click, hoặc kéo thả vào Chrome/Edge). Không cần cài đặt gì thêm.

## Flow chính (đúng lát cắt spec.md §4)

1. Chọn ngày → bấm **"Quét dữ liệu hôm nay"** → hệ thống gom nhóm tin nhắn từ 4 kênh (`#hoi-dap`, `#logistics`, `#sprint-1`, `#sprint-2`).
2. Bản tin hiện 4 khối: **Top 3 chủ đề kẹt nhiều nhất** · **Cảnh báo tồn đọng >2h** · **Đề xuất Recap** · **Cần TA xác minh (tin nhắn mơ hồ)**.
3. Mỗi mục có trích dẫn nguyên văn + mã tin nhắn để TA kiểm tra lại (G2).
4. TA có thể **"Gạt bỏ"** một mục nếu thấy phân loại sai (G8/G9), hoặc bấm **"Re-sync"** để chạy lại từ đầu.
5. Chọn ngày "Hôm qua (29/07)" để xem kịch bản **Failure** (không có tin nhắn nào).

## Phần nào MOCK, phần nào THẬT

| Phần | Trạng thái | Ghi chú |
|---|---|---|
| Dữ liệu tin nhắn (`mock-data.js`) | **Mock** | 30 tin nhắn giả lập, không phải data thật của học viên |
| Logic gom nhóm chủ đề + lọc tồn đọng (`classifyMessages` trong `app.js`) | **Mock (rule-based)** | Hiện dùng keyword-matching để flow bấm được ngay ở CP2. Sẽ thay bằng 1 lời gọi AI (LLM) thật ở CP3 — giữ nguyên input/output shape nên phần UI không cần đổi |
| Giao diện bản tin + 4 đường đi trải nghiệm | **Thật** | Happy / low-confidence / failure / correction đều bấm được |

## 4 đường đi trải nghiệm đã thể hiện

- **Happy path:** chọn "Hôm nay" → quét → ra đủ 3 nhóm phân loại.
- **Low-confidence (②):** tin nhắn quá ngắn ("hả", "dạ", "ơi") → rơi vào khối "Cần TA xác minh thủ công".
- **Failure (①):** chọn "Hôm qua" (log trống) → hiện "Không ghi nhận thắc mắc mới trong ngày".
- **Correction:** bấm "Gạt bỏ" trên 1 mục sai, hoặc "Re-sync" để làm lại từ đầu.

## Kế hoạch CP3

Thay hàm `classifyMessages()` bằng lời gọi AI thật (ví dụ Google AI Studio/Gemini free tier — chỉ đưa data giả) để gom nhóm chủ đề + phát hiện tồn đọng, log lại request/response vào `eval/` để làm bằng chứng "AI thật, không hardcode".
