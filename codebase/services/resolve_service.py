# -*- coding: utf-8 -*-
"""Mô-đun quản lý danh sách tin nhắn được đánh dấu đã trả lời thủ công."""

import json
import os
from typing import Set

RESOLVED_FILE = "data/resolved_ids.json"

def load_resolved_ids() -> Set[int]:
    """Tải danh sách ID tin nhắn đã giải quyết từ file JSON.

    Returns:
        Tập hợp (set) chứa các ID tin nhắn đã giải quyết.
    """
    if not os.path.exists(RESOLVED_FILE):
        return set()
    try:
        with open(RESOLVED_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data) if isinstance(data, list) else set()
    except Exception:
        return set()

def save_resolved_id(message_id: int) -> None:
    """Lưu vĩnh viễn một ID tin nhắn đã giải quyết thủ công vào file JSON.

    Args:
        message_id: ID của tin nhắn cần lưu.
    """
    resolved = load_resolved_ids()
    resolved.add(message_id)
    os.makedirs(os.path.dirname(RESOLVED_FILE), exist_ok=True)
    with open(RESOLVED_FILE, "w", encoding="utf-8") as f:
        json.dump(list(resolved), f, ensure_ascii=False, indent=2)
