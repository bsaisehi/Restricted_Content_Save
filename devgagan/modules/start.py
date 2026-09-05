# ---------------------------------------------------
# File Name: start.py
# Description: Pyrogram bot for downloading files and
#              handling Telegram Stars + UPI payments.
# Author: VoidXDevs
# Telegram: https://t.me/VoidXDevs
# Created: 2025-01-11
# Last Modified: 2026-09-05
# Version: 2.3.0
# License: MIT License
# ---------------------------------------------------

import asyncio

from pyrogram import filters, Client
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    BotCommand,
    LabeledPrice,
    PreCheckoutQuery,
    Message
)

from devgagan import app
from config import OWNER_ID


# ===================================================
# PAYMENT CONFIGURATION
# ===================================================

# Put your real UPI ID here
UPI_ID = "your_upi_id@okaxis"

# Direct URL of your UPI QR image
QR_CODE_URL = (
    "https://raw.githubusercontent.com/"
    "DevXShiva/Save-Restricted-Bot/"
    "refs/heads/main/logo.png"
)


# ===================================================
# PREMIUM PLAN CONFIGURATION
# ===================================================

# ---------------------------------------------------
# UPI PLANS
# ---------------------------------------------------

UPI_PLANS = {
    "1": {
        "name": "1 Day",
        "days": 1,
        "amount": 10
    },
    "7": {
        "name": "7 Days",
        "days": 7,
        "amount": 60
    },
    "30": {
        "name": "30 Days",
        "days": 30,
        "amount": 150
    }
}


# ---------------------------------------------------
# TELEGRAM STARS PLANS
# ---------------------------------------------------

STARS_PLANS = {
    "1": {
        "name": "1 Day",
        "days": 1,
        "stars": 10
    },
    "7": {
        "name": "7 Days",
        "days": 7,
        "stars": 50
    },
    "30": {
        "name": "30 Days",
        "days": 30,
        "stars": 150
    }
}


# ===================================================
# TEMPORARY UPI PAYMENT STATE
# ===================================================

# Stores the selected UPI plan for users who clicked
# "Send Payment Screenshot".
#
# Example:
# {
#     123456789: "7"
# }
#
# Note:
# This is in-memory and resets when the bot restarts.

pending_upi_plans = {}


# ===================================================
# HELPER FUNCTIONS
# ===================================================

def get_primary_owner():
    """Return primary owner ID safely."""

    if isinstance(OWNER_ID, (list, tuple)):
        return OWNER_ID[0]

    return OWNER_ID


def is_owner(user_id):
    """Check whether a user is an owner."""

    if isinstance(OWNER_ID, (list, tuple, set)):
        return user_id in OWNER_ID

    return user_id == OWNER_ID


# ===================================================
# MAIN PAYMENT KEYBOARD
# ===================================================

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


# ===================================================
# UPI PLAN KEYBOARD
# ===================================================

