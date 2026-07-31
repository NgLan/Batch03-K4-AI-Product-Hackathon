# -*- coding: utf-8 -*-
"""Mô-đun khởi chạy Bot Discord và xử lý các lệnh Slash phân tích tin nhắn."""

import os
from datetime import datetime, time, timezone, timedelta
from typing import Any, Dict
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from src.discord_fetcher import fetch_discord_messages 
from src.services.discord_service import fetch_channel_messages
from src.services.cache_service import get_cached_analysis, save_to_cache
from src.services.resolve_service import load_resolved_ids
from src.main_pipeline import filter_resolved_from_results
from src.services.ui_service import MessagePaginationView, build_topics_summary_embed
from src.config import TARGET_CHANNELS

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready() -> None:
    """Gọi khi bot online thành công và đồng bộ cây lệnh Slash."""
    await bot.tree.sync() 
    print(f'Bot {bot.user} đã online và sẵn sàng chạy thật!')

# async def get_or_run_analysis(channel: Any, limit: int) -> Dict[str, Any]:
#     """Lấy dữ liệu phân tích từ cache hoặc chạy phân tích mới nếu hết hạn."""
#     cached = get_cached_analysis()
#     if cached:
#         return filter_resolved_from_results(cached)
#     msgs = await fetch_channel_messages(channel, limit)
#     from src.services.unanswered_service import filter_unanswered_messages
#     from src.services.clustering_service import cluster_messages
#     raw = {
#         "unanswered_over_2h": filter_unanswered_messages(msgs),
#         "top_issues": cluster_messages(msgs).get("top_issues", [])
#     }
#     save_to_cache(raw)
#     return filter_resolved_from_results(raw)

async def get_or_run_analysis(bot: commands.Bot, limit: int) -> Dict[str, Any]:
    """Lấy dữ liệu phân tích từ cache hoặc chạy phân tích mới cho TẤT CẢ các kênh."""
    cached = get_cached_analysis()
    if cached:
        return filter_resolved_from_results(cached)
    # Tính mốc thời gian 00:00 hôm nay (Theo giờ Việt Nam GMT+7)
    now_utc = datetime.now(timezone.utc)
    vn_tz = timezone(timedelta(hours=7))
    start_of_today = datetime.combine(now_utc.astimezone(vn_tz).date(), time.min).replace(tzinfo=vn_tz)

    msgs = []
    # Quét qua toàn bộ ID kênh trong cấu hình
    for ch_id in TARGET_CHANNELS:
        ch = bot.get_channel(ch_id)
        if ch:
            # Lấy tin nhắn của từng kênh và gom chung vào mảng msgs
            ch_msgs = await fetch_channel_messages(ch, limit, after=start_of_today)
            msgs.extend(ch_msgs)
            
    from src.services.unanswered_service import filter_unanswered_messages
    from src.services.clustering_service import cluster_messages
    raw = {
        "unanswered_over_2h": filter_unanswered_messages(msgs),
        "top_issues": cluster_messages(msgs).get("top_issues", [])
    }
    save_to_cache(raw)
    return filter_resolved_from_results(raw)

async def process_messages_and_send(interaction: discord.Interaction, is_clustering: bool) -> None:
    """Xử lý yêu cầu phân tích và hiển thị kết quả phân trang."""
    await interaction.response.defer()
    try:
        res = await get_or_run_analysis(bot, limit=50)
        if is_clustering:
            embed = build_topics_summary_embed(res.get("top_issues", []))
            await interaction.followup.send(embed=embed)
        else:
            messages = res.get("unanswered_over_2h", [])
            view = MessagePaginationView(messages, title_prefix="Tin chưa trả lời")
            await interaction.followup.send(embed=view.get_embed(), view=view)
    except Exception as e:
        await interaction.followup.send(f"Đã xảy ra lỗi: {str(e)}")

@bot.tree.command(name="test_fetch", description="Test quét tin nhắn từ 00:00 hôm nay")
@app_commands.default_permissions(manage_messages=True)
async def test_fetch(interaction: discord.Interaction) -> None:
    """Quét tin nhắn thử nghiệm từ đầu ngày."""
    await interaction.response.defer(ephemeral=True)
    now_utc = datetime.now(timezone.utc)
    vn_tz = timezone(timedelta(hours=7))
    start = datetime.combine(now_utc.astimezone(vn_tz).date(), time.min).replace(tzinfo=vn_tz)
    fetched = await fetch_discord_messages(bot, time_from=start, time_to=None)
    missed = [m for m in fetched if not m["is_replied"]]
    rep = f"📊 **QUÉT 00:00**\n- Học viên: {len(fetched)}\n- Chưa rep: {len(missed)}"
    if missed:
        rep += "\n**🚨 Tin bị Miss:**\n" + "\n".join(
            f"{i+1}. #{m['channel_name']}: {m['author']} [Link]({m['jump_url']})"
            for i, m in enumerate(missed[:5])
        )
    await interaction.followup.send(rep)

@bot.tree.command(name="tonghop", description="[Dành cho TA] Tổng hợp tin nhắn trong ngày hôm nay")
@app_commands.default_permissions(manage_messages=True) 
async def tonghop(interaction: discord.Interaction) -> None:
    """Lệnh slash /tonghop tổng hợp tin nhắn."""
    await process_messages_and_send(interaction, is_clustering=True)

@bot.tree.command(name="checkmiss", description="[Dành cho TA] Check tin nhắn chưa rep")
@app_commands.default_permissions(manage_messages=True)
async def checkmiss(interaction: discord.Interaction) -> None:
    """Lệnh slash /checkmiss lọc tin chưa trả lời."""
    await process_messages_and_send(interaction, is_clustering=False)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
    """Xử lý lỗi phân quyền và lỗi hệ thống."""
    orig = getattr(error, 'original', error)
    if isinstance(orig, discord.errors.NotFound) and orig.code == 10062:
        return
    msg = "❌ Chỉ TA mới được phép dùng lệnh này!" if isinstance(error, app_commands.MissingPermissions) else "❌ Lỗi hệ thống!"
    send = interaction.followup.send if interaction.response.is_done() else interaction.response.send_message
    await send(msg, ephemeral=True)

TOKEN = os.getenv('DISCORD_TOKEN')
if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("LỖI: Không tìm thấy DISCORD_TOKEN. Hãy kiểm tra lại file .env")