# -*- coding: utf-8 -*-
"""Mô-đun giao diện người dùng hiển thị phân trang tin nhắn và xử lý tương tác."""

import discord
from typing import List, Dict, Any
from src.services.resolve_service import save_resolved_id

class MessagePaginationView(discord.ui.View):
    """View phân trang hiển thị tin nhắn Discord kèm nút Đã giải quyết."""

    def __init__(self, messages: List[Dict[str, Any]], title_prefix: str = "Tin nhắn"):
        super().__init__(timeout=180)
        self.messages = messages
        self.title_prefix = title_prefix
        self.current_index = 0
        self.update_buttons()

    def update_buttons(self) -> None:
        """Cập nhật trạng thái hiển thị của các nút phân trang."""
        self.children[0].disabled = (self.current_index == 0)
        self.children[2].disabled = (self.current_index >= len(self.messages) - 1)
        self.children[1].disabled = (len(self.messages) == 0)

    def get_embed(self) -> discord.Embed:
        """Tạo đối tượng Embed mô tả chi tiết tin nhắn hiện tại."""
        if not self.messages:
            return discord.Embed(
                title="Hoàn thành", 
                description="Không còn tin nhắn nào cần xử lý!", 
                color=discord.Color.green()
            )
        
        msg = self.messages[self.current_index]
        embed = discord.Embed(
            title=f"{self.title_prefix} ({self.current_index + 1}/{len(self.messages)})",
            color=discord.Color.blue()
        )
        if "topic" in msg:
            embed.add_field(name="Chủ đề", value=msg["topic"], inline=False)
        embed.add_field(name="Người gửi", value=msg["author"], inline=True)
        embed.add_field(name="Kênh", value=msg["channel_name"], inline=True)
        embed.add_field(name="Nội dung", value=msg["content"], inline=False)
        embed.description = f"[Link đến tin nhắn]({msg['jump_url']})"
        return embed

    @discord.ui.button(label="◀ Trước", style=discord.ButtonStyle.grey)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Xử lý sự kiện nút Trước được bấm."""
        if self.current_index > 0:
            self.current_index -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Mark as Resolved", style=discord.ButtonStyle.green)
    async def resolve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Xử lý sự kiện đánh dấu đã trả lời thủ công."""
        if not self.messages:
            return
            
        current_msg = self.messages[self.current_index]
        save_resolved_id(current_msg["message_id"])
        self.messages.pop(self.current_index)
        
        if self.current_index >= len(self.messages) and self.current_index > 0:
            self.current_index -= 1
            
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Sau ▶", style=discord.ButtonStyle.grey)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Xử lý sự kiện nút Sau được bấm."""
        if self.current_index < len(self.messages) - 1:
            self.current_index += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
