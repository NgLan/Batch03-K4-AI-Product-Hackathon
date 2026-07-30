// app.js — logic của "Bản tin Điều hành" (TA Co-pilot)
//
// MOCK Ở BƯỚC NÀY (CP2 — flow bấm được, chưa cần AI thật):
//   classifyMessages() dùng rule-based (keyword) để gom nhóm/lọc.
//   Ở CP3 hàm này sẽ được thay bằng 1 lời gọi AI thật (LLM phân loại + gom nhóm),
//   giữ nguyên input/output shape bên dưới để phần UI không phải đổi.
//
// THẬT ở bước sau: quyết định trung tâm (gom nhóm chủ đề + lọc câu hỏi tồn đọng)
// sẽ được giao cho AI thật tại CP3 — xem spec.md §4.

const TOPIC_RULES = [
  { key: "api-key-sprint1", label: "Lỗi API key khi viết Prompt (Sprint 1)", test: (t) => /api key/.test(t) && /sprint 1/.test(t) },
  { key: "gate-timeout", label: "Lệnh /gate nộp bài bị timeout", test: (t) => /\/gate/.test(t) || (/timeout/.test(t) && /nộp bài|deadline/.test(t)) },
  { key: "deadline", label: "Thắc mắc deadline / lịch nộp", test: (t) => /deadline/.test(t) },
  { key: "automation-augment", label: "Phân biệt automation vs augment (Sprint 2)", test: (t) => /automation|augment/.test(t) },
  { key: "content-lecture", label: "Thắc mắc nội dung buổi giảng", test: (t) => /slide|recording|rag|few-shot|zero-shot|golden set/.test(t) },
];

const OUT_OF_SCOPE_TEST = (t) => /pass wifi|mật khẩu|số điện thoại|thông tin cá nhân/.test(t);
const AMBIGUOUS_TEST = (t) => {
  const trimmed = t.trim();
  const wordCount = trimmed.split(/\s+/).length;
  return wordCount <= 2 && trimmed.length <= 10; // "hả", "dạ", "ơi", "anh ơi"... input quá ngắn để hiểu ý định
};

function toMinutes(hhmm) {
  const [h, m] = hhmm.split(":").map(Number);
  return h * 60 + m;
}

function classifyMessages(messages, nowMinutes) {
  const result = {
    topics: [],        // top chủ đề kẹt nhiều nhất
    overdue: [],        // chưa trả lời quá 2 tiếng (Recall phải đạt 100%)
    ambiguous: [],       // ② mơ hồ — cần TA xác minh thủ công (G10)
    recapSuggestions: [],
    filteredOutOfScope: [], // ③ ngoài phạm vi — không đưa vào bản tin, chỉ giữ lại để TA soát nếu cần
  };

  const topicBuckets = {};

  for (const msg of messages) {
    const text = msg.text.toLowerCase();

    if (OUT_OF_SCOPE_TEST(text)) {
      result.filteredOutOfScope.push(msg);
      continue; // §5 lớp ③: không đưa vào bản tin điều hành
    }

    if (AMBIGUOUS_TEST(text)) {
      result.ambiguous.push(msg); // §5 lớp ②
      continue;
    }

    const rule = TOPIC_RULES.find((r) => r.test(text));
    const topicKey = rule ? rule.key : "khac";
    const topicLabel = rule ? rule.label : "Câu hỏi khác chưa gom nhóm";
    if (!topicBuckets[topicKey]) topicBuckets[topicKey] = { label: topicLabel, messages: [] };
    topicBuckets[topicKey].messages.push(msg);

    if (!msg.answered && nowMinutes - toMinutes(msg.time) > 120) {
      result.overdue.push(msg); // Cảnh báo tồn đọng >2h
    }
  }

  result.topics = Object.values(topicBuckets)
    .sort((a, b) => b.messages.length - a.messages.length)
    .slice(0, 3);

  if (result.topics.length > 0) {
    result.recapSuggestions = result.topics.map(
      (t) => `Recap lại "${t.label}" — ${t.messages.length} học viên đã hỏi trong ngày.`
    );
  }

  return result;
}

// ---------- Rendering ----------

const state = {
  dismissed: new Set(), // các mục TA đã gạt bỏ (correction path — G8)
};

function quoteBlock(msg) {
  return `
    <li class="quote-item" data-id="${msg.id}">
      <div class="quote-text">"${msg.text}"</div>
      <div class="quote-meta">
        <span>${msg.channel}</span> · <span>${msg.time}</span> · <span>mã tin: ${msg.id}</span>
        ${msg.answered ? `<span class="tag tag-answered">đã trả lời lúc ${msg.answeredAt}</span>` : `<span class="tag tag-pending">chưa trả lời</span>`}
      </div>
    </li>`;
}

