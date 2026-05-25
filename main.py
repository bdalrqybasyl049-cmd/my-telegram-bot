import telebot
from telebot import types

# --- الإعدادات ---
TOKEN = '8600585281:AAFBa-EbKMdN1xJKzG_4iiYbJ17vXlqEB3c'
CHANNEL_ID = '-1003100842650'  # ملاحظة: يجب إضافة - قبل رقم القناة
BOT_LINK = 't.me/Asil_OTP_bot'
UPDATES_LINK = 'https://t.me/aseel_alhmzy7820'

bot = telebot.TeleBot(TOKEN)

# 1. دالة التحقق من الاشتراك
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error: {e}")
        return False

# 2. القائمة الرئيسية
@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.chat.id):
        markup = types.InlineKeyboardMarkup()
        # قناة الاشتراك تكون بدون - في الرابط
        markup.add(types.InlineKeyboardButton("📢 اشترك في القناة", url="https://t.me/A_ToolsX"))
        markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data='check_sub'))
        bot.send_message(message.chat.id, "⚠️ يجب الاشتراك في القناة أولاً:", reply_markup=markup)
        return
    
    text = "مرحباً بك في بوت [أصيل الحمزي]، اختر الخدمة:"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("واتساب 🟢", callback_data='service_wa'),
               types.InlineKeyboardButton("فيسبوك 🔵", callback_data='service_fb'),
               types.InlineKeyboardButton("تلجرام 🔵", callback_data='service_tg'))
    bot.send_message(message.chat.id, text, reply_markup=markup)

# 3. باقي الدوال (اختيار الدول وعرض الأرقام) كما هي في كودك السابق
@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def choose_country(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("العراق 🇮🇶", callback_data='country_iq'),
               types.InlineKeyboardButton("السعودية 🇸🇦", callback_data='country_sa'))
    markup.add(types.InlineKeyboardButton("🔙 الرجوع للخدمات", callback_data='back_to_services'))
    bot.edit_message_text("اختر الدولة:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('country_'))
def show_numbers(call):
    numbers = ["+9647826634643", "+9647826635395", "+9647826631386", "+9647826639032"]
    markup = types.InlineKeyboardMarkup()
    for num in numbers:
        markup.add(types.InlineKeyboardButton(f"📋 {num}", callback_data=f"copy_{num}"))
    markup.add(types.InlineKeyboardButton("🔙 الرجوع للخدمات", callback_data='back_to_services'))
    bot.edit_message_text("إليك الأرقام المتاحة، اضغط لنسخ الرقم:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# 4. النشر في القناة
def publish_to_channel(number):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"📋 {number}", callback_data="none"))
    btn_bot = types.InlineKeyboardButton("🤖 بوت أصيل", url=f"https://{BOT_LINK}")
    btn_updates = types.InlineKeyboardButton("📢 Updates & News", url=UPDATES_LINK)
    markup.row(btn_bot, btn_updates)
    msg = f"🇮🇶 #IQ واتساب\nالرقم: `{number[:7]}****{number[-4:]}`"
    bot.send_message(CHANNEL_ID, msg, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('copy_'))
def copy_number(call):
    number = call.data.split('_')[1]
    bot.answer_callback_query(call.id, f"تم نسخ الرقم: {number}", show_alert=True)
    publish_to_channel(number)

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_services')
def back(call):
    start(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'check_sub')
def check(call):
    if is_subscribed(call.message.chat.id):
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "لم تشترك بعد!")

bot.infinity_polling()
