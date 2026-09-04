# ---------------------------------------------------
# File Name: start.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: VoidXDevs
# Telegram: https://t.me/VoidXDevs
# Created: 2025-01-11
# Last Modified: 2026-09-04
# Version: 2.1.0
# License: MIT License
# ---------------------------------------------------

import asyncio
from pyrogram import filters, Client
from devgagan import app
from config import OWNER_ID
from pyrogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, 
    BotCommand, LabeledPrice, PreCheckoutQuery, Message
)
from pyrogram.raw.functions.bots import SetBotInfo
from pyrogram.raw.types import InputUserSelf

# CONFIGURATION FOR PAYMENTS & BRANDING
UPI_ID = "your_upi_id@okaxis"  # Change to your real UPI ID
QR_CODE_URL = "https://yourdomain.com/path_to_qr.jpg"  # Direct image URL of your UPI QR code

# ---------------------------------------------------
# COMMAND SETTER
# ---------------------------------------------------
@app.on_message(filters.command("set"))
async def set(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply("You are not authorized to use this command.")
        return
      
    await app.set_bot_commands([
        BotCommand("start", "🚀 Start the bot"),
        BotCommand("batch", "🫠 Extract in bulk"),
        BotCommand("login", "🔑 Get into the bot"),
        BotCommand("logout", "🚪 Get out of the bot"),
        BotCommand("token", "🎲 Get 3 hours free access"),
        BotCommand("adl", "👻 Download audio from 30+ sites"),
        BotCommand("dl", "💀 Download videos from 30+ sites"),
        BotCommand("freez", "🧊 Remove all expired user"),
        BotCommand("pay", "₹ Pay now to get subscription"),
        BotCommand("status", "⟳ Refresh Payment status"),
        BotCommand("transfer", "💘 Gift premium to others"),
        BotCommand("myplan", "⌛ Get your plan details"),
        BotCommand("add", "➕ Add user to premium"),
        BotCommand("rem", "➖ Remove from premium"),
        BotCommand("session", "🧵 Generate Pyrogramv2 session"),
        BotCommand("settings", "⚙️ Personalize things"),
        BotCommand("stats", "📊 Get stats of the bot"),
        BotCommand("plan", "🗓️ Check our premium plans"),
        BotCommand("terms", "🥺 Terms and conditions"),
        BotCommand("speedtest", "🚅 Speed of server"),
        BotCommand("lock", "🔒 Protect channel from extraction"),
        BotCommand("gcast", "⚡ Broadcast message to bot users"),
        BotCommand("help", "❓ Help & Command List"),
        BotCommand("cancel", "🚫 Cancel batch process")
    ])

    await message.reply("✅ Commands configured successfully by **VoidXDevs**!")


# ---------------------------------------------------
# HELP SECTION
# ---------------------------------------------------
help_pages = [
    (
        "📝 **Bot Commands Overview (1/2)**:\n\n"
        "1. **/add userID**\n"
        "> Add user to premium (Owner only)\n\n"
        "2. **/rem userID**\n"
        "> Remove user from premium (Owner only)\n\n"
        "3. **/transfer userID**\n"
        "> Transfer premium to your beloved major purpose for resellers (Premium members only)\n\n"
        "4. **/get**\n"
        "> Get all user IDs (Owner only)\n\n"
        "5. **/lock**\n"
        "> Lock channel from extraction (Owner only)\n\n"
        "6. **/dl link**\n"
        "> Download videos (Not available in v3 if you are using)\n\n"
        "7. **/adl link**\n"
        "> Download audio (Not available in v3 if you are using)\n\n"
        "8. **/login**\n"
        "> Log into the bot for private channel access\n\n"
        "9. **/batch**\n"
        "> Bulk extraction for posts (After login)\n\n"
    ),
    (
        "📝 **Bot Commands Overview (2/2)**:\n\n"
        "10. **/logout**\n"
        "> Logout from the bot\n\n"
        "11. **/stats**\n"
        "> Get bot stats\n\n"
        "12. **/plan**\n"
        "> Check premium plans\n\n"
        "13. **/speedtest**\n"
        "> Test the server speed (not available in v3)\n\n"
        "14. **/terms**\n"
        "> Terms and conditions\n\n"
        "15. **/cancel**\n"
        "> Cancel ongoing batch process\n\n"
        "16. **/myplan**\n"
        "> Get details about your plans\n\n"
        "17. **/session**\n"
        "> Generate Pyrogram V2 session\n\n"
        "18. **/settings**\n"
        "> 1. SETCHATID : To directly upload in channel or group or user's dm use it with -100[chatID]\n"
        "> 2. SETRENAME : To add custom rename tag or username of your channels\n"
        "> 3. CAPTION : To add custom caption\n"
        "> 4. REPLACEWORDS : Can be used for words in deleted set via REMOVE WORDS\n"
        "> 5. RESET : To set the things back to default\n\n"
        "> You can set CUSTOM THUMBNAIL, PDF WATERMARK, VIDEO WATERMARK, SESSION-based login, etc. from settings\n\n"
        "**__Powered by VoidXDevs__**"
    )
]


async def send_or_edit_help_page(_, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return

    prev_button = InlineKeyboardButton("◀️ Previous", callback_data=f"help_prev_{page_number}")
    next_button = InlineKeyboardButton("Next ▶️", callback_data=f"help_next_{page_number}")

    buttons = []
    if page_number > 0:
        buttons.append(prev_button)
    if page_number < len(help_pages) - 1:
        buttons.append(next_button)

    keyboard = InlineKeyboardMarkup([buttons])

    await message.delete()

    await message.reply(
        help_pages[page_number],
        reply_markup=keyboard
    )


@app.on_message(filters.command("help"))
async def help(client, message):
    join = await subscribe(client, message)
    if join == 1:
        return

    await send_or_edit_help_page(client, message, 0)


@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = callback_query.data.split("_")[1], int(callback_query.data.split("_")[2])

    if action == "prev":
        page_number -= 1
    elif action == "next":
        page_number += 1

    await send_or_edit_help_page(client, callback_query.message, page_number)
    await callback_query.answer()


# ---------------------------------------------------
# TERMS & CONDITIONS
# ---------------------------------------------------
@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
        "✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion.\n\n"
        "**__Powered by VoidXDevs__**"
    )
      
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Support", url="https://t.me/VoidXDevs")],
        ]
    )
    await message.reply_text(terms_text, reply_markup=buttons)


