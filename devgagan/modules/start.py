# ---------------------------------------------------
# File Name: start.py
# Description: Pyrogram bot for downloading files and
#              handling Telegram Stars + UPI payments.
# Author: VoidXDevs
# Telegram: https://t.me/VoidXDevs
# Created: 2025-01-11
# Last Modified: 2026-09-04
# Version: 2.2.0
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


# ===================================================
# PAYMENT CONFIGURATION
# ===================================================

# Put your real UPI ID here
UPI_ID = "chaudhary18shiva@okaxis"

# Direct URL of your UPI QR image
QR_CODE_URL = "https://raw.githubusercontent.com/DevXShiva/Save-Restricted-Bot/refs/heads/main/logo.png"


# ===================================================
# PREMIUM PLAN CONFIGURATION
# ===================================================

# UPI plans
UPI_PLANS = {
    "1": {
        "name": "1 Month",
        "months": 1,
        "amount": 200
    },
    "3": {
        "name": "3 Months",
        "months": 3,
        "amount": 500
    },
    "12": {
        "name": "1 Year",
        "months": 12,
        "amount": 1500
    }
}

# Telegram Stars plans
STARS_PLANS = {
    "1": {
        "name": "1 Month",
        "months": 1,
        "stars": 100
    },
    "3": {
        "name": "3 Months",
        "months": 3,
        "stars": 250
    },
    "12": {
        "name": "1 Year",
        "months": 12,
        "stars": 800
    }
}


# ===================================================
# HELPER FUNCTIONS
# ===================================================

def get_primary_owner():
    """Return primary owner ID."""
    if isinstance(OWNER_ID, (list, tuple)):
        return OWNER_ID[0]
    return OWNER_ID


def get_main_plan_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "💳 Pay via UPI",
                    callback_data="pay_upi_options"
                )
            ],
            [
                InlineKeyboardButton(
                    "⭐ Pay via Telegram Stars",
                    callback_data="pay_stars_options"
                )
            ],
            [
                InlineKeyboardButton(
                    "📜 See Terms",
                    callback_data="see_terms"
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 Contact Support",
                    url="https://t.me/VoidXDevs"
                )
            ]
        ]
    )


def get_upi_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "1 Month - ₹200",
                    callback_data="upi_plan_1"
                )
            ],
            [
                InlineKeyboardButton(
                    "3 Months - ₹500",
                    callback_data="upi_plan_3"
                )
            ],
            [
                InlineKeyboardButton(
                    "1 Year - ₹1500",
                    callback_data="upi_plan_12"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Back to Methods",
                    callback_data="see_plan"
                )
            ]
        ]
    )


def get_stars_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "1 Month - 100 ⭐",
                    callback_data="buy_stars_1"
                )
            ],
            [
                InlineKeyboardButton(
                    "3 Months - 250 ⭐",
                    callback_data="buy_stars_3"
                )
            ],
            [
                InlineKeyboardButton(
                    "1 Year - 800 ⭐",
                    callback_data="buy_stars_12"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Back to Methods",
                    callback_data="see_plan"
                )
            ]
        ]
    )


# ===================================================
# COMMAND SETTER
# ===================================================

@app.on_message(filters.command("set"))
async def set_commands(_, message):
    if message.from_user.id not in OWNER_ID:
        await message.reply(
            "You are not authorized to use this command."
        )
        return

    await app.set_bot_commands(
        [
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
        ]
    )

    await message.reply(
        "✅ Commands configured successfully by **VoidXDevs**!"
    )


# ===================================================
# HELP SECTION
# ===================================================

help_pages = [
    (
        "📝 **Bot Commands Overview (1/2):**\n\n"
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
        "> Bulk extraction for posts (After login)\n"
    ),

    (
        "📝 **Bot Commands Overview (2/2):**\n\n"

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
        "> Personalize your settings\n\n"

        "**__Powered by VoidXDevs__**"
    )
]


async def send_or_edit_help_page(client, message, page_number):
    if page_number < 0 or page_number >= len(help_pages):
        return

    buttons = []

    if page_number > 0:
        buttons.append(
            InlineKeyboardButton(
                "◀️ Previous",
                callback_data=f"help_prev_{page_number}"
            )
        )

    if page_number < len(help_pages) - 1:
        buttons.append(
            InlineKeyboardButton(
                "Next ▶️",
                callback_data=f"help_next_{page_number}"
            )
        )

    keyboard = InlineKeyboardMarkup([buttons]) if buttons else None

    try:
        await message.delete()
    except Exception:
        pass

    await message.reply(
        help_pages[page_number],
        reply_markup=keyboard
    )


