# -*- coding: utf-8 -*-
"""Mô-đun giao diện người dùng hiển thị phân trang tin nhắn và xử lý tương tác."""

import discord
from typing import List, Dict, Any
from codebase.services.resolve_service import save_resolved_id

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


class TopicPaginationView(discord.ui.View):
    """View phân trang hiển thị từng chủ đề thắc mắc, mỗi trang một chủ đề."""

    MAX_MESSAGES_PER_PAGE = 4

    def __init__(self, top_issues: List[Dict[str, Any]]):
        super().__init__(timeout=180)
        self.top_issues = top_issues
        self.current_index = 0
        self.update_buttons()

    def update_buttons(self) -> None:
        """Cập nhật trạng thái hiển thị của các nút phân trang."""
        self.children[0].disabled = (self.current_index == 0)
        self.children[1].disabled = (self.current_index >= len(self.top_issues) - 1)

    def get_embed(self) -> discord.Embed:
        """Tạo đối tượng Embed mô tả chi tiết chủ đề hiện tại."""
        if not self.top_issues:
            return discord.Embed(
                title="Chủ đề thắc mắc",
                description="Không có chủ đề nào cần tổng hợp!",
                color=discord.Color.green()
            )

        issue = self.top_issues[self.current_index]
        topic = issue.get("topic", "Không rõ chủ đề")
        messages = issue.get("messages", [])
        shown = messages[:self.MAX_MESSAGES_PER_PAGE]

        lines = []
        for i, m in enumerate(shown):
            mark = "✅ " if m.get("is_replied") else ""
            lines.append(f"{mark}{i + 1}. **{m['author']}** (#{m['channel_name']}): {m['content'][:150]} [Link]({m['jump_url']})")
        remaining = len(messages) - len(shown)
        if remaining > 0:
            lines.append(f"... còn {remaining} tin nữa trong chủ đề này")

        embed = discord.Embed(
            title=topic,
            description="\n".join(lines) if lines else "Không có tin nhắn.",
            color=discord.Color.blue()
        )
        embed.set_footer(
            text=f"Chủ đề {self.current_index + 1}/{len(self.top_issues)} · ✅ = đã trả lời"
        )
        return embed

    @discord.ui.button(label="◀ Trước", style=discord.ButtonStyle.grey)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Xử lý sự kiện nút Trước được bấm."""
        if self.current_index > 0:
            self.current_index -= 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Sau ▶", style=discord.ButtonStyle.grey)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Xử lý sự kiện nút Sau được bấm."""
        if self.current_index < len(self.top_issues) - 1:
            self.current_index += 1
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)