@app.on_callback_query(filters.regex("see_terms"))
async def see_terms(client, callback_query):
    terms_text = (
        "> 📜 **Terms and Conditions** 📜\n\n"
        "✨ We are not responsible for user deeds, and we do not promote copyrighted content. If any user engages in such activities, it is solely their responsibility.\n"
        "✨ Upon purchase, we do not guarantee the uptime, downtime, or the validity of the plan. __Authorization and banning of users are at our discretion; we reserve the right to ban or authorize users at any time.__\n"
        "✨ Payment to us **__does not guarantee__** authorization for the /batch command. All decisions regarding authorization are made at our discretion.\n\n"
        "**__Powered by VoidXDevs__**"
    )
      
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📋 See Plans", callback_data="see_plan")],
            [InlineKeyboardButton("💬 Contact Support", url="https://t.me/VoidXDevs")],
        ]
    )
    await callback_query.message.edit_text(terms_text, reply_markup=buttons)


# ---------------------------------------------------
# PLAN & PAYMENT SYSTEM (VoidXDevs Flow)
# ---------------------------------------------------
def get_main_plan_keyboard():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("💳 Pay via UPI", callback_data="pay_upi_options")],
            [InlineKeyboardButton("⭐ Pay via Telegram Stars", callback_data="pay_stars_options")],
            [InlineKeyboardButton("📜 See Terms", callback_data="see_terms")],
            [InlineKeyboardButton("💬 Contact Support", url="https://t.me/VoidXDevs")]
        ]
    )