@app.on_message(filters.command("help"))
async def help_command(client, message):
    # Keep your existing subscribe() function if it exists
    try:
        join = await subscribe(client, message)
        if join == 1:
            return
    except NameError:
        pass

    await send_or_edit_help_page(client, message, 0)


@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):
    action, page_number = (
        callback_query.data.split("_")[1],
        int(callback_query.data.split("_")[2])
    )

    if action == "prev":
        page_number -= 1
    else:
        page_number += 1

    await send_or_edit_help_page(
        client,
        callback_query.message,
        page_number
    )

    await callback_query.answer()


# ===================================================
# TERMS & CONDITIONS
# ===================================================

def get_terms_text():
    return (
        "> 📜 **Terms and Conditions** 📜\n\n"

        "✨ We are not responsible for user deeds, and we do not "
        "promote copyrighted content. If any user engages in such "
        "activities, it is solely their responsibility.\n\n"

        "✨ Upon purchase, we do not guarantee the uptime, downtime, "
        "or the validity of the plan. __Authorization and banning of "
        "users are at our discretion; we reserve the right to ban or "
        "authorize users at any time.__\n\n"

        "✨ Payment to us **__does not guarantee__** authorization "
        "for the /batch command. All decisions regarding "
        "authorization are made at our discretion.\n\n"

        "**__Powered by VoidXDevs__**"
    )


def get_terms_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📋 See Plans",
                    callback_data="see_plan"
                )
            ],
            [
                InlineKeyboardButton(
                    "💬 Contact Support",
                    url="https://t.me/VoidXDevs"
                )
            ]
        ]
    )


@app.on_message(filters.command("terms") & filters.private)
async def terms(client, message):
    await message.reply_text(
        get_terms_text(),
        reply_markup=get_terms_keyboard()
    )


@app.on_callback_query(filters.regex("^see_terms$"))
async def see_terms(client, callback_query):
    await callback_query.message.edit_text(
        get_terms_text(),
        reply_markup=get_terms_keyboard()
    )

    await callback_query.answer()


# ===================================================
# PLAN SYSTEM
# ===================================================

def get_plan_text():
    return (
        "> 💰 **VoidXDevs Premium Plans**\n\n"

        "Choose your preferred payment method below:\n\n"

        "🇮🇳 **UPI Payment**\n"
        "• 1 Month — ₹200\n"
        "• 3 Months — ₹500\n"
        "• 1 Year — ₹1500\n\n"

        "⭐ **Telegram Stars**\n"
        "• 1 Month — 100 ⭐\n"
        "• 3 Months — 250 ⭐\n"
        "• 1 Year — 800 ⭐\n\n"

        "📥 **Download Limit:** Up to 100,000 files in a single batch.\n"
        "🛑 **Batch Modes:** Access to `/bulk` and `/batch` commands.\n\n"

        "📜 Please check `/terms` before payment."
    )


@app.on_message(filters.command("plan") & filters.private)
async def plan(client, message):
    await message.reply_text(
        get_plan_text(),
        reply_markup=get_main_plan_keyboard()
    )


@app.on_callback_query(filters.regex("^see_plan$"))
async def see_plan(client, callback_query):
    await callback_query.message.edit_text(
        get_plan_text(),
        reply_markup=get_main_plan_keyboard()
    )

    await callback_query.answer()


# ===================================================
# UPI PAYMENT
# ===================================================

@app.on_callback_query(filters.regex("^pay_upi_options$"))
async def pay_upi_options(client, callback_query):
    await callback_query.message.edit_text(
        "🇮🇳 **Select a UPI Premium Plan:**\n\n"
        "Choose the plan you want to purchase.",
        reply_markup=get_upi_keyboard()
    )

    await callback_query.answer()


