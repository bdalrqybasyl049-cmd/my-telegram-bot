import asyncio
import requests
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode

# --- الإعدادات ---
API_TOKEN = "8600585281:AAFBa-EbKMdN1xJKzG_4iiYbJ17vXlqEB3c"
GRIZZLY_API_KEY = "289bbe85505b8fa3ad2a6d77797a1fa6"

CHANNEL_OTP_ID = -1003100842650 # قناة الأكواد
CHANNEL_UPDATE_ID = -1003575629070 # قناة التحديثات

BOT_LINK = "https://t.me/Asil_OTP_bot"
CHANNEL_OTP_LINK = "https://t.me/aseel_alhmzy7820"
CHANNEL_UPDATE_LINK = "https://t.me/aseel_alhmzy777"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- البيانات ---
COUNTRIES = {"اليمن": "7", "السعودية": "3", "العراق": "6"}
SERVICES = {"واتساب": "wa", "فيسبوك": "fb"}

# --- الدالة: التحقق من الاشتراك ---
async def is_subscribed(user_id):
    try:
        c1 = await bot.get_chat_member(chat_id=CHANNEL_OTP_ID, user_id=user_id)
        c2 = await bot.get_chat_member(chat_id=CHANNEL_UPDATE_ID, user_id=user_id)
        return c1.status != 'left' and c2.status != 'left'
    except: return False

# --- الدالة: لوحة الاشتراك ---
def get_sub_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="1. @aseel_alhmzy7820", url=CHANNEL_OTP_LINK)],
        [InlineKeyboardButton(text="2. @aseel_alhmzy777", url=CHANNEL_UPDATE_LINK)],
        [InlineKeyboardButton(text="✅ تحقق من الاشتراك", callback_data="check_sub")]
    ])

# --- الأوامر الأساسية ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if await is_subscribed(message.from_user.id):
        kb = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="☎️ الحصول على رقم")],
            [KeyboardButton(text="🔄 تغيير الرقم"), KeyboardButton(text="🌐 تغيير الدولة")],
            [KeyboardButton(text="🔑 جروب البوت"), KeyboardButton(text="⬅️ القائمة الرئيسية")]
        ], resize_keyboard=True)
        await message.answer(f"مرحباً بك في بوت [اصيل الحمزي]، اختر خدمة:", reply_markup=kb)
    else:
        await message.answer("يرجى الاشتراك ثم الضغط على زر 'تحقق من الاشتراك' أدناه:", reply_markup=get_sub_kb())

@dp.callback_query(F.data == "check_sub")
async def check_sub(callback: types.CallbackQuery):
    if await is_subscribed(callback.from_user.id):
        await callback.message.delete()
        await cmd_start(callback.message)
    else:
        await callback.answer("لم تشترك بعد!", show_alert=True)

# --- اختيار الخدمة ---
@dp.message(F.text == "☎️ الحصول على رقم")
async def select_service(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 واتساب", callback_data="svc_wa"), InlineKeyboardButton(text="🔵 فيسبوك", callback_data="svc_fb")]
    ])
    await message.answer("اختر الخدمة المطلوبة:", reply_markup=kb)

# --- اختيار الدولة ---
@dp.callback_query(F.data.startswith("svc_"))
async def select_country(callback: types.CallbackQuery):
    service = callback.data.split("_")[1]
    kb_list = []
    for name, code in COUNTRIES.items():
        # جلب العدد التلقائي
        url = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={GRIZZLY_API_KEY}&action=getNumbersStatus&country={code}"
        try:
            res = requests.get(url).json()
            count = res.get(f"{service}_{code}", 0)
        except: count = 0
        kb_list.append([InlineKeyboardButton(text=f"{name} ({count})", callback_data=f"buy_{service}_{code}")])
    await callback.message.edit_text("اختر الدولة:", reply_markup=InlineKeyboardMarkup(inline_keyboard=kb_list))

# --- جلب الرقم والنشر ---
@dp.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: types.CallbackQuery):
    _, service, country = callback.data.split("_")
    url = f"https://api.grizzlysms.com/stubs/handler_api.php?api_key={GRIZZLY_API_KEY}&action=getNumber&service={service}&country={country}"
    
    response = requests.get(url).text
    if response.startswith("ACCESS_NUMBER"):
        _, order_id, phone = response.split(":")
        
        # تنسيق الرموز
        icon = "🟢" if service == "wa" else "🔵"
        country_name = "🇮🇶" if country == "6" else "🇾🇪" if country == "7" else "🇸🇦"
        
        post_text = f"🔊 ➔ {country_name} #Code {icon}\n+{phone} #Arabic ┤ 👤\n🪙 ❏ `{phone}`\n\n[ 📞 قناة التحديثات ] [ 🔑 دخول البوت ]"
        
        # نشر في القناة
        await bot.send_message(CHANNEL_OTP_ID, post_text, parse_mode=ParseMode.MARKDOWN, 
                               reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                                   [InlineKeyboardButton(text="📞 قناة التحديثات", url=CHANNEL_UPDATE_LINK), 
                                    InlineKeyboardButton(text="🔑 دخول البوت", url=BOT_LINK)]
                               ]))
        await callback.message.answer(f"✅ تم الحصول على الرقم: `{phone}`")
    else:
        await callback.message.answer("⚠️ عذراً، لا توجد أرقام متاحة حالياً.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
