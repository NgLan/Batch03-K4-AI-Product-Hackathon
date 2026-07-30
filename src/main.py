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
    print(f'Bot {bot.user} đã online và sẵn sàng test CP2!')

# --- BẮT ĐẦU FLOW CHÍNH (DATA GIẢ) ---
@bot.command()
async def ask(ctx, *, question: str = None):
    # Nếu user chỉ gõ "!ask" mà không có câu hỏi
    if not question:
        await ctx.send("Bạn cần nhập câu hỏi nhé! Ví dụ: `!ask tài liệu buổi 1 ở đâu?`")
        return

    # In log ra terminal để quan sát
    print(f"User {ctx.author} vừa hỏi: {question}")
    
    # TRẢ VỀ DỮ LIỆU GIẢ (Mock) - Chưa gọi AI
    mock_reply = (
        f"**[MOCK AI]** Chào {ctx.author.name}, mình nhận được câu hỏi: *'{question}'*.\n\n"
        "*(Đây là text hardcode - Ở CP3 chỗ này sẽ là kết quả sinh ra từ Gemini/OpenAI)*.\n"
        "Tài liệu buổi 1 bạn có thể tìm thấy tại link ghim trên kênh #tai-lieu nhé!"
    )
    
    await ctx.send(mock_reply)

# Chạy bot (Thay YOUR_TOKEN_HERE bằng Token bạn copy ở Bước 2)
# Khuyến cáo: Trong thực tế nên dùng os.environ.get('DISCORD_TOKEN') thay vì dán cứng token.
TOKEN = os.getenv('DISCORD_TOKEN')

# Kiểm tra xem token có được load thành công không (phòng hờ bạn quên tạo file .env)
if TOKEN is None:
    print("LỖI: Không tìm thấy DISCORD_TOKEN. Hãy kiểm tra lại file .env")
else:
    bot.run(TOKEN)