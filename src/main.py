import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv # Thêm thư viện này
from datetime import datetime, time, timezone, timedelta

from discord_fetcher import fetch_discord_messages 

load_dotenv() # Tải các biến môi trường từ file .env

# Cấu hình Intents để đọc được tin nhắn
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Khởi tạo bot với tiền tố lệnh là "!" (Ví dụ: !ask)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync() 
    print(f'Bot {bot.user} đã online và sẵn sàng test CP2!')

# --- BẮT ĐẦU FLOW CHÍNH (DATA GIẢ) ---
@bot.tree.command(name="test_fetch", description="Test quét tin nhắn từ 00:00 hôm nay")
@app_commands.default_permissions(manage_messages=True)
async def test_fetch(interaction: discord.Interaction):
    # Báo cho Discord biết bot đang xử lý (vì kéo tin nhắn mất vài giây)
    await interaction.response.defer(ephemeral=True)

    # Lấy thời gian 00:00 của ngày hôm nay (Theo giờ Việt Nam UTC+7)
    now_utc = datetime.now(timezone.utc)
    vn_timezone = timezone(timedelta(hours=7))
    now_vn = now_utc.astimezone(vn_timezone)
    
    # Set giờ về 00:00:00
    start_of_day_vn = datetime.combine(now_vn.date(), time.min).replace(tzinfo=vn_timezone)

    # GỌI MODULE CỦA BẠN Ở ĐÂY
    fetched_data = await fetch_discord_messages(bot, time_from=start_of_day_vn, time_to=None)
    print(f"✅ Đã quét xong tin nhắn từ 00:00 đến hiện tại. Tổng số tin nhắn học viên: {fetched_data}")
    # Đếm số tin nhắn miss
    missed_messages = [msg for msg in fetched_data if not msg["is_replied"]]

    # Bàn giao (In ra mock data để kiểm tra)
    report = (
        f"📊 **BÁO CÁO QUÉT TIN NHẮN TỪ 00:00**\n"
        f"- Tổng số tin học viên đã hỏi: **{len(fetched_data)}**\n"
        f"- Số tin nhắn CHƯA CÓ TA TRẢ LỜI: **{len(missed_messages)}**\n\n"
    )
    
    if len(missed_messages) > 0:
        report += "**🚨 Danh sách tin nhắn bị Miss:**\n"
        
        # Chỉ lấy tối đa 5 tin để in ra
        so_tin_hien_thi = len(missed_messages)
        for i, msg in enumerate(missed_messages[:so_tin_hien_thi]): 
            report += f"{i+1}. Kênh #{msg['channel_name']} - {msg['author']}: *{msg['content'][:30]}...* [Bấm để xem]({msg['jump_url']})\n"
            
        # Nếu tổng số tin miss lớn hơn 5, báo cho TA biết còn nữa
        tin_bi_an = len(missed_messages) - so_tin_hien_thi
        if tin_bi_an > 0:
            report += f"\n*... và **{tin_bi_an}** tin nhắn khác nữa. (Dùng AI tóm tắt để xem chi tiết)*"

    # Trả kết quả cho TA
    await interaction.followup.send(report)


@bot.tree.command(name="tonghop", description="[Dành cho TA] Tổng hợp tin nhắn")
@app_commands.default_permissions(manage_messages=True) 
async def tonghop(interaction: discord.Interaction):
    mock_data = "**[BÁO CÁO TA]** Có 15 tin nhắn quan trọng..."
    await interaction.response.send_message(mock_data)

@bot.tree.command(name="checkmiss", description="[Dành cho TA] Check tin nhắn chưa rep")
@app_commands.default_permissions(manage_messages=True)
async def checkmiss(interaction: discord.Interaction):
    await interaction.response.send_message("**[BÁO CÁO TA]** Có 2 tin nhắn miss!")

# --- XỬ LÝ LỖI KHI HỌC VIÊN CỐ TÌNH DÙNG LỆNH (Trượt thẩm quyền) ---
# --- XỬ LÝ LỖI CHUYÊN NGHIỆP ---
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    # Lấy lỗi gốc (nếu có)
    original_error = getattr(error, 'original', error)

    # Bỏ qua nếu lỗi là do mạng chậm / quá 3 giây (Unknown Interaction)
    if isinstance(original_error, discord.errors.NotFound) and original_error.code == 10062:
        print(f"⚠️ [CẢNH BÁO] Discord API timeout (quá 3s). Người dùng cần gõ lại lệnh.")
        return

    # Thông báo lỗi phân quyền
    if isinstance(error, app_commands.MissingPermissions):
        error_msg = "❌ Xin lỗi, chỉ Teaching Assistant (TA) mới được phép dùng lệnh này!"
    else:
        print(f"❌ Lỗi hệ thống: {original_error}")
        error_msg = "❌ Đã có lỗi xảy ra. Hãy báo cho team Dev kiểm tra log!"

    # Thử gửi tin nhắn lỗi cho user một cách an toàn
    try:
        if not interaction.response.is_done():
            await interaction.response.send_message(error_msg, ephemeral=True)
        else:
            await interaction.followup.send(error_msg, ephemeral=True)
    except Exception as e:
        print(f"⚠️ Không thể gửi báo lỗi cho user (Bot đã mất kết nối với tin nhắn này).")
        
TOKEN = os.getenv('DISCORD_TOKEN')

# Kiểm tra xem token có được load thành công không (phòng hờ bạn quên tạo file .env)
if TOKEN is None:
    print("LỖI: Không tìm thấy DISCORD_TOKEN. Hãy kiểm tra lại file .env")
else:
    bot.run(TOKEN)