function renderDigest(classified) {
  const root = document.getElementById("digest-root");

  if (classified.__empty) {
    root.innerHTML = `
      <div class="empty-state">
        <p>📭 Không ghi nhận thắc mắc mới trong ngày.</p>
        <p class="hint">(Kịch bản Failure §6: log input trống — không có tin nhắn nào để gom nhóm.)</p>
      </div>`;
    return;
  }

  const visibleTopics = classified.topics.filter((t) => !state.dismissed.has("topic:" + t.label));
  const visibleOverdue = classified.overdue.filter((m) => !state.dismissed.has("overdue:" + m.id));
  const visibleRecap = classified.recapSuggestions.filter((r) => !state.dismissed.has("recap:" + r));

  root.innerHTML = `
    <div class="banner">
      ℹ️ Bản tin tổng hợp tin nhắn từ 08:00 - 22:00 tại 4 kênh chính: #hoi-dap, #logistics, #sprint-1, #sprint-2.
      Mọi mục dưới đây đều kèm trích dẫn nguyên văn để TA bấm vào kiểm tra lại.
    </div>

    <section class="card">
      <h2>🔥 Top ${visibleTopics.length} chủ đề kẹt nhiều nhất</h2>
      ${visibleTopics.length === 0 ? "<p class='hint'>Không còn chủ đề nào (đã gạt bỏ hết).</p>" : ""}
      ${visibleTopics
        .map(
          (t, i) => `
        <div class="topic-block">
          <div class="topic-header">
            <strong>#${i + 1} — ${t.label}</strong> <span class="count">(${t.messages.length} lượt hỏi)</span>
            <button class="dismiss-btn" data-kind="topic" data-key="${t.label}">Gạt bỏ nhóm này</button>
          </div>
          <ul class="quote-list">${t.messages.map(quoteBlock).join("")}</ul>
        </div>`
        )
        .join("")}
    </section>

    <section class="card warn">
      <h2>⏰ Cảnh báo tồn đọng &gt; 2 tiếng chưa trả lời</h2>
      ${visibleOverdue.length === 0 ? "<p class='hint'>Không có câu hỏi nào tồn đọng quá 2 tiếng 🎉</p>" : ""}
      <ul class="quote-list">
        ${visibleOverdue
          .map(
            (m) => `
          <li class="quote-item" data-id="${m.id}">
            <div class="quote-text">"${m.text}"</div>
            <div class="quote-meta">
              <span>${m.channel}</span> · <span>${m.time}</span> · <span>mã tin: ${m.id}</span>
              <button class="dismiss-btn small" data-kind="overdue" data-key="${m.id}">Gạt bỏ</button>
            </div>
          </li>`
          )
          .join("")}
      </ul>
    </section>

    <section class="card">
      <h2>📝 Đề xuất nội dung Recap</h2>
      ${visibleRecap.length === 0 ? "<p class='hint'>Chưa có đề xuất recap.</p>" : ""}
      <ul class="recap-list">
        ${visibleRecap
          .map(
            (r) => `
          <li>${r} <button class="dismiss-btn small" data-kind="recap" data-key="${r}">Bỏ qua gợi ý này</button></li>`
          )
          .join("")}
      </ul>
    </section>

    <section class="card muted">
      <h2>❓ Cần TA xác minh thủ công (tin nhắn mơ hồ)</h2>
      <p class="hint">AI không chắc ý định của các tin nhắn dưới đây nên KHÔNG tự phân loại — xếp riêng để TA đọc lại (nguyên tắc G10).</p>
      ${classified.ambiguous.length === 0 ? "<p class='hint'>Không có tin nhắn mơ hồ nào hôm nay.</p>" : ""}
      <ul class="quote-list">${classified.ambiguous.map(quoteBlock).join("")}</ul>
    </section>

    ${
      classified.filteredOutOfScope.length > 0
        ? `<details class="card muted">
      <summary>🚫 Đã lọc bỏ ${classified.filteredOutOfScope.length} tin nhắn ngoài phạm vi (không hiện trong bản tin chính)</summary>
      <ul class="quote-list">${classified.filteredOutOfScope.map(quoteBlock).join("")}</ul>
    </details>`
        : ""
    }
  `;

  document.querySelectorAll(".dismiss-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const { kind, key } = e.target.dataset;
      state.dismissed.add(`${kind}:${key}`);
      renderDigest(window.__lastClassified);
    });
  });
}

function runScan() {
  const daySelect = document.getElementById("day-select");
  const day = MOCK_DAYS[daySelect.value];
  const root = document.getElementById("digest-root");

  root.innerHTML = `<div class="loading">⏳ Đang quét ${day.messages.length} tin nhắn tại 4 kênh...</div>`;

  // giả lập độ trễ gọi AI — ở CP3 đây sẽ là await gọi LLM thật
  setTimeout(() => {
    if (day.messages.length === 0) {
      window.__lastClassified = { __empty: true };
      renderDigest(window.__lastClassified);
      return;
    }
    const classified = classifyMessages(day.messages, NOW_MINUTES);
    window.__lastClassified = classified;
    renderDigest(classified);
  }, 400);
}

function resyncScan() {
  state.dismissed.clear();
  runScan();
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("scan-btn").addEventListener("click", runScan);
  document.getElementById("resync-btn").addEventListener("click", resyncScan);
  runScan();
});
