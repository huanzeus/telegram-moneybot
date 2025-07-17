import telebot
from utils import save_transaction, get_summary
from chart import draw_summary_chart

TOKEN = "7623058416:AAGuBeZk0RIO2K77AFlCq2uJjuq3fSiIOMc"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Xin chào! Gửi /help để xem hướng dẫn sử dụng bot.")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "📌 Gửi tin nhắn theo định dạng:\n"
        "`+100000` để ghi thu nhập\n"
        "`-50000` để ghi chi tiêu\n\n"
        "📊 Xem thống kê:\n"
        "`/week` - trong tuần\n"
        "`/month` - trong tháng\n"
        "`/year` - trong năm"
    )
    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['week', 'month', 'year'])
def send_summary(message):
    period = message.text[1:]
    summary = get_summary(message.from_user.id, period)
    chart = draw_summary_chart(summary)
    bot.send_photo(message.chat.id, chart)

@bot.message_handler(func=lambda m: True)
def log_transaction(message):
    try:
        amount = int(message.text.strip())
        save_transaction(message.from_user.id, amount)
        msg = f"✅ Đã lưu {'thu nhập' if amount > 0 else 'chi tiêu'}: {abs(amount):,}đ"
        bot.reply_to(message, msg)
    except:
        bot.reply_to(message, "❌ Vui lòng nhập số hợp lệ. Ví dụ: +100000 hoặc -50000")

bot.polling()