@app.on_callback_query(filters.regex(r"^upi_plan_(1|3|12)$"))
async def show_upi_details(client, callback_query):
    plan_id = callback_query.data.split("_")[2]

    plan_data = UPI_PLANS.get(plan_id)

    if not plan_data:
        await callback_query.answer(
            "❌ Invalid plan selected.",
            show_alert=True
        )
        return

    plan_name = plan_data["name"]
    amount = plan_data["amount"]
    months = plan_data["months"]

    # -----------------------------------------------
    # QR IMAGE CAPTION
    # -----------------------------------------------

    upi_caption = (
        "💳 **VoidXDevs UPI Payment**\n\n"

        f"📦 **Plan:** {plan_name} Premium\n"
        f"💰 **Amount:** ₹{amount}\n"
        f"🆔 **UPI ID:** `{UPI_ID}`\n\n"

        "📌 **Payment Instructions:**\n"
        f"1. Pay exactly **₹{amount}** using the QR code or UPI ID.\n"
        "2. After payment, take a screenshot of the successful payment.\n"
        "3. Send the screenshot in this chat.\n\n"

        "⏳ Your payment will be verified by our admin."
    )

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📸 Send Payment Screenshot",
                    callback_data=f"send_screenshot_{plan_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "⬅️ Back to UPI Plans",
                    callback_data="pay_upi_options"
                )
            ]
        ]
    )

    await callback_query.answer()

    try:
        # Delete old plan-selection message
        await callback_query.message.delete()

        # Send QR image with selected plan's details
        await client.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=QR_CODE_URL,
            caption=upi_caption,
            reply_markup=buttons
        )

    except Exception as e:
        # If QR image fails, still show payment details
        fallback_text = (
            upi_caption +
            "\n\n⚠️ QR image could not be loaded. "
            "Please use the UPI ID above."
        )

        try:
            await callback_query.message.edit_text(
                fallback_text,
                reply_markup=buttons
            )
        except Exception:
            pass


# ===================================================
# UPI SCREENSHOT BUTTON
# ===================================================

@app.on_callback_query(filters.regex(r"^send_screenshot_(1|3|12)$"))
async def send_screenshot_info(client, callback_query):
    plan_id = callback_query.data.split("_")[2]
    plan_data = UPI_PLANS.get(plan_id)

    if not plan_data:
        await callback_query.answer(
            "❌ Invalid plan.",
            show_alert=True
        )
        return

    await callback_query.answer(
        "Please send your payment screenshot in this chat.",
        show_alert=True
    )

    await callback_query.message.reply_text(
        "📸 **Send your payment screenshot here.**\n\n"

        f"📦 **Selected Plan:** {plan_data['name']} Premium\n"
        f"💰 **Amount:** ₹{plan_data['amount']}\n"
        f"🆔 **Your Telegram ID:** `{callback_query.from_user.id}`\n\n"

        "Once received, our admin will verify your payment "
        "and activate your subscription."
    )


# ===================================================
# UPI SCREENSHOT FORWARDING
# ===================================================

@app.on_message(filters.photo & filters.private)
async def handle_screenshot(client, message: Message):
    user = message.from_user

    admin_caption = (
        "📥 **New Payment Screenshot Received!**\n\n"

        f"👤 **User:** {user.mention}\n"
        f"🆔 **Numeric User ID:** `{user.id}`\n"
        f"🏷️ **Username:** "
        f"@{user.username if user.username else 'N/A'}\n\n"

        f"📌 Verify payment and add user using:\n"
        f"`/add {user.id}`"
    )

    primary_owner = get_primary_owner()

    try:
        await client.send_photo(
            chat_id=primary_owner,
            photo=message.photo.file_id,
            caption=admin_caption
        )

        await message.reply_text(
            "✅ **Screenshot received!**\n\n"
            "Our admins will verify your payment within "
            "**24 hours**."
        )

    except Exception:
        await message.reply_text(
            "❌ Error sending screenshot to admin.\n\n"
            "Please contact support @VoidXDevs."
        )


# ===================================================
# TELEGRAM STARS PAYMENT
# ===================================================

@app.on_callback_query(filters.regex("^pay_stars_options$"))
async def pay_stars_options(client, callback_query):
    await callback_query.message.edit_text(
        "⭐ **Select a Telegram Stars Premium Plan:**\n\n"
        "Choose a plan below. After selecting it, "
        "Telegram's official Stars payment invoice will open.",
        reply_markup=get_stars_keyboard()
    )

    await callback_query.answer()


