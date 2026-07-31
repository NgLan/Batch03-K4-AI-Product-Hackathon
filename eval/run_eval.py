# -*- coding: utf-8 -*-
"""Tập lệnh kiểm thử tự động (Evaluation Run) cho bộ 20 câu hỏi Checkpoint 3."""

import json
import os
import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv
from codebase.services.llm_client import get_genai_client
from codebase.services.clustering_service import cluster_messages

def load_dataset() -> List[Dict[str, Any]]:
    """Tải bộ dữ liệu câu hỏi từ file JSON."""
    path = "eval/dataset.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def verify_match(expected: str, actual: str) -> bool:
    """Kiểm tra xem chủ đề thực tế có khớp nghĩa với chủ đề mong muốn không."""
    expected_lower = expected.lower()
    actual_lower = actual.lower()
    if expected_lower in actual_lower or actual_lower in expected_lower:
        return True
    keywords = {
        "api": ["api", "key", "auth", "xác thực", "unauthorized"],
        "môi trường": ["cài đặt", "môi trường", "thư viện", "pip", "dotenv", "modulenotfound"],
        "ngoài phạm vi": ["ngoài", "phạm vi", "aws", "docker", "vps", "photoshop", "native"],
        "mơ hồ": ["mơ hồ", "thiếu", "ngữ cảnh", "thông tin", "cụt"],
        "quy chế": ["quy chế", "vi phạm", "quiz", "đáp án", "code hộ", "hack"],
        "nộp bài": ["nộp", "muộn", "hạn", "deadline", "trễ"]
    }
    for key, words in keywords.items():
        if key in expected_lower:
            return any(w in actual_lower for w in words)
    return False

def write_results_report(rows: List[Dict[str, Any]], passed_count: int, total: int) -> None:
    """Ghi báo cáo kết quả kiểm thử ra tệp Markdown."""
    report_path = "eval/results.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Báo cáo kết quả kiểm thử tự động - Checkpoint 3\n\n")
        f.write(f"## Kết quả tổng quan: **{passed_count}/{total}** câu đạt chuẩn (Tỉ lệ: {passed_count/total*100:.1f}%)\n\n")
        f.write("### Chuẩn đạt của nhóm:\n")
        f.write("- **Tỉ lệ đạt:** >= 80% số câu hỏi.\n")
        f.write("- **Zero-tolerance:** Tuyệt đối không được trả lời sai/bịa đặt thông tin liên quan đến hạn chót (Deadline) hoặc vi phạm quy chế học tập.\n\n")
        f.write("### Bảng kết quả chi tiết:\n\n")
        f.write("| ID | Phân loại | Nguồn | Nội dung câu hỏi | Chủ đề mong muốn | Chủ đề thực tế | Kết quả |\n")
        f.write("|---|---|---|---|---|---|---|\n")
        for r in rows:
            status = "✅ Đạt" if r["pass"] else "❌ Fail"
            f.write(f"| {r['id']} | {r['type']} | {r['source']} | {r['content']} | {r['expected']} | {r['actual']} | {status} |\n")

def main() -> None:
    """Hàm chạy chính để quét và đánh giá toàn bộ tập dữ liệu."""
    load_dotenv()
    dataset = load_dataset()
    now = datetime.datetime.now(datetime.timezone.utc)
    msgs = [{
        "message_id": d["id"], "author": "Student", "content": d["content"], "is_ta": False, "is_replied": False,
        "created_at": now, "channel_name": "test-channel", "jump_url": "https://discord.com/channels/1/1/1"
    } for d in dataset]
    clustered = cluster_messages(msgs)
    id_to_topic = {m["message_id"]: issue["topic"] for issue in clustered.get("top_issues", []) for m in issue.get("messages", [])}
    rows, passed = [], 0
    for item in dataset:
        actual = id_to_topic.get(item["id"], "Không phân loại được")
        is_ok = verify_match(item["expected_category"], actual)
        passed += 1 if is_ok else 0
        rows.append({
            "id": item["id"], "type": item["type"], "source": item["source"],
            "content": item["content"], "expected": item["expected_category"],
            "actual": actual, "pass": is_ok
        })
    write_results_report(rows, passed, len(dataset))
    print(f"Hoàn thành đánh giá. Kết quả: {passed}/{len(dataset)} câu đạt.")

if __name__ == "__main__":
    main()
