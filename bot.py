import telebot
from utils import save_transaction, get_summary
from chart import draw_summary_chart
import os

TOKEN = "7623058416:AAGuBeZk0RIO2K77AFlCq2uJjuq3fSiIOMc"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Chào mừng bạn đến với bot thống kê chi tiêu của Tường Nhí!\nGửi /help để xem hướng dẫn.")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_msg = (
        "📝 *Hướng dẫn sử dụng:*\n\n"
        "`+100000` — Ghi nhận *thu nhập*\n"
        "`-50000` — Ghi nhận *chi tiêu*\n\n"
        "📊 *Xem thống kê:*\n"
        "`/week` — Thống kê tuần\n"
        "`/month` — Thống kê tháng\n"
        "`/year` — Thống kê năm"
    )
    bot.reply_to(message, help_msg, parse_mode="Markdown")

@bot.message_handler(commands=['week', 'month', 'year'])
def send_chart(message):
    period = message.text[1:]  # bỏ dấu "/"
    summary = get_summary(message.from_user.id, period)
    if not summary:
        bot.reply_to(message, "Không có dữ liệu để thống kê.")
        return

    chart_path = draw_summary_chart(summary)
    with open(chart_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    os.remove(chart_path)

@bot.message_handler(func=lambda m: True)
def handle_transaction(message):
    try:
        amount = int(message.text.strip())
        save_transaction(message.from_user.id, amount)
        loai = "thu nhập" if amount > 0 else "chi tiêu"
        bot.reply_to(message, f"✅ Đã ghi {loai}: {abs(amount):,}đ")
    except:
        bot.reply_to(message, "❌ Lỗi: Gửi số tiền như `+100000` hoặc `-50000`.")

bot.polling()
