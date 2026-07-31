# -*- coding: utf-8 -*-
"""Mô-đun pipeline tích hợp toàn bộ luồng tổng hợp tin nhắn."""

from typing import List, Dict, Any
from codebase.services.unanswered_service import filter_unanswered_messages
from codebase.services.clustering_service import cluster_messages
from codebase.services.resolve_service import load_resolved_ids

def filter_resolved_from_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """Loại bỏ các tin nhắn đã được giải quyết thủ công khỏi kết quả."""
    resolved = load_resolved_ids()
    if not resolved:
        return results
        
    unanswered = [m for m in results.get("unanswered_over_2h", []) if m["message_id"] not in resolved]
    top_issues = []
    for issue in results.get("top_issues", []):
        msgs = [m for m in issue.get("messages", []) if m["message_id"] not in resolved]
        if msgs:
            top_issues.append({
                "topic": issue["topic"],
                "count": len(msgs),
                "messages": msgs
            })
    return {"unanswered_over_2h": unanswered, "top_issues": top_issues}

def run_pipeline(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Chạy toàn bộ pipeline tích hợp để tạo JSON đầu ra cho UI.

    Args:
        messages: Danh sách tin nhắn đầu vào.

    Returns:
        JSON tổng hợp chứa danh sách chưa trả lời và danh sách gom cụm.
    """
    unanswered = filter_unanswered_messages(messages)
    clustered = cluster_messages(messages)
    
    raw_results = {
        "unanswered_over_2h": unanswered,
        "top_issues": clustered.get("top_issues", [])
    }
    return filter_resolved_from_results(raw_results)
