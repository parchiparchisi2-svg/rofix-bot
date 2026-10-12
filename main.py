import telebot

TOKEN = '8989576551:AAFLvMZ7AZosLY8T5AJ3HQAnDSkaCptXTZs'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    welcome_text = """✨ **مرحباً بك في بوت ROFIX الرسمي** ✨

إليك قائمة الأوامر المتاحة للتصفح:

📌 /start - القائمة الرئيسية
👑 /rofix - من هو ROFIX؟
🛠 /services - الخدمات المتاحة
📞 /contact - التواصل المباشر مع الدعم
⚡ /ping - فحص سرعة واستجابة البوت
❓ /help - طريقة الاستخدام والتعليمات"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['rofix'])
def send_rofix(message):
    bot.reply_to(message, "ROFIX هو نظام برمجاتي متطور مصمم لمساعدتك وتقديم خدمات رقمية سريعة وموثوقة.")

@bot.message_handler(commands=['services'])
def send_services(message):
    bot.reply_to(message, "الخدمات المتاحة حالياً:\n1. إدارة وتطوير بوتات تليجرام\n2. استشارات تقنية\n3. حلول رقمية مخصصة")

@bot.message_handler(commands=['contact'])
def send_contact(message):
    bot.reply_to(message, "للتواصل المباشر مع الدعم الفني، يرجى إرسال رسالتك وسنقوم بالرد عليك في أقرب وقت! 💡")

@bot.message_handler(commands=['ping'])
def send_ping(message):
    bot.reply_to(message, "Pong! ⚡ البوت يعمل بشكل ممتاز وسريع جداً.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "استخدم الأوامر الموجودة في القائمة /start أو /menu لتتفاعل مع البوت بكل سهولة.")

bot.infinity_polling()
