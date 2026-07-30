// Dữ liệu GIẢ LẬP (mock) — 30 tin nhắn mô phỏng theo đúng lát cắt spec.md §4.
// KHÔNG phải data thật của học viên. Dùng để bấm-thử flow ở CP2.
// "now" giả định là 22:00 cùng ngày — thời điểm TA mở bản tin điều hành.

const NOW_MINUTES = 22 * 60; // 22:00

function toMinutes(hhmm) {
  const [h, m] = hhmm.split(":").map(Number);
  return h * 60 + m;
}

// channel: #hoi-dap | #logistics | #sprint-1 | #sprint-2
// answered: đã có người trả lời trong kênh chưa
// scope: "in" (đúng phạm vi TA cần xử lý) | "out" (ngoài phạm vi, vd hỏi info cá nhân)
const MESSAGES_TODAY = [
  { id: "M01", channel: "#sprint-1", time: "14:05", author: "U12", text: "Mọi người cho mình hỏi bài 2 Sprint 1 đoạn viết Prompt bị lỗi API key thì sửa sao ạ?", answered: false },
  { id: "M02", channel: "#sprint-1", time: "14:20", author: "U03", text: "Em cũng bị y chang, lỗi API key khi chạy Prompt bài 2 Sprint 1 luôn", answered: false },
  { id: "M03", channel: "#sprint-1", time: "15:02", author: "U27", text: "API key Sprint 1 bị invalid hoài, ai fix chưa ạ", answered: false },
  { id: "M04", channel: "#sprint-1", time: "15:40", author: "U08", text: "lỗi api key sprint 1 y như 3 bạn trên, chưa ai trả lời hết á", answered: false },
  { id: "M05", channel: "#sprint-1", time: "16:10", author: "U19", text: "cho em hỏi thêm về lỗi api key ở bài 2 sprint 1 với, key em copy từ .env mà vẫn lỗi", answered: false },
  { id: "M06", channel: "#sprint-1", time: "17:00", author: "U31", text: "confirm thêm 1 case lỗi api key sprint 1 nữa nè mọi người", answered: false },
  { id: "M07", channel: "#logistics", time: "22:10", author: "U02", text: "Em gõ lệnh /gate nộp bài toàn báo timeout, deadline 23h59 hôm nay rồi ạ", answered: false },
  { id: "M08", channel: "#logistics", time: "21:50", author: "U15", text: "/gate của em cũng timeout y vậy, deadline gần tới rồi lo quá", answered: false },
  { id: "M09", channel: "#logistics", time: "20:30", author: "U22", text: "lệnh /gate nộp bài lag/timeout từ chiều tới giờ, TA check giúp em với", answered: false },
  { id: "M10", channel: "#hoi-dap", time: "21:15", author: "U05", text: "Anh chị TA ơi câu hỏi của em ở trên từ chiều chưa ai answer ạ 😭", answered: false },
  { id: "M11", channel: "#hoi-dap", time: "13:00", author: "U09", text: "Cho em hỏi buổi giảng hôm nay phần RAG có slide đính kèm không ạ?", answered: true, answeredAt: "13:20" },
  { id: "M12", channel: "#hoi-dap", time: "18:45", author: "U14", text: "Thầy ơi khái niệm few-shot prompting với zero-shot khác nhau chỗ nào ạ, em đọc slide chưa rõ lắm", answered: false },
  { id: "M13", channel: "#sprint-2", time: "19:00", author: "U06", text: "Sprint 2 phần đánh giá golden set mình nộp file json hay csv vậy ạ?", answered: true, answeredAt: "19:30" },
  { id: "M14", channel: "#sprint-2", time: "20:05", author: "U28", text: "Rubric sprint 2 mục automation với augment khác nhau thế nào, em vẫn lú ạ", answered: false },
  { id: "M15", channel: "#hoi-dap", time: "20:50", author: "U11", text: "anh ơi", answered: false },
  { id: "M16", channel: "#hoi-dap", time: "21:05", author: "U11", text: "hả", answered: false },
  { id: "M17", channel: "#logistics", time: "12:00", author: "U17", text: "dạ", answered: false },
  { id: "M18", channel: "#hoi-dap", time: "09:30", author: "U04", text: "cho em xin pass wifi phòng lab với ạ", answered: false, scope: "out" },
  { id: "M19", channel: "#logistics", time: "10:15", author: "U21", text: "mọi người ơi số điện thoại TA trực hôm nay là gì vậy ạ, em cần liên hệ riêng", answered: false, scope: "out" },
  { id: "M20", channel: "#sprint-1", time: "11:00", author: "U33", text: "cảm ơn TA đã fix lỗi hôm qua nha, giờ chạy mượt rồi ạ", answered: true, answeredAt: "11:05" },
  { id: "M21", channel: "#logistics", time: "08:40", author: "U07", text: "Deadline sprint 1 là 23h59 hôm nay đúng không ạ, em xem lịch thấy ghi 2 mốc khác nhau", answered: true, answeredAt: "09:00" },
  { id: "M22", channel: "#hoi-dap", time: "16:30", author: "U29", text: "Bài giảng buổi 2 phần đo lường chất lượng AI, TA có thể cho em xin lại link recording không ạ", answered: false },
  { id: "M23", channel: "#sprint-1", time: "18:00", author: "U16", text: "lỗi api key sprint 1 giờ này em vẫn chưa fix được, deadline tối nay rồi", answered: false },
  { id: "M24", channel: "#sprint-2", time: "13:45", author: "U24", text: "Golden set sprint 2 cần tối thiểu bao nhiêu case vậy TA?", answered: true, answeredAt: "14:00" },
  { id: "M25", channel: "#logistics", time: "21:30", author: "U18", text: "/gate lại timeout nữa rồi, đây là lần thứ 3 em thử trong tối nay", answered: false },
  { id: "M26", channel: "#hoi-dap", time: "10:00", author: "U13", text: "ơi", answered: false },
  { id: "M27", channel: "#sprint-2", time: "17:15", author: "U26", text: "Phần automation trong sprint 2 TA ơi cho em hỏi thêm ví dụ cụ thể được không ạ", answered: false },
  { id: "M28", channel: "#hoi-dap", time: "19:20", author: "U32", text: "Em thấy 2 bạn hỏi giống câu em từ chiều mà chưa thấy TA trả lời chung ạ", answered: false },
  { id: "M29", channel: "#logistics", time: "22:05", author: "U30", text: "Sắp hết giờ nộp bài mà /gate vẫn timeout, TA cứu em với ạ", answered: false },
  { id: "M30", channel: "#sprint-1", time: "09:15", author: "U10", text: "Chào mọi người, chúc cả lớp code vui vẻ hôm nay!", answered: true, answeredAt: "09:16" },
];

// Kịch bản "Failure / không căn cứ" (§6): ngày không có tin nhắn mới nào.
const MESSAGES_EMPTY_DAY = [];

const MOCK_DAYS = {
  "2026-07-30": { label: "Hôm nay (30/07) — có 30 tin nhắn", messages: MESSAGES_TODAY },
  "2026-07-29": { label: "Hôm qua (29/07) — không có tin nhắn mới", messages: MESSAGES_EMPTY_DAY },
};
