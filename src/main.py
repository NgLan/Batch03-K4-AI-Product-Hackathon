import discord
from discord.ext import commands
import os
from dotenv import load_dotenv # Thêm thư viện này

load_dotenv() # Tải các biến môi trường từ file .env

# Cấu hình Intents để đọc được tin nhắn
intents = discord.Intents.default()
intents.message_content = True

# Khởi tạo bot với tiền tố lệnh là "!" (Ví dụ: !ask)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync() 
    print(f'Bot {bot.user} đã online và sẵn sàng test CP2!')

# --- BẮT ĐẦU FLOW CHÍNH (DATA GIẢ) ---
@bot.tree.command(name="tonghop", description="Tổng hợp các tin nhắn quan trọng trong ngày")
async def tonghop(interaction: discord.Interaction):
    # Trả về MOCK DATA cho CP2
    mock_data = (
        "**[MOCK] BÁO CÁO TỔNG HỢP TRONG NGÀY:**\n"
        "- Có 15 tin nhắn hỏi về bài tập Buổi 1.\n"
        "- Có 3 bạn xin nghỉ phép.\n"
        "*(Chỗ này ở CP3 AI sẽ tự đọc lịch sử và tóm tắt)*"
    )
    await interaction.response.send_message(mock_data)

@bot.tree.command(name="checkmiss", description="Tìm các tin nhắn chưa được TA trả lời")
async def checkmiss(interaction: discord.Interaction):
    await interaction.response.send_message("**[MOCK]** Có 2 tin nhắn của @HocVienA chưa ai rep từ 10:00 sáng nay!")

TOKEN = os.getenv('DISCORD_TOKEN')

# Kiểm tra xem token có được load thành công không (phòng hờ bạn quên tạo file .env)
if TOKEN is None:
    print("LỖI: Không tìm thấy DISCORD_TOKEN. Hãy kiểm tra lại file .env")
else:
    bot.run(TOKEN)