@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    plan_text = (
        "> 💰 **VoidXDevs Premium Plans**:\n\n"
        "Choose your preferred payment method below:\n"
        "• **UPI Payment** (Instant QR / UPI ID)\n"
        "• **Telegram Stars** (Direct In-App Purchase)\n\n"
        "📥 **Download Limit**: Up to 100,000 files in a single batch.\n"
        "🛑 **Batch Modes**: Access to `/bulk` and `/batch` commands.\n\n"
        "📜 **Terms and Conditions**: Please check `/terms` before payment."
    )
    await message.reply_text(plan_text, reply_markup=get_main_plan_keyboard())


@app.on_callback_query(filters.regex("see_plan"))
async def see_plan(client, callback_query):
    plan_text = (
        "> 💰 **VoidXDevs Premium Plans**:\n\n"
        "Choose your preferred payment method below:\n"
        "• **UPI Payment** (Instant QR / UPI ID)\n"
        "• **Telegram Stars** (Direct In-App Purchase)\n\n"
        "📥 **Download Limit**: Up to 100,000 files in a single batch.\n"
        "🛑 **Batch Modes**: Access to `/bulk` and `/batch` commands.\n\n"
        "📜 **Terms and Conditions**: Please check `/terms` before payment."
    )
    await callback_query.message.edit_text(plan_text, reply_markup=get_main_plan_keyboard())


# --- UPI PAYMENT OPTION ---
@app.on_callback_query(filters.regex("pay_upi_options"))
async def pay_upi_options(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("1 Month - ₹200", callback_data="upi_plan_1")],
        [InlineKeyboardButton("3 Months - ₹500", callback_data="upi_plan_3")],
        [InlineKeyboardButton("1 Year - ₹1500", callback_data="upi_plan_12")],
        [InlineKeyboardButton("⬅️ Back to Methods", callback_data="see_plan")]
    ])
    await callback_query.message.edit_text("🇮🇳 **Select a UPI Premium Plan:**", reply_markup=buttons)


@app.on_callback_query(filters.regex(r"upi_plan_(\d+)"))
async def show_upi_details(client, callback_query):
    months = callback_query.data.split("_")[2]
    prices = {"1": "200", "3": "500", "12": "1500"}
    amount = prices.get(months, "200")

    upi_text = (
        f"💳 **VoidXDevs UPI Payment Details**\n\n"
        f"📌 **Plan**: {months} Month(s) Premium\n"
        f"💵 **Amount**: ₹{amount}\n\n"
        f"🆔 **UPI ID**: `{UPI_ID}`\n\n"
        f"⚠️ **Instructions**:\n"
        f"1. Pay ₹{amount} to the UPI ID or scan the QR Code.\n"
        f"2. After payment, click the **'📸 Send Screenshot'** button below.\n"
        f"3. Upload your payment screenshot. Approval takes up to 24 hours."
    )

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 Send Screenshot to Admin", callback_data="send_screenshot_info")],
        [InlineKeyboardButton("⬅️ Back to UPI Plans", callback_data="pay_upi_options")]
    ])

    try:
        await callback_query.message.delete()
        await client.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=QR_CODE_URL,
            caption=upi_text,
            reply_markup=buttons
        )
    except Exception:
        await callback_query.message.edit_text(upi_text, reply_markup=buttons)


