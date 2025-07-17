import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from utils import save_transaction, get_summary
from chart import draw_summary_chart

# Thiết lập token bot Telegram (đã thêm token của bạn)
TOKEN = "7623058416:AAGuBeZk0RIO2K77AFlCq2uJjuq3fSiIOMc"

# Bật logging để debug nếu cần
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Xử lý tin nhắn người dùng nhập tiền thu/chi
async def handle_transaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.startswith('+') or text.startswith('-'):
        save_transaction(update.message.chat_id, text)
        await update.message.reply_text("✅ Đã lưu giao dịch!")
    else:
        await update.message.reply_text(
            "❗ Vui lòng nhập đúng định dạng:\n"
            "`+100000 Lương` để thu\n"
            "`-50000 Ăn sáng` để chi",
            parse_mode="Markdown"
        )

# Xử lý lệnh thống kê theo tuần, tháng, năm
async def show_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text[1:].lower()  # week / month / year
    summary_text, chart_data = get_summary(update.message.chat_id, mode=cmd)
    await update.message.reply_text(summary_text)
    
    # Gửi biểu đồ nếu có dữ liệu
    chart = draw_summary_chart(chart_data, mode=cmd)
    if chart:
        await update.message.reply_photo(photo=chart)

# Khởi chạy bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    # Xử lý tin nhắn thu/chi
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_transaction))

    # Các lệnh thống kê
    app.add_handler(CommandHandler("week", show_summary))
    app.add_handler(CommandHandler("month", show_summary))
    app.add_handler(CommandHandler("year", show_summary))

    # Bắt đầu chạy bot
    print("🤖 Bot đang chạy...")
    app.run_polling()
