import logging
import datetime
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from db import init_db, add_transaction, get_transactions
from chart import draw_summary_chart

TOKEN = "7623058416:AAGuBeZk0RIO2K77AFlCq2uJjuq3fSiIOMc"

logging.basicConfig(level=logging.INFO)
init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Chào mừng bạn đến với Bot Thống kê chi tiêu!\n\nDùng:\n+ 50000 Lương\n- 20000 Cafe\n\n/week /month /year để xem thống kê.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id
    today = datetime.date.today().isoformat()

    if text.startswith('+') or text.startswith('-'):
        sign = 'income' if text.startswith('+') else 'expense'
        try:
            parts = text[1:].strip().split(" ", 1)
            amount = int(parts[0])
            note = parts[1] if len(parts) > 1 else ''
            add_transaction(user_id, today, sign, amount, note)
            await update.message.reply_text("✅ Ghi lại thành công!")
        except:
            await update.message.reply_text("❌ Định dạng sai. Dùng: + 50000 Lương hoặc - 20000 Cafe")
    else:
        await update.message.reply_text("❗ Dùng: + 100000 Tiền thưởng hoặc - 30000 Ăn trưa")

async def summary(update: Update, context: ContextTypes.DEFAULT_TYPE, range_days):
    user_id = update.effective_user.id
    today = datetime.date.today()
    start = today - datetime.timedelta(days=range_days)

    data = get_transactions(user_id, start.isoformat(), today.isoformat())
    if not data:
        await update.message.reply_text("Không có dữ liệu.")
        return

    income = sum(row[2] for row in data if row[1] == "income")
    expense = sum(row[2] for row in data if row[1] == "expense")
    balance = income - expense

    msg = f"📊 Thống kê:\n\n🔹 Tổng thu: {income:,}đ\n🔸 Tổng chi: {expense:,}đ\n💰 Còn lại: {balance:,}đ"
    draw_summary_chart(data)
    await update.message.reply_photo(photo=InputFile("chart.png"), caption=msg)

async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await summary(update, context, 7)

async def month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await summary(update, context, 30)

async def year(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await summary(update, context, 365)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("week", week))
app.add_handler(CommandHandler("month", month))
app.add_handler(CommandHandler("year", year))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

app.run_polling()