from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

ADMIN_ID = 7971660348

NAME, PHONE, PASSWORD, SCREENSHOT = range(4)


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Welcome to Practice Only!\n\n"
        "Please enter your full name:"
    )

    return NAME


# NAME
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["name"] = update.message.text

    button = KeyboardButton(
        text="Share Phone Number",
        request_contact=True
    )

    reply_markup = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "Please share your phone number:",
        reply_markup=reply_markup
    )

    return PHONE


# PHONE
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        phone = update.message.text

    context.user_data["phone"] = phone

    await update.message.reply_text(
        "Create your password:"
    )

    return PASSWORD


# PASSWORD
async def get_password(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["password"] = update.message.text

    payment_text = """
Registration Fee: 290 Birr

Choose Payment Method

1. CBE
Account Name: Rakeb Shiferaw
Account Number: 1000711346205

2. Addis Bank
Account Name: Rakeb Shiferaw
Account Number: 2000123456789

3. Telebirr
Account Name: Rakeb Shiferaw
Phone Number: 0990306961

After payment, send payment screenshot.
"""

    await update.message.reply_text(payment_text)

    return SCREENSHOT


# SCREENSHOT
async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.photo:

        photo = update.message.photo[-1]

        user = update.message.from_user

        user_id = user.id

        caption = f"""
NEW PAYMENT RECEIVED

Name: {context.user_data['name']}
Phone: {context.user_data['phone']}

USERNAME:
@{user.username}

USER ID:
{user_id}

To approve:
/approve {user_id}

To reject:
/reject {user_id}
"""

        # SEND TO ADMIN
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo.file_id,
            caption=caption
        )

        await update.message.reply_text(
            "Payment submitted successfully!\n\n"
            "Admin will verify your payment."
        )

    else:

        await update.message.reply_text(
            "Please send payment screenshot."
        )

        return SCREENSHOT

    return ConversationHandler.END


# APPROVE
async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id != ADMIN_ID:
        return

    try:

        user_id = int(context.args[0])

        await context.bot.send_message(
            chat_id=user_id,
            text="Your payment has been approved!\n\nYou can now access the platform."
        )

        await update.message.reply_text(
            "User approved successfully."
        )

    except:

        await update.message.reply_text(
            "Usage:\n/approve USER_ID"
        )


# REJECT
async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.from_user.id != ADMIN_ID:
        return

    try:

        user_id = int(context.args[0])

        await context.bot.send_message(
            chat_id=user_id,
            text="Your payment was rejected.\nPlease send valid payment proof."
        )

        await update.message.reply_text(
            "User rejected successfully."
        )

    except:

        await update.message.reply_text(
            "Usage:\n/reject USER_ID"
        )


# CANCEL
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Registration cancelled."
    )

    return ConversationHandler.END


# MAIN
def main():

    TOKEN = "8784148016:AAGG05v-PFTwHy3oAL8mMWdmnDU-IizpN10"

    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(

        entry_points=[
            CommandHandler("start", start)
        ],

        states={

            NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_name
                )
            ],

            PHONE: [
                MessageHandler(
                    filters.CONTACT | (filters.TEXT & ~filters.COMMAND),
                    get_phone
                )
            ],

            PASSWORD: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND,
                    get_password
                )
            ],

            SCREENSHOT: [
                MessageHandler(
                    filters.PHOTO,
                    get_screenshot
                )
            ],
        },

        fallbacks=[
            CommandHandler("cancel", cancel)
        ],
    )

    app.add_handler(conv_handler)

    # ADMIN COMMANDS
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("reject", reject))

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()