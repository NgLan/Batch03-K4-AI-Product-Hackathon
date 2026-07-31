# -*- coding: utf-8 -*-
"""Mô-đun kéo tin nhắn từ các kênh Discord được cấu hình."""

import discord
from typing import List, Dict, Any
from src.config import TARGET_CHANNELS, TA_ROLE_IDS

def is_member_ta(member: Any) -> bool:
    """Kiểm tra xem thành viên có vai trò TA/Mod trong server không."""
    if hasattr(member, 'roles'):
        return any(r.id in TA_ROLE_IDS for r in member.roles)
    return False

async def check_replied_in_thread(msg: discord.Message) -> bool:
    """Kiểm tra xem thread của tin nhắn có câu trả lời của TA không."""
    if not msg.thread:
        return False
    async for t_msg in msg.thread.history(limit=50):
        if is_member_ta(t_msg.author):
            return True
    return False

async def process_channel(bot: discord.Client, ch_id: int, time_from: Any, time_to: Any) -> List[Dict[str, Any]]:
    """Quét và xử lý tin nhắn của một kênh Discord nhất định."""
    channel = bot.get_channel(ch_id)
    if not channel:
        return []
    history = [m async for m in channel.history(after=time_from, before=time_to, limit=500)]
    msg_dict = {}
    for m in [x for x in history if not x.author.bot]:
        msg_dict[m.id] = {
            "message_id": m.id, "channel_name": channel.name, "author": m.author.display_name,
            "is_ta": is_member_ta(m.author), "content": m.content, "created_at": m.created_at,
            "jump_url": m.jump_url, "is_replied": False
        }
    for m in [x for x in history if not x.author.bot]:
        if m.reference and m.reference.message_id in msg_dict and is_member_ta(m.author):
            msg_dict[m.reference.message_id]["is_replied"] = True
        if await check_replied_in_thread(m) and m.id in msg_dict:
            msg_dict[m.id]["is_replied"] = True
    return [data for data in msg_dict.values() if not data["is_ta"]]

async def fetch_discord_messages(bot: discord.Client, time_from: Any, time_to: Any) -> List[Dict[str, Any]]:
    """Kéo tin nhắn từ các kênh được chỉ định trong khoảng thời gian."""
    raw_messages = []
    for channel_id in TARGET_CHANNELS:
        ch_msgs = await process_channel(bot, channel_id, time_from, time_to)
        raw_messages.extend(ch_msgs)
    return raw_messages