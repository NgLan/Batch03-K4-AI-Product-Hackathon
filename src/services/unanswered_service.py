# -*- coding: utf-8 -*-
"""Mô-đun lọc các câu hỏi chưa được trả lời trên Discord."""

import datetime
from typing import List, Dict, Any

def format_datetime(dt: Any) -> str:
    """Định dạng đối tượng datetime thành chuỗi ISO 8601 với múi giờ UTC.

    Args:
        dt: Đối tượng datetime hoặc chuỗi thời gian.

    Returns:
        Chuỗi thời gian định dạng ISO 8601 (ví dụ: '2026-07-30T08:55:40Z').
    """
    if isinstance(dt, datetime.datetime):
        # Đảm bảo UTC format kết thúc bằng Z
        if dt.tzinfo == datetime.timezone.utc or (dt.tzinfo and dt.tzinfo.utcoffset(dt) == datetime.timedelta(0)):
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        return dt.isoformat()
    return str(dt)

def filter_unanswered_messages(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Lọc danh sách các tin nhắn của học viên chưa được trả lời tại thời điểm phân tích.

    Args:
        messages: Danh sách tin nhắn đầu vào.

    Returns:
        Danh sách tin nhắn chưa trả lời được định dạng lại các trường cần thiết.
    """
    unanswered = []
    for msg in messages:
        if not msg.get("is_ta", False) and not msg.get("is_replied", False):
            unanswered.append({
                "message_id": msg["message_id"],
                "author": msg["author"],
                "content": msg["content"],
                "created_at": format_datetime(msg["created_at"]),
                "channel_name": msg["channel_name"],
                "jump_url": msg["jump_url"]
            })
    return unanswered
