# discord_fetcher.py
import discord
from config import TARGET_CHANNELS, TA_ROLE_IDS

async def fetch_discord_messages(bot: discord.Client, time_from, time_to):
    """
    Kéo tin nhắn từ các kênh được chỉ định trong khoảng thời gian.
    Trả về danh sách các dict chứa dữ liệu tin nhắn thô.
    """
    raw_messages = []

    for channel_id in TARGET_CHANNELS:
        channel = bot.get_channel(channel_id)
        if not channel:
            print(f"Cảnh báo: Không tìm thấy kênh ID {channel_id}")
            continue

        print(f"Đang quét kênh: #{channel.name}...")

        # 1. Kéo toàn bộ lịch sử tin nhắn trong khoảng thời gian
        # (Chỉ dùng time_from (after), vì ta muốn quét từ 00:00 đến hiện tại)
        messages_in_range = [msg async for msg in channel.history(after=time_from, before=time_to, limit=500)]
        
        # Tạo một từ điển để lưu trạng thái các tin nhắn (dễ bề cập nhật is_replied)
        msg_dict = {}

        for msg in messages_in_range:
            # print(f"{msg}")
            # Bỏ qua tin nhắn do Bot gửi
            if msg.author.bot:
                continue
                
            # Xác định xem người gửi có phải là TA không
            is_sender_ta = False
            if hasattr(msg.author, 'roles'): # Tránh lỗi nếu user đã rời server
                # Lấy danh sách ID các role của người gửi
                user_role_ids = [role.id for role in msg.author.roles]
                
                # Check xem có khớp với TA_ROLE_IDS trong config không
                is_sender_ta = any(r_id in TA_ROLE_IDS for r_id in user_role_ids)
                
                # ------ THÊM DÒNG NÀY ĐỂ DEBUG ------
                print(f"🕵️ Check User: {msg.author.display_name} | Các Role ID đang có: {user_role_ids} | Có phải TA không? -> {is_sender_ta}")

            msg_dict[msg.id] = {
                "message_id": msg.id,
                "channel_name": channel.name,
                "author": msg.author.display_name,
                "is_ta": is_sender_ta,
                "content": msg.content,
                "created_at": msg.created_at,
                "jump_url": msg.jump_url, # Link bấm vào nhảy tới tin nhắn
                "is_replied": False
            }

        # 2. Xử lý logic is_replied (Quét lại danh sách vừa tạo)
        for msg in messages_in_range:
            if msg.author.bot:
                continue

            # Check 1: Nếu đây là một tin nhắn TA DÙNG TÍNH NĂNG REPLY người khác
            if msg.reference and msg.reference.message_id in msg_dict:
                # Nếu người reply là TA
                if hasattr(msg.author, 'roles') and any(role.id in TA_ROLE_IDS for role in msg.author.roles):
                    msg_dict[msg.reference.message_id]["is_replied"] = True

            # Check 2: Nếu tin nhắn này CÓ TẠO THREAD (Luồng)
            if msg.thread:
                # Kéo lịch sử chat trong thread đó
                thread_msgs = [t_msg async for t_msg in msg.thread.history(limit=50)]
                for t_msg in thread_msgs:
                    if hasattr(t_msg.author, 'roles') and any(role.id in TA_ROLE_IDS for role in t_msg.author.roles):
                        msg_dict[msg.id]["is_replied"] = True
                        break # Chỉ cần 1 TA trả lời là đủ, thoát vòng lặp thread

        # 3. Lọc lại kết quả: Chỉ lấy tin nhắn của Học viên (Không lấy tin nhắn TA hỏi/thông báo)
        for key, data in msg_dict.items():
            if not data["is_ta"]:
                raw_messages.append(data)

    return raw_messages