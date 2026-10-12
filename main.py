import telebot

# ضع التوكن الخاص ببوتك هنا بين العلامات
TOKEN = '8989576551:AAFLvMZ7AZosLY8T5AJ3HQAnDSkaCptXTZs'

bot = telebot.TeleBot(TOKEN)

# أمر القائمة الرئيسية
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    welcome_text = """✨ **أهلاً بك في بوت التواصل الرسمي لـ ROFIX** 🤖

إليك قائمة الأوامر المتاحة للتصفح:

📌 /start - القائمة الرئيسية
👑 /rofix - من هو ROFIX؟
🛠 /services - الخدمات المتاحة
📞 /contact - التواصل المباشر مع الدعم
⚡ /ping - فحص سرعة واستجابة البوت
❓ /help - طريقة الاستخدام والتعليمات

💡 *أو يمكنك إرسال رسالتك مباشرة وسنقوم بالرد عليك في أقرب وقت!*"""
    
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

# أمر تعريف بـ ROFIX
@bot.message_handler(commands=['rofix'])
def send_rofix_info(message):
    info_text = """👑 **حول ROFIX:**

مرحباً بك! أنا **ROFIX**، أقدم أفضل الحلول الرقمية والخدمات التقنية باحترافية وسرعة عالية. يسعدني تواصلك واهتمامك دائماً! ✨"""
    
    bot.reply_to(message, info_text, parse_mode="Markdown")

# أمر الخدمات
@bot.message_handler(commands=['services'])
def send_services(message):
    services_text = """🛠 **خدمات ROFIX:**

• خدمات وتطوير البوتات الذكية 🤖
• الدعم الفني والاستشارات التقنية 💻
• تصميم وإدارة الحسابات الرقمية 🎨

📩 لأي طلب خاص، أرسل تفاصيل طلبك مباشرة هنا!"""
    
    bot.reply_to(message, services_text, parse_mode="Markdown")

# أمر التواصل
@bot.message_handler(commands=['contact'])
def send_contact(message):
    contact_text = """📞 **التواصل المباشر:**

يمكنك كتابة رسالتك الآن في الشات وسيتم تحويلها مباشرة إلى **ROFIX** للرد عليك في أقرب وقت ممكن. 🚀"""
    
    bot.reply_to(message, contact_text, parse_mode="Markdown")

# أمر فحص حالة البوت
@bot.message_handler(commands=['ping'])
def send_ping(message):
    bot.reply_to(message, "⚡ **البوت يعمل بنجاح وبسرعة ممتازة!** 🚀", parse_mode="Markdown")

# أمر المساعدة
@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """❓ **دليل المساعدة:**

• استخدم الأوامر الموضحة في القائمة لجمع المعلومات.
• لإرسال استفسار أو رسالة خاصة، اكتبها مباشرة وستصلنا فوراً."""
    
    bot.reply_to(message, help_text, parse_mode="Markdown")

# الرد التلقائي على باقي الرسائل العادية
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_name = message.from_user.first_name
    
    auto_reply = f"""مرحباً بك يا {user_name} 👋

لقد توصلنا برسالتك بنجاح في منصة **ROFIX** 🛡️
شكراً لتواصلك معنا، سنقوم بمراجعتها والرد عليك في أقرب وقت! ✨"""
    
    bot.reply_to(message, auto_reply, parse_mode="Markdown")

print("Bot is running...")
bot.infinity_polling()
