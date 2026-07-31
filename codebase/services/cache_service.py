# -*- coding: utf-8 -*-
"""Mô-đun quản lý bộ nhớ đệm (cache) kết quả phân tích tin nhắn."""

import json
import os
import datetime
from typing import Dict, Any, Optional

CACHE_FILE = "data/analysis_cache.json"

def get_cached_analysis() -> Optional[Dict[str, Any]]:
    """Lấy kết quả phân tích từ cache nếu chưa quá 10 phút.

    Returns:
        Dữ liệu kết quả phân tích hoặc None nếu cache đã hết hạn hoặc không tồn tại.
    """
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache_data = json.load(f)
        
        timestamp_str = cache_data.get("timestamp", "")
        timestamp = datetime.datetime.fromisoformat(timestamp_str)
        now = datetime.datetime.now(datetime.timezone.utc)
        
        if (now - timestamp).total_seconds() < 600:
            return cache_data.get("data")
    except Exception:
        pass
    return None

def save_to_cache(data: Dict[str, Any]) -> None:
    """Lưu kết quả phân tích và thời điểm hiện tại vào cache file.

    Args:
        data: Kết quả phân tích cần lưu.
    """
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    cache_data = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "data": data
    }
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache_data, f, ensure_ascii=False, indent=2)
