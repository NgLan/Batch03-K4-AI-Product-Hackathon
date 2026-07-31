# -*- coding: utf-8 -*-
"""Mô-đun hỗ trợ trích xuất và chuyển đổi dữ liệu tin nhắn từ Discord API."""

import discord
from typing import List, Dict, Any

def is_ta_user(member: Any) -> bool:
    """Kiểm tra xem người dùng có phải là TA/Mod hay không.

    Args:
        member: Đối tượng tác giả tin nhắn (Member hoặc User).

    Returns:
        True nếu là TA/Mod, ngược lại False.
    """
    if hasattr(member, "roles"):
        for role in member.roles:
            if "TA" in role.name.upper() or "MOD" in role.name.upper():
                return True
    return False

def check_replied(msg: discord.Message, all_msgs: List[discord.Message]) -> bool:
    """Kiểm tra xem tin nhắn đã có câu trả lời từ TA hoặc người khác chưa.

    Args:
        msg: Tin nhắn cần kiểm tra.
        all_msgs: Danh sách toàn bộ tin nhắn trong kênh.

    Returns:
        True nếu đã được phản hồi, ngược lại False.
    """
    msg_idx = all_msgs.index(msg)
    # Duyệt các tin nhắn gửi sau tin nhắn này
    for post_msg in all_msgs[:msg_idx]:
        if post_msg.reference and post_msg.reference.message_id == msg.id:
            return True
        # Nếu có tin nhắn của TA gửi sau đó trong cùng kênh
        if is_ta_user(post_msg.author) and post_msg.created_at > msg.created_at:
            return True
    return False

def is_calling_ta(msg: discord.Message) -> bool:
    """Kiểm tra xem tin nhắn có gọi đến TA hoặc chứa '@TA'/'@Mod' không."""
    content_upper = msg.content.upper()
    if "@TA" in content_upper or "@MOD" in content_upper:
        return True
    if any("TA" in r.name.upper() or "MOD" in r.name.upper() for r in msg.role_mentions):
        return True
    return any(is_ta_user(u) for u in msg.mentions)

def transform_message(msg: discord.Message, all_msgs: List[discord.Message]) -> Dict[str, Any]:
    """Chuyển đổi tin nhắn discord.Message sang dạng dict chuẩn của pipeline.

    Args:
        msg: Đối tượng tin nhắn Discord.
        all_msgs: Danh sách tất cả tin nhắn trong kênh.

    Returns:
        Dictionary chứa thông tin tin nhắn đã chuẩn hóa.
    """
    return {
        "message_id": msg.id,
        "channel_name": msg.channel.name if hasattr(msg.channel, "name") else "unknown",
        "author": msg.author.display_name,
        "is_ta": is_ta_user(msg.author),
        "content": msg.content,
        "created_at": msg.created_at,
        "jump_url": msg.jump_url,
        "is_replied": check_replied(msg, all_msgs)
    }

async def fetch_channel_messages(channel: Any, limit: int = 50) -> List[Dict[str, Any]]:
    """Lấy danh sách tin nhắn từ một channel Discord và chuyển đổi định dạng.

    Args:
        channel: Kênh chat Discord.
        limit: Số lượng tin nhắn tối đa cần lấy.

    Returns:
        Danh sách tin nhắn định dạng dict chuẩn.
    """
    history_msgs = []
    async for m in channel.history(limit=limit):
        history_msgs.append(m)
        
    result = []
    for m in history_msgs:
        if m.author.bot:
            continue
        if is_ta_user(m.author):
            continue
        if is_calling_ta(m) and not check_replied(m, history_msgs):
            result.append(transform_message(m, history_msgs))
    return result