def get_upi_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "1 Day - ₹10",
                    callback_data="upi_plan_1"
                )
            ],
            [
                InlineKeyboardButton(
                    "7 Days - ₹60",
                    callback_data="upi_plan_7"
                )
            ],
            [
                InlineKeyboardButton(
                    "30 Days - ₹150",
                    callback_data="upi_plan_30"
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
# TELEGRAM STARS PLAN KEYBOARD
# ===================================================

def get_stars_keyboard():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "1 Day - 10 ⭐",
                    callback_data="buy_stars_1"
                )
            ],
            [
                InlineKeyboardButton(
                    "7 Days - 50 ⭐",
                    callback_data="buy_stars_7"
                )
            ],
            [
                InlineKeyboardButton(
                    "30 Days - 150 ⭐",
                    callback_data="buy_stars_30"
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

    if not message.from_user:
        return

    if not is_owner(message.from_user.id):
        await message.reply(
            "❌ You are not authorized to use this command."
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
            BotCommand("rem", "➖ Remove user from premium"),
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
        "> Transfer premium to your beloved major purpose "
        "for resellers (Premium members only)\n\n"

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

    keyboard = (
        InlineKeyboardMarkup([buttons])
        if buttons
        else None
    )

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

    try:
        join = await subscribe(client, message)

        if join == 1:
            return

    except NameError:
        pass

    await send_or_edit_help_page(
        client,
        message,
        0
    )


@app.on_callback_query(filters.regex(r"help_(prev|next)_(\d+)"))
async def on_help_navigation(client, callback_query):

    parts = callback_query.data.split("_")

    action = parts[1]
    page_number = int(parts[2])

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
        "• 1 Day — ₹10\n"
        "• 7 Days — ₹60\n"
        "• 30 Days — ₹150\n\n"

        "⭐ **Telegram Stars**\n"
        "• 1 Day — 10 ⭐\n"
        "• 7 Days — 50 ⭐\n"
        "• 30 Days — 150 ⭐\n\n"

        "📥 **Download Limit:** "
        "Up to 100,000 files in a single batch.\n"

        "🛑 **Batch Modes:** "
        "Access to `/bulk` and `/batch` commands.\n\n"

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

        "Choose the plan you want to purchase.\n\n"

        "💰 **Available Plans:**\n"
        "• 1 Day — ₹10\n"
        "• 7 Days — ₹60\n"
        "• 30 Days — ₹150",
        
        reply_markup=get_upi_keyboard()
    )

    await callback_query.answer()


# ===================================================
# SHOW UPI PAYMENT DETAILS
# ===================================================

@app.on_callback_query(
    filters.regex(r"^upi_plan_(1|7|30)$")
)
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
    days = plan_data["days"]

    upi_caption = (
        "💳 **VoidXDevs UPI Payment**\n\n"

        f"📦 **Plan:** {plan_name} Premium\n"
        f"⏳ **Duration:** {days} Day(s)\n"
        f"💰 **Amount:** ₹{amount}\n"
        f"🆔 **UPI ID:** `{UPI_ID}`\n\n"

        "📌 **Payment Instructions:**\n"
        f"1. Pay exactly **₹{amount}** using the QR code "
        "or UPI ID.\n"
        "2. After payment, take a screenshot of the "
        "successful payment.\n"
        "3. Click **Send Payment Screenshot** below.\n\n"

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

        await callback_query.message.delete()

        await client.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=QR_CODE_URL,
            caption=upi_caption,
            reply_markup=buttons
        )

    except Exception:

        fallback_text = (
            upi_caption +
            "\n\n⚠️ QR image could not be loaded.\n"
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

@app.on_callback_query(
    filters.regex(r"^send_screenshot_(1|7|30)$")
)
async def send_screenshot_info(client, callback_query):

    plan_id = callback_query.data.split("_")[2]

    plan_data = UPI_PLANS.get(plan_id)

    if not plan_data:
        await callback_query.answer(
            "❌ Invalid plan.",
            show_alert=True
        )
        return

    user_id = callback_query.from_user.id

    # Save selected plan temporarily
    pending_upi_plans[user_id] = plan_id

    await callback_query.answer(
        "Please send your payment screenshot in this chat.",
        show_alert=True
    )

    await callback_query.message.reply_text(
        "📸 **Send your payment screenshot here.**\n\n"

        f"📦 **Selected Plan:** "
        f"{plan_data['name']} Premium\n"

        f"⏳ **Duration:** "
        f"{plan_data['days']} Day(s)\n"

        f"💰 **Amount:** "
        f"₹{plan_data['amount']}\n"

        f"🆔 **Your Telegram ID:** "
        f"`{user_id}`\n\n"

        "Once received, our admin will verify your payment "
        "and activate your subscription."
    )


# ===================================================
# UPI SCREENSHOT FORWARDING
# ===================================================

@app.on_message(filters.photo & filters.private)
async def handle_screenshot(client, message: Message):

    user = message.from_user

    if not user:
        return

    user_id = user.id

    # Get selected plan
    plan_id = pending_upi_plans.get(user_id)

    if plan_id:
        plan_data = UPI_PLANS.get(plan_id)
    else:
        plan_data = None

    # ------------------------------------------------
    # Plan information
    # ------------------------------------------------

    if plan_data:

        plan_name = plan_data["name"]
        days = plan_data["days"]
        amount = plan_data["amount"]

        plan_info = (
            f"📦 **Plan:** {plan_name} Premium\n"
            f"⏳ **Duration:** {days} Day(s)\n"
            f"💰 **Amount:** ₹{amount}\n\n"
        )

    else:

        plan_info = (
            "⚠️ **Plan:** Not detected\n"
            "⚠️ Please verify the payment amount manually.\n\n"
        )

    # ------------------------------------------------
    # Admin caption
    # ------------------------------------------------

    admin_caption = (
        "📥 **New UPI Payment Screenshot Received!**\n\n"

        f"👤 **User:** {user.mention}\n"
        f"🆔 **Numeric User ID:** `{user.id}`\n"
        f"🏷️ **Username:** "
        f"@{user.username if user.username else 'N/A'}\n\n"

        f"{plan_info}"

        "📌 **Action:**\n"
        f"Verify payment and add user using:\n"
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

            "Your payment screenshot has been sent to "
            "our admin for verification.\n\n"

            "⏳ Please wait up to **24 hours** for verification."
        )

        # Remove pending state after receiving screenshot
        pending_upi_plans.pop(user_id, None)

    except Exception:

        await message.reply_text(
            "❌ **Error sending screenshot to admin.**\n\n"

            "Please contact support @VoidXDevs."
        )


# ===================================================
# TELEGRAM STARS PAYMENT
# ===================================================

@app.on_callback_query(
    filters.regex("^pay_stars_options$")
)
async def pay_stars_options(client, callback_query):

    await callback_query.message.edit_text(
        "⭐ **Select a Telegram Stars Premium Plan:**\n\n"

        "Choose a plan below.\n\n"

        "⭐ **Available Plans:**\n"
        "• 1 Day — 10 ⭐\n"
        "• 7 Days — 50 ⭐\n"
        "• 30 Days — 150 ⭐\n\n"

        "After selecting a plan, Telegram's official "
        "Stars payment invoice will open.",

        reply_markup=get_stars_keyboard()
    )

    await callback_query.answer()


# ===================================================
# CREATE TELEGRAM STARS INVOICE
# ===================================================

@app.on_callback_query(
    filters.regex(r"^buy_stars_(1|7|30)$")
)
async def send_stars_invoice(client, callback_query):

    plan_id = callback_query.data.split("_")[2]

    plan_data = STARS_PLANS.get(plan_id)

    if not plan_data:
        await callback_query.answer(
            "❌ Invalid Stars plan.",
            show_alert=True
        )
        return

    days = plan_data["days"]
    plan_name = plan_data["name"]
    stars = plan_data["stars"]

    user_id = callback_query.from_user.id

    # Unique payload for this user and plan
    payload = (
        f"stars_plan_{plan_id}_{user_id}"
    )

    title = (
        f"VoidXDevs {plan_name} Premium"
    )

    description = (
        f"Premium subscription for {days} day(s). "
        f"Price: {stars} Telegram Stars."
    )

    prices = [
        LabeledPrice(
            label=f"{plan_name} Premium",
            amount=stars
        )
    ]

    try:

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

    except Exception:

        await callback_query.answer(
            "❌ Unable to create payment invoice.",
            show_alert=True
        )


# ===================================================
# TELEGRAM STARS PRE-CHECKOUT
# ===================================================

@app.on_pre_checkout_query()
async def pre_checkout_handler(
    client,
    query: PreCheckoutQuery
):

    try:
        await query.answer(ok=True)

    except Exception:
        pass


# ===================================================
# TELEGRAM STARS SUCCESSFUL PAYMENT
# ===================================================

@app.on_message(filters.successful_payment)
async def successful_payment_handler(
    client,
    message: Message
):

    payment = message.successful_payment
    user = message.from_user

    if not payment or not user:
        return

    payload = payment.invoice_payload

    # ------------------------------------------------
    # Extract plan from payload
    #
    # stars_plan_1_USERID
    # stars_plan_7_USERID
    # stars_plan_30_USERID
    # ------------------------------------------------

    plan_id = None

    if payload.startswith("stars_plan_"):

        parts = payload.split("_")

        if len(parts) >= 4:
            plan_id = parts[2]

    plan_data = STARS_PLANS.get(plan_id)

    # ------------------------------------------------
    # Validate payment
    # ------------------------------------------------

    if plan_data:

        plan_name = plan_data["name"]
        days = plan_data["days"]
        expected_stars = plan_data["stars"]

    else:

        plan_name = "Unknown"
        days = 0
        expected_stars = None

    paid_stars = payment.total_amount

    transaction_id = (
        payment.telegram_payment_charge_id
    )

    # ------------------------------------------------
    # Payment amount verification
    # ------------------------------------------------

    if expected_stars is not None:

        if paid_stars != expected_stars:

            warning_text = (
                "⚠️ **Payment Amount Mismatch**\n\n"

                f"Expected: **{expected_stars} ⭐**\n"
                f"Received: **{paid_stars} ⭐**\n\n"

                "Please contact support."
            )

            await message.reply_text(
                warning_text
            )

            try:

                await client.send_message(
                    chat_id=get_primary_owner(),
                    text=(
                        "🚨 **Stars Payment Mismatch!**\n\n"

                        f"👤 **User:** {user.mention}\n"
                        f"🆔 **User ID:** `{user.id}`\n"
                        f"📦 **Plan:** {plan_name}\n"
                        f"💰 **Expected:** "
                        f"{expected_stars} ⭐\n"
                        f"💰 **Received:** "
                        f"{paid_stars} ⭐\n"
                        f"📑 **Charge ID:** "
                        f"`{transaction_id}`"
                    )
                )

            except Exception:
                pass

            return

    # =================================================
    # USER RECEIPT
    # =================================================

    receipt_user = (
        "🧾 **VoidXDevs Official Purchase Receipt**\n\n"

        f"👤 **Customer:** {user.mention}\n"
        f"🆔 **User ID:** `{user.id}`\n"
        f"📦 **Plan:** {plan_name} Premium\n"
        f"⏳ **Duration:** {days} Day(s)\n"
        f"💰 **Paid:** "
        f"{paid_stars} Telegram Stars ⭐\n"
        f"📑 **Transaction ID:** "
        f"`{transaction_id}`\n\n"

        "✅ **Payment Verified Successfully!**\n"

        "Your Telegram Stars payment has been "
        "received successfully.\n\n"

        "⏳ Premium activation will be handled by "
        "our admin."
    )

    # =================================================
    # ADMIN RECEIPT
    # =================================================

    receipt_admin = (
        "🌟 **New Telegram Stars Payment Received!**\n\n"

        f"👤 **User:** {user.mention}\n"
        f"🆔 **Numeric User ID:** `{user.id}`\n"
        f"🏷️ **Username:** "
        f"@{user.username if user.username else 'N/A'}\n\n"

        f"📦 **Plan:** {plan_name} Premium\n"
        f"⏳ **Duration:** {days} Day(s)\n"
        f"💰 **Paid:** {paid_stars} Stars ⭐\n"
        f"📑 **Charge ID:** `{transaction_id}`\n\n"

        "📌 **Add Premium:**\n"
        f"`/add {user.id}`"
    )

    # Send receipt to user
    await message.reply_text(
        receipt_user
    )

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

@app.on_message(
    filters.command("pay") & filters.private
)
async def pay_command(client, message):

    await message.reply_text(
        get_plan_text(),
        reply_markup=get_main_plan_keyboard()
    )


# ===================================================
# END OF PAYMENT SYSTEM
# ===================================================
