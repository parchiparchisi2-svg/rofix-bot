import os
import telebot
from flask import Flask
from threading import Thread

TOKEN = os.environ.get('TOKEN', '8989576551:AAFLvMZ7AZosLY8T5AJ3HQAnDSkaCptXTZs')
bot = telebot.TeleBot(TOKEN)

app = Flask('')

@app.route('/')
def home():
    return "ROFIX Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    welcome_text = """✨ **مرحباً بك في بوت ROFIX الرسمي** ✨

إليك قائمة الأوامر المتاحة للتصفح:
📌 /start - القائمة الرئيسية
👑 /rofix - من هو ROFIX؟
🛠️ /services - الخدمات المتاحة
📞 /contact - التواصل المباشر مع الدعم
⚡ /ping - فحص سرعة واستجابة البوت
❓ /help - طريقة الاستخدام والتعليمات"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['rofix'])
def send_rofix(message):
    bot.reply_to(message, "👑 **ROFIX** هو علامتك التجارية الرسمية والذكية لتسيير وتقديم الخدمات الرقمية باحترافية عالية.")

@bot.message_handler(commands=['services'])
def send_services(message):
    bot.reply_to(message, "🛠️ **الخدمات المتاحة:**\n- برمجة وتطوير البوتات\n- حلول رقمية متكاملة\n- دعم فني واستشارات")

@bot.message_handler(commands=['ping'])
def send_ping(message):
    bot.reply_to(message, "⚡ البوت يعمل بشكل ممتاز وسريع جداً!")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "❓ اختر أحد الأوامر في القائمة أو أرسل استفسارك وسيتم خدمتك.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
    