@app.on_callback_query(filters.regex("send_screenshot_info"))
async def send_screenshot_info(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.answer("Please send your payment screenshot directly in this chat!", show_alert=True)
    await callback_query.message.reply_text(
        f"📸 **Send your payment screenshot here.**\n\n"
        f"Your Telegram Numeric ID: `{user_id}`\n"
        f"Once sent, our admins will verify it within **24 hours** and activate your subscription."
    )


# --- SCREENSHOT FORWARDING TO ADMIN ---
@app.on_message(filters.photo & filters.private)
async def handle_screenshot(client, message: Message):
    user = message.from_user
    admin_caption = (
        f"📥 **New Payment Screenshot Received!**\n\n"
        f"👤 **User**: {user.mention}\n"
        f"🆔 **Numeric User ID**: `{user.id}`\n"
        f"🏷️ **Username**: @{user.username if user.username else 'N/A'}\n\n"
        f"📌 Verify payment and add user using `/add {user.id}`"
    )
    
    # Send screenshot to primary owner
    try:
        primary_owner = OWNER_ID[0] if isinstance(OWNER_ID, list) else OWNER_ID
        await client.send_photo(
            chat_id=primary_owner,
            photo=message.photo.file_id,
            caption=admin_caption
        )
        await message.reply_text(
            "✅ **Screenshot received!** Our admins will verify your payment within **24 hours**."
        )
    except Exception as e:
        await message.reply_text("❌ Error sending screenshot to admin. Please contact support @VoidXDevs.")


# --- TELEGRAM STARS PAYMENT OPTION ---
@app.on_callback_query(filters.regex("pay_stars_options"))
async def pay_stars_options(client, callback_query):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("1 Month - 100 ⭐️", callback_data="buy_stars_1_100")],
        [InlineKeyboardButton("3 Months - 250 ⭐️", callback_data="buy_stars_3_250")],
        [InlineKeyboardButton("1 Year - 800 ⭐️", callback_data="buy_stars_12_800")],
        [InlineKeyboardButton("⬅️ Back to Methods", callback_data="see_plan")]
    ])
    await callback_query.message.edit_text("⭐ **Select a Telegram Stars Plan:**", reply_markup=buttons)


@app.on_callback_query(filters.regex(r"buy_stars_(\d+)_(\d+)"))
async def send_stars_invoice(client, callback_query):
    _, _, months, stars = callback_query.data.split("_")
    
    title = f"VoidXDevs {months} Month(s) Premium"
    description = f"Get premium access to bulk downloads for {months} month(s)."
    payload = f"stars_plan_{months}_{callback_query.from_user.id}"
    currency = "XTR"
    prices = [LabeledPrice("Premium Subscription", int(stars))]

    await client.send_invoice(
        chat_id=callback_query.message.chat.id,
        title=title,
        description=description,
        payload=payload,
        currency=currency,
        prices=prices,
        start_parameter="voidxdevs-premium"
    )
    await callback_query.answer()


@app.on_pre_checkout_query()
async def pre_checkout_handler(client, query: PreCheckoutQuery):
    await query.answer(ok=True)


@app.on_message(filters.successful_payment)
async def successful_payment_handler(client, message: Message):
    payment = message.successful_payment
    user = message.from_user
    payload = payment.invoice_payload
    months = payload.split("_")[2] if "stars_plan" in payload else "1"

    receipt_user = (
        f"🧾 **VoidXDevs Official Purchase Receipt**\n\n"
        f"👤 **Customer**: {user.mention}\n"
        f"🆔 **User ID**: `{user.id}`\n"
        f"📦 **Plan**: {months} Month(s) Premium\n"
        f"💰 **Paid**: {payment.total_amount} Telegram Stars ⭐️\n"
        f"📑 **Transaction ID**: `{payment.telegram_payment_charge_id}`\n\n"
        f"✅ Payment Verified Successfully! Your request has been logged for auto-approval."
    )
    
    receipt_admin = (
        f"🌟 **New Telegram Stars Payment Received!**\n\n"
        f"👤 **User**: {user.mention}\n"
        f"🆔 **Numeric User ID**: `{user.id}`\n"
        f"📦 **Plan**: {months} Month(s) Premium\n"
        f"💰 **Paid**: {payment.total_amount} Stars ⭐️\n"
        f"📑 **Charge ID**: `{payment.telegram_payment_charge_id}`\n\n"
        f"📌 Execute command: `/add {user.id}`"
    )

    await message.reply_text(receipt_user)

    try:
        primary_owner = OWNER_ID[0] if isinstance(OWNER_ID, list) else OWNER_ID
        await client.send_message(chat_id=primary_owner, text=receipt_admin)
    except Exception:
        pass
