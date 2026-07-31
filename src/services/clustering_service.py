# -*- coding: utf-8 -*-
"""Mô-đun thực hiện gom cụm thắc mắc của học viên sử dụng Gemini API."""

import json
from typing import List, Dict, Any
from src.services import llm_client
from src.services.unanswered_service import format_datetime
from src.prompts.clustering_prompt import SYSTEM_PROMPT

def serialize_message(msg: Dict[str, Any]) -> str:
    """Chuyển đổi một tin nhắn sang chuỗi JSON rút gọn để gửi lên LLM.

    Args:
        msg: Dictionary tin nhắn gốc.

    Returns:
        Chuỗi JSON của tin nhắn đã lọc bớt các trường không cần thiết.
    """
    clean_msg = {
        "message_id": msg["message_id"],
        "author": msg["author"],
        "content": msg["content"],
        "created_at": format_datetime(msg["created_at"]),
        "channel_name": msg["channel_name"],
        "jump_url": msg["jump_url"]
    }
    return json.dumps(clean_msg, ensure_ascii=False)

def clean_json_text(text: str) -> str:
    """Lọc bỏ các ký tự bọc markdown block để lấy chuỗi JSON thuần.

    Args:
        text: Chuỗi văn bản thô từ model.

    Returns:
        Chuỗi JSON đã được làm sạch.
    """
    text = text.strip()
    if text.startswith("```"):
        text = text[3:].strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()
    if text.endswith("```"):
        text = text[:-3].strip()
    return text

def cluster_messages(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Gom nhóm các câu hỏi của học sinh thông qua Gemini API."""
    student_msgs = [m for m in messages if not m.get("is_ta", False)]
    if not student_msgs:
        return {"top_issues": []}

    xml_data = f"<student_messages>\n" + \
               "\n".join(serialize_message(m) for m in student_msgs) + \
               "\n</student_messages>"

    response_text = llm_client.generate_text(
        prompt=xml_data,
        system_instruction=SYSTEM_PROMPT
    )
    result = json.loads(clean_json_text(response_text))

    # Gemini không được yêu cầu trả về is_replied, nên gắn lại từ dữ liệu gốc
    # (nguồn sự thật) thay vì tin vào model, để hiển thị đúng trạng thái đã rep.
    id_to_replied = {m["message_id"]: m.get("is_replied", False) for m in student_msgs}
    for issue in result.get("top_issues", []):
        for m in issue.get("messages", []):
            m["is_replied"] = id_to_replied.get(m["message_id"], False)

    return result
