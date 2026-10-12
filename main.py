import os
import re
import logging
import threading
import telebot
from flask import Flask
from telebot import types

# ==================== CONFIG ====================

TOKEN = "8989576551:AAGsY99JB81Wx7Th5ZsmCRsueb_hQsUhiXs"
if not TOKEN:
    raise RuntimeError("Missing TOKEN environment variable")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
log = logging.getLogger("ROFIX")

bot = telebot.TeleBot(TOKEN, threaded=True, num_threads=8)
app = Flask(__name__)

# ==================== HEALTH SERVER ====================

@app.route("/")
def home():
    return "ROFIX Bot is running", 200

@app.route("/health")
def health():
    return {"status": "ok", "bot": "ROFIX"}, 200

def keep_alive():
    threading.Thread(
        target=lambda: app.run(
            host="0.0.0.0",
            port=int(os.environ.get("PORT", "8080")),
            debug=False,
            use_reloader=False,
            threaded=True
        ),
        daemon=True
    ).start()

# ==================== KEYBOARDS ====================

def get_language_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("العربية 🇲🇦", callback_data="lang_ar"),
        types.InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")
    )
    return markup

def get_main_menu_ar():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📌 خدماتنا", callback_data="services_ar"),
        types.InlineKeyboardButton("💰 الأسعار", callback_data="prices_ar")
    )
    markup.add(
        types.InlineKeyboardButton("📞 الدعم والتواصل", callback_data="support_ar"),
        types.InlineKeyboardButton("🌐 تغيير اللغة", callback_data="change_lang")
    )
    return markup

def get_main_menu_en():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📌 Our Services", callback_data="services_en"),
        types.InlineKeyboardButton("💰 Pricing", callback_data="prices_en")
    )
    markup.add(
        types.InlineKeyboardButton("📞 Contact & Support", callback_data="support_en"),
        types.InlineKeyboardButton("🌐 Change Language", callback_data="change_lang")
    )
    return markup

# ==================== TEXTS ====================

MENU_TEXTS = {
    "services_ar": (
        "📌 **خدماتنا:**\n"
        "- إدارة وتأمين المجموعات والقنوات.\n"
        "- أتمتة الردود وإدارة طلبات العملاء.\n"
        "- تصاميم وحلول برمجية مخصصة."
    ),
    "services_en": (
        "📌 **Our Services:**\n"
        "- Group & Channel Management & Security.\n"
        "- Automated Replies & Customer Management.\n"
        "- Custom Graphic Design & Software Solutions."
    ),
    "prices_ar": (
        "💰 **الأسعار:**\n"
        "تواصل معنا للحصول على عرض سعر يناسب احتياجات مشروعك."
    ),
    "prices_en": (
        "💰 **Pricing:**\n"
        "Contact us to get a custom quote tailored for your project."
    ),
    "support_ar": (
        "📞 **الدعم والتواصل:**\n"
        "لأي استفسار يمكنك التواصل مع الإدارة مباشرة."
    ),
    "support_en": (
        "📞 **Support & Contact:**\n"
        "For any inquiries, feel free to contact the admin directly."
    )
}

# ==================== START / HELP ====================

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    try:
        bot.reply_to(
            message,
            "مرحباً بك في بوت ROFIX! 🤖\n"
            "الرجاء اختيار اللغة / Please select your language:",
            reply_markup=get_language_keyboard()
        )
    except Exception:
        log.exception("Welcome error")

# ==================== CALLBACKS ====================

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        log.warning("Callback acknowledgement failed")

    try:
        if not call.message:
            return

        chat_id = call.message.chat.id
        message_id = call.message.message_id

        menus = {
            "lang_ar": (
                "مرحباً بك في القائمة الرئيسية لـ **ROFIX**! "
                "اختر ما يناسبك من الأزرار أسفله 👇",
                get_main_menu_ar()
            ),
            "lang_en": (
                "Welcome to **ROFIX** Main Menu! "
                "Choose an option from below 👇",
                get_main_menu_en()
            ),
            "change_lang": (
                "الرجاء اختيار اللغة / Please select your language:",
                get_language_keyboard()
            )
        }

        if call.data in menus:
            text, keyboard = menus[call.data]
            try:
                bot.edit_message_text(
                    text, chat_id, message_id,
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
            except Exception:
                log.info("Menu unchanged or unavailable")
            return

        if call.data in MENU_TEXTS:
            bot.send_message(
                chat_id,
                MENU_TEXTS[call.data],
                parse_mode="Markdown"
            )

    except Exception:
        log.exception("Callback processing error")

# ==================== WELCOME MEMBERS ====================

@bot.message_handler(content_types=["new_chat_members"])
def welcome_new_member(message):
    for member in message.new_chat_members:
        name = member.first_name or "صديقنا"
        try:
            bot.send_message(
                message.chat.id,
                f"أهلاً بك يا {name} في المجموعة! 🖐️\n"
                "مرحباً بك معنا، نرجو الالتزام بقوانين المجموعة."
            )
        except Exception:
            log.exception("New member welcome error")

# ==================== ANTI-SPAM ====================

URL_PATTERN = re.compile(
    r"(?i)(?:https?://|www\.)[^\s<>]+"
    r"|(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)"
    r"[a-z]{2,}(?::\d+)?(?:/[^\s<>]*)?"
)

def contains_link(message):
    content = message.text or message.caption or ""
    if URL_PATTERN.search(content):
        return True

    entities = (
        getattr(message, "entities", None)
        or getattr(message, "caption_entities", None)
        or []
    )
    return any(
        entity.type in ("url", "text_link")
        for entity in entities
    )

@bot.message_handler(
    func=lambda m: (
        m.chat.type in ("group", "supergroup")
        and bool(m.text or m.caption)
    ),
    content_types=[
        "text", "photo", "video", "document",
        "animation", "audio", "voice", "video_note"
    ]
)
def anti_spam_links(message):
    if not message.from_user:
        return

    try:
        member = bot.get_chat_member(
            message.chat.id,
            message.from_user.id
        )
        if member.status in ("administrator", "creator"):
            return

        if not contains_link(message):
            return

        bot.delete_message(
            message.chat.id,
            message.message_id
        )

        username = (
            f"@{message.from_user.username}"
            if message.from_user.username
            else message.from_user.first_name or "عضو"
        )
        bot.send_message(
            message.chat.id,
            f"⚠️ تنبيه عزيزي {username}، "
            "يُمنع إرسال الروابط داخل المجموعة!"
        )

    except Exception:
        log.exception("Anti-spam error")

# ==================== START BOT ====================

def main():
    keep_alive()
    log.info("ROFIX is starting")

    bot.infinity_polling(
        timeout=30,
        long_polling_timeout=25,
        skip_pending=True,
        logger_level=logging.INFO
    )

if __name__ == "__main__":
    main()
    
