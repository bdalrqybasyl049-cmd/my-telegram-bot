import telebot
from telebot import types

# --- الإعدادات ---
TOKEN = '8600585281:AAFBa-EbKMdN1xJKzG_4iiYbJ17vXlqEB3c'
CHANNEL_1 = '-1003100842650' # قناة الأكواد
CHANNEL_2 = '-1003575629070' # القناة الجديدة
UPDATES_LINK = 'https://t.me/aseel_alhmzy777'
BOT_LINK = 'https://t.me/Asil_OTP_bot'

bot = telebot.TeleBot(TOKEN)

def mask_number(number):
    return f"{number[:7]}****{number[-3:]}"

def is_subscribed(user_id):
    channels = [CHANNEL_1, CHANNEL_2]
    for ch in channels:
        try:
            if bot.get_chat_member(ch, user_id).status not in ['member', 'administrator', 'creator']:
                return False
        except: return False
    return True

# دالة النشر التلقائي في قناة الأكواد عند نسخ الرقم
def send_to_channel(number):
    text = f"🚨 **كود جديد تم طلبه**\n\nالرقم: `{mask_number(number)}`\n\nاضغط للنسخ من الأسفل 👇"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(f"📋 {number}", callback_data=f"copy_{number}"))
    markup.row(
        types.InlineKeyboardButton("📞 قناة التحديثات", url=UPDATES_LINK),
        types.InlineKeyboardButton("🤖 دخول البوت", url=BOT_LINK)
    )
    bot.send_message(CHANNEL_1, text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.chat.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 اشترك في القناة الجديدة", url=UPDATES_LINK))
        bot.send_message(message.chat.id, "⚠️ يجب الاشتراك في القنوات أولاً:", reply_markup=markup)
        return
    
    text = "📍 [ SERVICE MENU ]\n\nSelect a service or country 💎"
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("WhatsApp 🟢", callback_data='service_wa'))
    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def show_numbers(call):
    # مثال للأرقام
    numbers = ["+9647826634643", "+9647826635395", "+9647826631386"]
    text = "إليك الأرقام المتاحة، اختر واحداً للنسخ:"
    
    markup = types.InlineKeyboardMarkup()
    for num in numbers:
        markup.add(types.InlineKeyboardButton(f"📋 {num}", callback_data=f"copy_{num}"))
    
    markup.add(
        types.InlineKeyboardButton("🔄 تغيير الرقم", callback_data='service_wa'),
        types.InlineKeyboardButton("🌐 تغيير الدولة", callback_data='service_wa'),
        types.InlineKeyboardButton("📢 قناة الأكواد", url="https://t.me/aseel_alhmzy7820"),
        types.InlineKeyboardButton("⬅️ القائمة الرئيسية", callback_data='back_to_services')
    )
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('copy_'))
def copy_number(call):
    num = call.data.split('_')[1]
    # النشر التلقائي في القناة عند النسخ
    send_to_channel(num)
    bot.answer_callback_query(call.id, f"تم نسخ الرقم: {num}", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == 'back_to_services')
def back(call):
    start(call.message)

bot.infinity_polling()
