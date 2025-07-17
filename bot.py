import telebot
from utils import save_transaction, get_summary
from chart import draw_summary_chart

API_TOKEN = '7623058416:AAGuBeZk0RIO2K77AFlCq2uJjuq3fSiIOMc'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,
        "Chào mừng bạn đến với bot thống kê chi tiêu @tuongnhithongkechitieu!\n"
        "Bạn có thể nhập:\n"
        "`+100000 lương` để thêm thu nhập\n"
        "`-50000 ăn trưa` để ghi chi tiêu\n"
        "`/week`, `/month`, `/year` để xem thống kê",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['week', 'month', 'year'])
def send_summary(message):
    period = message.text[1:]
    summary = get_summary(period)
    chart = draw_summary_chart(summary["transactions"], period)
    caption = f"📊 Thống kê {period}:\n"
    caption += f"🟢 Thu nhập: {summary['income']:,} VND\n"
    caption += f"🔴 Chi tiêu: {summary['expense']:,} VND"
    bot.send_photo(message.chat.id, chart, caption=caption)

@bot.message_handler(func=lambda m: m.text)
def handle_transaction(message):
    text = message.text.strip()
    try:
        if text[0] not in ('+', '-'):
            raise ValueError("Dòng nhập phải bắt đầu bằng + hoặc -")

        parts = text[1:].strip().split(" ", 1)
        amount = int(parts[0])
        description = parts[1] if len(parts) > 1 else ""

        if text[0] == '+':
            save_transaction(amount, "income", description)
            bot.reply_to(message, f"✅ Đã ghi thu nhập: {amount} VND - {description}")
        else:
            save_transaction(amount, "expense", description)
            bot.reply_to(message, f"✅ Đã ghi chi tiêu: {amount} VND - {description}")

    except Exception as e:
        bot.reply_to(message, f"❌ Lỗi: {str(e)}")

bot.infinity_polling()
