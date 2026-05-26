import telebot
from telebot import types

# --- الإعدادات ---
TOKEN = '8600585281:AAFBa-EbKMdN1xJKzG_4iiYbJ17vXlqEB3c'
CHANNEL_ID = '-1003100842650'
BOT_LINK = 't.me/Asil_OTP_bot'
UPDATES_LINK = 'https://t.me/aseel_alhmzy7820'

bot = telebot.TeleBot(TOKEN)

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(CHANNEL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.chat.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 اشترك في القناة", url=UPDATES_LINK))
        markup.add(types.InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data='check_sub'))
        bot.send_message(message.chat.id, "⚠️ يجب الاشتراك في القناة أولاً:", reply_markup=markup)
        return
    
    text = "مرحباً بك في بوت [أصيل الحمزي]، اختر الخدمة:"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("واتساب 🟢", callback_data='service_wa'),
               types.InlineKeyboardButton("فيسبوك 🔵", callback_data='service_fb'),
               types.InlineKeyboardButton("تلجرام 🔵", callback_data='service_tg'))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def choose_country(call):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("العراق 🇮🇶", callback_data='country_iq'),
               types.InlineKeyboardButton("السعودية 🇸🇦", callback_data='country_sa'))
    markup.add(types.InlineKeyboardButton("🔙 الرجوع للخدمات", callback_data='back_to_services'))
    bot.edit_message_text("اختر الدولة:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('country_'))
def show_numbers(call):
    country_code = call.data.split('_')[1]
    flag = "🇮🇶" if country_code == 'iq' else "🇸🇦"
    # يمكنك إضافة أرقامك هنا
    numbers = ["+9647826634643", "+9647826635395"]
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for num in numbers:
        # التنسيق المطلوب: العلم + أيقونة النسخ + الرقم
        markup.add(types.InlineKeyboardButton(f"{flag} ❏ {num}", callback_data=f"copy_{num}"))
    
    markup.add(types.InlineKeyboardButton("🔄 تبديل الرقم", callback_data=f"country_{country_code}"),
               types.InlineKeyboardButton("🔑 Group OTP", url=UPDATES_LINK),
               types.InlineKeyboardButton("🔙 الرجوع للخدمات", callback_data='back_to_services'))
    
    bot.edit_message_text("إليك الأرقام المتاحة، اضغط لنسخ الرقم:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('copy_'))
def copy_number(call):
    number = call.data.split('_')[1]
    # إزالة التنبيه المزعج (بدون show_alert=True)
    bot.answer_callback_query(call.id, "تم النسخ") 

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_services')
def back(call):
    # إعادة توجيه للقائمة الرئيسية
    text = "مرحباً بك في بوت [أصيل الحمزي]، اختر الخدمة:"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("واتساب 🟢", callback_data='service_wa'),
               types.InlineKeyboardButton("فيسبوك 🔵", callback_data='service_fb'),
               types.InlineKeyboardButton("تلجرام 🔵", callback_data='service_tg'))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'check_sub')
def check(call):
    if is_subscribed(call.message.chat.id):
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "لم تشترك بعد!")

bot.infinity_polling()
