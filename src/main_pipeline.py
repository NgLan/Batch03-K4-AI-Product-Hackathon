# -*- coding: utf-8 -*-
"""Mô-đun pipeline tích hợp toàn bộ luồng tổng hợp tin nhắn."""

from typing import List, Dict, Any
from src.services.unanswered_service import filter_unanswered_messages
from src.services.clustering_service import cluster_messages

def run_pipeline(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Chạy toàn bộ pipeline tích hợp để tạo JSON đầu ra cho UI.

    Args:
        messages: Danh sách tin nhắn đầu vào.

    Returns:
        JSON tổng hợp chứa danh sách chưa trả lời và danh sách gom cụm.
    """
    unanswered = filter_unanswered_messages(messages)
    clustered = cluster_messages(messages)
    
    return {
        "unanswered_over_2h": unanswered,
        "top_issues": clustered.get("top_issues", [])
    }
