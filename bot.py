from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging

# ---------------- LOGGING ----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ---------------- BOT TOKEN ----------------
BOT_TOKEN = "8811166827:AAGKP6pA6u8y7aXxzZE76CjGEkyx7Jj-VfI"

# ---------------- EXAM LINK ----------------
EXAM_LINK = "https://radiant-cheesecake-c7b897.netlify.app/"

# ---------------- START COMMAND ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name

    message = f"""
👋 ሰላም {user_name}!

እንኳን ወደ Practice Only በደህና መጡ።

📝 ፈተናውን ለመጀመር ከታች ያለውን ሊንክ ይጠቀሙ፦

{EXAM_LINK}

🚀 መልካም ዕድል!
"""
    
    await update.message.reply_text(message)

# ---------------- HELP COMMAND ----------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"📝 ፈተናውን ለመጀመር:\n{EXAM_LINK}"
    )

# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    print("✅ Bot Started Successfully")

    app.run_polling(drop_pending_updates=True)

# ---------------- RUN BOT ----------------
if __name__ == "__main__":
    main()