@app.on_callback_query(filters.regex(r"^buy_stars_(1|3|12)$"))
async def send_stars_invoice(client, callback_query):
    plan_id = callback_query.data.split("_")[2]

    plan_data = STARS_PLANS.get(plan_id)

    if not plan_data:
        await callback_query.answer(
            "❌ Invalid Stars plan.",
            show_alert=True
        )
        return

    months = plan_data["months"]
    plan_name = plan_data["name"]
    stars = plan_data["stars"]

    user_id = callback_query.from_user.id

    # Unique payload for this user and plan
    payload = f"stars_plan_{plan_id}_{user_id}"

    title = f"VoidXDevs {plan_name} Premium"

    description = (
        f"Premium subscription for {months} month(s). "
        f"Price: {stars} Telegram Stars."
    )

    prices = [
        LabeledPrice(
            label=f"{plan_name} Premium",
            amount=stars
        )
    ]

    try:
        # Telegram Stars currency
        await client.send_invoice(
            chat_id=callback_query.message.chat.id,
            title=title,
            description=description,
            payload=payload,
            currency="XTR",
            prices=prices,
            start_parameter=f"voidxdevs-{plan_id}"
        )

        await callback_query.answer(
            f"⭐ Payment invoice created for {stars} Stars."
        )

    except Exception as e:
        await callback_query.answer(
            "❌ Unable to create payment invoice.",
            show_alert=True
        )


# ===================================================
# TELEGRAM STARS PRE-CHECKOUT
# ===================================================

@app.on_pre_checkout_query()
async def pre_checkout_handler(client, query: PreCheckoutQuery):
    try:
        await query.answer(ok=True)
    except Exception:
        pass


# ===================================================
# TELEGRAM STARS SUCCESSFUL PAYMENT
# ===================================================

@app.on_message(filters.successful_payment)
async def successful_payment_handler(client, message: Message):
    payment = message.successful_payment
    user = message.from_user

    payload = payment.invoice_payload

    # -----------------------------------------------
    # Extract selected plan from payload
    # payload format:
    # stars_plan_1_USERID
    # stars_plan_3_USERID
    # stars_plan_12_USERID
    # -----------------------------------------------

    plan_id = None

    if payload.startswith("stars_plan_"):
        parts = payload.split("_")

        if len(parts) >= 4:
            plan_id = parts[2]

    plan_data = STARS_PLANS.get(plan_id)

    if plan_data:
        plan_name = plan_data["name"]
        months = plan_data["months"]
        stars = plan_data["stars"]
    else:
        plan_name = "Unknown"
        months = 1
        stars = payment.total_amount

    transaction_id = payment.telegram_payment_charge_id

    # -----------------------------------------------
    # USER RECEIPT
    # -----------------------------------------------

    receipt_user = (
        "🧾 **VoidXDevs Official Purchase Receipt**\n\n"

        f"👤 **Customer:** {user.mention}\n"
        f"🆔 **User ID:** `{user.id}`\n"
        f"📦 **Plan:** {plan_name} Premium\n"
        f"💰 **Paid:** {payment.total_amount} Telegram Stars ⭐\n"
        f"📑 **Transaction ID:** `{transaction_id}`\n\n"

        "✅ **Payment Verified Successfully!**\n"
        "Your payment has been received."
    )

    # -----------------------------------------------
    # ADMIN RECEIPT
    # -----------------------------------------------

    receipt_admin = (
        "🌟 **New Telegram Stars Payment Received!**\n\n"

        f"👤 **User:** {user.mention}\n"
        f"🆔 **Numeric User ID:** `{user.id}`\n"
        f"📦 **Plan:** {plan_name} Premium\n"
        f"💰 **Paid:** {payment.total_amount} Stars ⭐\n"
        f"📑 **Charge ID:** `{transaction_id}`\n\n"

        f"📌 Add premium using:\n"
        f"`/add {user.id}`"
    )

    # Send receipt to user
    await message.reply_text(receipt_user)

    # Send payment notification to owner
    try:
        await client.send_message(
            chat_id=get_primary_owner(),
            text=receipt_admin
        )
    except Exception:
        pass


# ===================================================
# OPTIONAL: /PAY COMMAND
# ===================================================

@app.on_message(filters.command("pay") & filters.private)
async def pay_command(client, message):
    await message.reply_text(
        get_plan_text(),
        reply_markup=get_main_plan_keyboard()
    )


# ===================================================
# END OF PAYMENT SYSTEM
# ===================================================
