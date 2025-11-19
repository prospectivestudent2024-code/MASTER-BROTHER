from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)
import json
import datetime
import os

# ====== TOKEN & ADMIN ID ======
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8212670766:AAHRucHEvSLiOQuo-QDH920vx0BpzZwO7XM')
ADMIN_CHAT_IDS = [int(os.getenv('ADMIN_CHAT_ID', '5549431865')), 124894701]

# ====== HOLATLAR ======
LANG, CONTACT, MENU, PRODUCTS, ORDER_NAME, ORDER_PRODUCT, ORDER_QUANTITY, ORDER_PHONE, LOGISTICS, LOGISTICS_TYPE, LOGISTICS_COUNTRY, LOGISTICS_PHONE, UPDATE_PRICE, BROADCAST_MESSAGE, BROADCAST_CONFIRM = range(15)

# ====== MAHSULOTLAR LUG'ATI ======
PRODUCTS_DICT = {
    'uz': [
        "Acetic acid 99% Wanling (Xitoy) 🇨🇳",
        "Acetic acid 99% Fanovaran (Eron) 🇮🇷",
        "SLES 70% (Eron) 🇮🇷",
        "LABSA 97% (Eron) 🇮🇷",
        "MEG (Eron) 🇮🇷",
        "Caustic soda CCPC 98% (Eron) 🇮🇷",
        "Caustic soda other 99% (Eron) 🇮🇷",
        "Caustic soda Yihua 98% (Xitoy) 🇨🇳",
        "Caustic soda Tianye 98% (Xitoy) 🇨🇳",
        "Caustic soda Zhongtai 98% (Xitoy) 🇨🇳",
        "Longi panel (Xitoy) 🇨🇳",
        "Bicarbonate sodium (Eron) 🇮🇷"
    ],
    'ru': [
        "Уксусная кислота 99% Wanling (Китай) 🇨🇳",
        "Уксусная кислота 99% Fanovaran (Иран) 🇮🇷",
        "SLES 70% (Иран) 🇮🇷",
        "LABSA 97% (Иран) 🇮🇷",
        "MEG (Иран) 🇮🇷",
        "Каустическая сода CCPC 98% (Иран) 🇮🇷",
        "Каустическая сода other 99% (Иран) 🇮🇷",
        "Каустическая сода Yihua 98% (Китай) 🇨🇳",
        "Каустическая сода Tianye 98% (Китай) 🇨🇳",
        "Каустическая сода Zhongtai 98% (Китай) 🇨🇳",
        "Панель Longi (Китай) 🇨🇳",
        "Бикарбонат натрия (Иран) 🇮🇷"
    ],
    'en': [
        "Acetic acid 99% Wanling (China) 🇨🇳",
        "Acetic acid 99% Fanovaran (Iran) 🇮🇷",
        "SLES 70% (Iran) 🇮🇷",
        "LABSA 97% (Iran) 🇮🇷",
        "MEG (Iran) 🇮🇷",
        "Caustic soda CCPC 98% (Iran) 🇮🇷",
        "Caustic soda other 99% (Iran) 🇮🇷",
        "Caustic soda Yihua 98% (China) 🇨🇳",
        "Caustic soda Tianye 98% (China) 🇨🇳",
        "Caustic soda Zhongtai 98% (China) 🇨🇳",
        "Longi panel (China) 🇨🇳",
        "Bicarbonate sodium (Iran) 🇮🇷"
    ],
    'fa': [
        "اسید استیک ۹۹٪ Wanling (چین) 🇨🇳",
        "اسید استیک ۹۹٪ Fanovaran (ایران) 🇮🇷",
        "SLES 70٪ (ایران) 🇮🇷",
        "LABSA 97٪ (ایران) 🇮🇷",
        "MEG (ایران) 🇮🇷",
        "سود سوزآور CCPC 98٪ (ایران) 🇮🇷",
        "سود سوزآور other 99٪ (ایران) 🇮🇷",
        "سود سوزآور Yihua 98٪ (چین) 🇨🇳",
        "سود سوزآور Tianye 98٪ (چین) 🇨🇳",
        "سود سوزآور Zhongtai 98٪ (چین) 🇨🇳",
        "پنل Longi (چین) 🇨🇳",
        "بی کربنات سدیم (ایران) 🇮🇷"
    ],
    'ar': [
        "حمض الخل 99٪ Wanling (الصين) 🇨🇳",
        "حمض الخل 99٪ Fanovaran (إيران) 🇮🇷",
        "SLES 70٪ (إيران) 🇮🇷",
        "LABSA 97٪ (إيران) 🇮🇷",
        "MEG (إيران) 🇮🇷",
        "صودا كاوية CCPC 98٪ (إيران) 🇮🇷",
        "صودا كاوية other 99٪ (إيران) 🇮🇷",
        "صودا كاوية Yihua 98٪ (الصين) 🇨🇳",
        "صودا كاوية Tianye 98٪ (الصين) 🇨🇳",
        "صودا كاوية Zhongtai 98٪ (الصين) 🇨🇳",
        "لوحة Longi (الصين) 🇨🇳",
        "بيكربونات الصوديوم (إيران) 🇮🇷"
    ],
    'zh': [
        "醋酸 99% Wanling (中国) 🇨🇳",
        "醋酸 99% Fanovaran (伊朗) 🇮🇷",
        "SLES 70% (伊朗) 🇮🇷",
        "LABSA 97% (伊朗) 🇮🇷",
        "MEG (伊朗) 🇮🇷",
        "氢氧化钠 CCPC 98% (伊朗) 🇮🇷",
        "氢氧化钠 other 99% (伊朗) 🇮🇷",
        "氢氧化钠 Yihua 98% (中国) 🇨🇳",
        "氢氧化钠 Tianye 98% (中国) 🇨🇳",
        "氢氧化钠 Zhongtai 98% (中国) 🇨🇳",
        "隆基面板 (中国) 🇨🇳",
        "碳酸氢钠 (伊朗) 🇮🇷"
    ]
}

# ====== MENYU VA TUGMALAR ======
BUTTONS = {
    'uz': {
        'products': "🛒 Mahsulotlar",
        'address': "📍 Manzilimiz",
        'order': "📝 Buyurtma berish",
        'about': "ℹ️ Biz haqimizda",
        'logistics': "🚚 Logistika",
        'price': "💰 Narxnoma",
        'contact': "📞 Aloqa",
        'back': "⬅️ Orqaga",
        'cancel': "❌ Bekor qilish",
        'import': "📥 Import",
        'export': "📤 Export",
        'admin_panel': "👑 Boshqaruv paneli",
        'bot_users': "👥 Bot foydalanuvchilari",
        'applications': "📋 Zayavkalar",
        'delete': "🗑️ O'chirish",
        'delete_order': "🗑️ Buyurtmani o'chirish",
        'delete_logistics': "🗑️ Logistika so'rovini o'chirish",
        'delete_user': "🗑️ Foydalanuvchini o'chirish",
        'update_price': "📊 Narxnoma yangilash",
        'broadcast': "📢 Foydalanuvchilarga xabar yuborish"
    },
    'ru': {
        'products': "🛒 Продукты",
        'address': "📍 Наш адрес",
        'order': "📝 Сделать заказ",
        'about': "ℹ️ О нас",
        'logistics': "🚚 Логистика",
        'price': "💰 Прайс‑лист",
        'contact': "📞 Контакт",
        'back': "⬅️ Назад",
        'cancel': "❌ Отмена",
        'import': "📥 Импорт",
        'export': "📤 Экспорт",
        'admin_panel': "👑 Панель управления",
        'bot_users': "👥 Пользователи бота",
        'applications': "📋 Заявки",
        'delete': "🗑️ Удалить",
        'delete_order': "🗑️ Удалить заказ",
        'delete_logistics': "🗑️ Удалить логистику",
        'delete_user': "🗑️ Удалить пользователя",
        'update_price': "📊 Обновить прайс",
        'broadcast': "📢 Отправить сообщение пользователям"
    },
    'en': {
        'products': "🛒 Products",
        'address': "📍 Our address",
        'order': "📝 Make order",
        'about': "ℹ️ About us",
        'logistics': "🚚 Logistics",
        'price': "💰 Price list",
        'contact': "📞 Contact",
        'back': "⬅️ Back",
        'cancel': "❌ Cancel",
        'import': "📥 Import",
        'export': "📤 Export",
        'admin_panel': "👑 Admin Panel",
        'bot_users': "👥 Bot Users",
        'applications': "📋 Applications",
        'delete': "🗑️ Delete",
        'delete_order': "🗑️ Delete order",
        'delete_logistics': "🗑️ Delete logistics",
        'delete_user': "🗑️ Delete user",
        'update_price': "📊 Update Price List",
        'broadcast': "📢 Send message to users"
    },
    'fa': {
        'products': "🛒 محصولات",
        'address': "📍 آدرس ما",
        'order': "📝 سفارش دهید",
        'about': "ℹ️ درباره ما",
        'logistics': "🚚 لجستیک",
        'price': "💰 لیست قیمت",
        'contact': "📞 تماس",
        'back': "⬅️ بازگشت",
        'cancel': "❌ لغو",
        'import': "📥 واردات",
        'export': "📤 صادرات",
        'admin_panel': "👑 پنل مدیریت",
        'bot_users': "👥 کاربران ربات",
        'applications': "📋 درخواست‌ها",
        'delete': "🗑️ حذف",
        'delete_order': "🗑️ حذف سفارش",
        'delete_logistics': "🗑️ حذف لجستیک",
        'delete_user': "🗑️ حذف کاربر",
        'update_price': "📊 بروزرسانی قیمت",
        'broadcast': "📢 ارسال پیام به کاربران"
    },
    'ar': {
        'products': "🛒 المنتجات",
        'address': "📍 عنواننا",
        'order': "📝 اطلب الآن",
        'about': "ℹ️ معلومات عنا",
        'logistics': "🚚 الخدمات اللوجستية",
        'price': "💰 قائمة الأسعار",
        'contact': "📞 اتصال",
        'back': "⬅️ العودة",
        'cancel': "❌ إلغاء",
        'import': "📥 استيراد",
        'export': "📤 تصدير",
        'admin_panel': "👑 لوحة التحكم",
        'bot_users': "👥 مستخدمي البوت",
        'applications': "📋 الطلبات",
        'delete': "🗑️ حذف",
        'delete_order': "🗑️ حذف الطلب",
        'delete_logistics': "🗑️ حذف الخدمات اللوجستية",
        'delete_user': "🗑️ حذف المستخدم",
        'update_price': "📊 تحديث الأسعار",
        'broadcast': "📢 إرسال رسالة للمستخدمين"
    },
    'zh': {
        'products': "🛒 产品",
        'address': "📍 我们的位置",
        'order': "📝 下订单",
        'about': "ℹ️ 关于我们",
        'logistics': "🚚 物流",
        'price': "💰 价目表",
        'contact': "📞 联系方式",
        'back': "⬅️ 返回",
        'cancel': "❌ 取消",
        'import': "📥 进口",
        'export': "📤 出口",
        'admin_panel': "👑 管理面板",
        'bot_users': "👥 机器人用户",
        'applications': "📋 申请",
        'delete': "🗑️ 删除",
        'delete_order': "🗑️ 删除订单",
        'delete_logistics': "🗑️ 删除物流",
        'delete_user': "🗑️ 删除用户",
        'update_price': "📊 更新价目表",
        'broadcast': "📢 向用户发送消息"
    }
}

ADDRESS = {
    'uz': "O'zbekiston Respublikasi, Buxoro viloyati, Peshku tumani, Yangibozor",
    'ru': "Республика Узбекистан, Бухарская область, Пешку район, Янгибазар",
    'en': "Republic of Uzbekistan, Bukhara region, Peshku district, Yangibozor",
    'fa': "جمهوری ازبکستان، ولایت بخارا، ولسوالی پشتک، یانگیبازار",
    'ar': "جمهورية أوزبكستان، منطقة بخارى، منطقة بيشكو، يانغيبازار",
    'zh': "乌兹别克斯坦共和国，布哈拉州，佩什库区，扬吉巴扎尔"
}

# ====== LOKATSIYA KOORDINATALARI ======
LOCATION = {
    'latitude': 40.0379,
    'longitude': 64.5186
}

user_data = {}

# ====== KONTAKT MATNLARI ======
CONTACT_TEXTS = {
    'uz': "📱 Kontaktni yuborish",
    'ru': "📱 Отправить контакт", 
    'en': "📱 Share contact",
    'fa': "📱 ارسال مخاطب",
    'ar': "📱 مشاركة جهة اتصال",
    'zh': "📱 分享联系方式"
}

# ====== BUYURTMA MA'LUMOTLARINI SAQLASH ======
def save_order(order_data):
    try:
        with open('orders.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(order_data, ensure_ascii=False) + '\n')
    except Exception as e:
        print(f"Buyurtmani saqlashda xatolik: {e}")

def save_logistics_request(request_data):
    try:
        with open('logistics_requests.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(request_data, ensure_ascii=False) + '\n')
    except Exception as e:
        print(f"Logistika so'rovini saqlashda xatolik: {e}")

def save_user_data(user_data):
    try:
        with open('users.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(user_data, ensure_ascii=False) + '\n')
    except Exception as e:
        print(f"Foydalanuvchi ma'lumotlarini saqlashda xatolik: {e}")

def delete_order_by_index(index):
    """Buyurtmani index bo'yicha o'chirish"""
    try:
        orders = get_all_orders()
        if 0 <= index < len(orders):
            deleted_order = orders.pop(index)
            with open('orders.json', 'w', encoding='utf-8') as f:
                for order in orders:
                    f.write(json.dumps(order, ensure_ascii=False) + '\n')
            return deleted_order
        return None
    except Exception as e:
        print(f"Buyurtmani o'chirishda xatolik: {e}")
        return None

def delete_logistics_by_index(index):
    """Logistika so'rovini index bo'yicha o'chirish"""
    try:
        requests = get_all_logistics_requests()
        if 0 <= index < len(requests):
            deleted_request = requests.pop(index)
            with open('logistics_requests.json', 'w', encoding='utf-8') as f:
                for request in requests:
                    f.write(json.dumps(request, ensure_ascii=False) + '\n')
            return deleted_request
        return None
    except Exception as e:
        print(f"Logistika so'rovini o'chirishda xatolik: {e}")
        return None

def delete_user_by_index(index):
    """Foydalanuvchini index bo'yicha o'chirish"""
    try:
        users = get_all_users()
        if 0 <= index < len(users):
            deleted_user = users.pop(index)
            with open('users.json', 'w', encoding='utf-8') as f:
                for user in users:
                    f.write(json.dumps(user, ensure_ascii=False) + '\n')
            return deleted_user
        return None
    except Exception as e:
        print(f"Foydalanuvchini o'chirishda xatolik: {e}")
        return None

def get_all_users():
    """Barcha foydalanuvchilarni olish"""
    users = []
    try:
        with open('users.json', 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    user = json.loads(line.strip())
                    users.append(user)
                except:
                    continue
    except FileNotFoundError:
        pass
    return users

def get_all_orders():
    """Barcha buyurtmalarni olish"""
    orders = []
    try:
        with open('orders.json', 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    order = json.loads(line.strip())
                    orders.append(order)
                except:
                    continue
    except FileNotFoundError:
        pass
    return orders

def get_all_logistics_requests():
    """Barcha logistika so'rovlarini olish"""
    requests = []
    try:
        with open('logistics_requests.json', 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    request = json.loads(line.strip())
                    requests.append(request)
                except:
                    continue
    except FileNotFoundError:
        pass
    return requests

def lang_keyboard():
    return ReplyKeyboardMarkup(
        [
            ['Oʻzbekcha 🇺🇿', 'Русский 🇷🇺'],
            ['English 🇬🇧', 'فارسی 🇮🇷'],
            ['العربية 🇸🇦', '中文 🇨🇳']
        ],
        resize_keyboard=True
    )

def main_menu_keyboard(lang, chat_id):
    b = BUTTONS[lang]
    buttons = [
        [b['products'], b['address']],
        [b['order'], b['about']],
        [b['logistics'], b['price']],
        [b['contact']],
        [b['back']]
    ]
    
    if chat_id in ADMIN_CHAT_IDS:
        buttons.insert(0, [b['admin_panel']])
    
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def admin_panel_keyboard(lang):
    b = BUTTONS[lang]
    return ReplyKeyboardMarkup([
        [b['applications'], b['bot_users']],
        [b['update_price'], b['broadcast']],
        [b['back']]
    ], resize_keyboard=True)

def applications_keyboard(lang):
    b = BUTTONS[lang]
    return ReplyKeyboardMarkup([
        [b['delete_order'], b['delete_logistics']],
        [b['back']]
    ], resize_keyboard=True)

def users_keyboard(lang):
    b = BUTTONS[lang]
    return ReplyKeyboardMarkup([
        [b['delete_user']],
        [b['back']]
    ], resize_keyboard=True)

def broadcast_confirm_keyboard(lang):
    b = BUTTONS[lang]
    return ReplyKeyboardMarkup([
        [b['broadcast']],
        [b['cancel']]
    ], resize_keyboard=True)

def products_keyboard(lang):
    prods = PRODUCTS_DICT.get(lang, PRODUCTS_DICT['uz'])
    buttons = []
    
    buttons.append([prods[0], prods[1]])
    buttons.append([prods[2], prods[3]])
    buttons.append([prods[4], prods[5]])
    buttons.append([prods[6], prods[7]])
    buttons.append([prods[8], prods[9]])
    buttons.append([prods[10], prods[11]])
    
    buttons.append([BUTTONS[lang]['back']])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def order_cancel_keyboard(lang):
    return ReplyKeyboardMarkup([[BUTTONS[lang]['cancel']]], resize_keyboard=True)

def order_menu_keyboard(lang):
    b = BUTTONS[lang]
    return ReplyKeyboardMarkup([
        [b['order']],
        [b['back']]
    ], resize_keyboard=True)

def logistics_type_keyboard(lang):
    b = BUTTONS[lang]
    return ReplyKeyboardMarkup([
        [b['import'], b['export']],
        [b['back']]
    ], resize_keyboard=True)

def logistics_country_keyboard(lang):
    countries = {
        'uz': [
            "Xitoy 🇨🇳", "Eron 🇮🇷",
            "Rossiya 🇷🇺", "Qozog'iston 🇰🇿", 
            "Tojikiston 🇹🇯", "Turkmaniston 🇹🇲",
            "Hindiston 🇮🇳"
        ],
        'ru': [
            "Китай 🇨🇳", "Иран 🇮🇷",
            "Россия 🇷🇺", "Казахстан 🇰🇿",
            "Таджикистан 🇹🇯", "Туркменистан 🇹🇲", 
            "Индия 🇮🇳"
        ],
        'en': [
            "China 🇨🇳", "Iran 🇮🇷",
            "Russia 🇷🇺", "Kazakhstan 🇰🇿",
            "Tajikistan 🇹🇯", "Turkmenistan 🇹🇲",
            "India 🇮🇳"
        ],
        'fa': [
            "چین 🇨🇳", "ایران 🇮🇷",
            "روسیه 🇷🇺", "قزاقستان 🇰🇿",
            "تاجیکستان 🇹🇯", "ترکمنستان 🇹🇲",
            "هند 🇮🇳"
        ],
        'ar': [
            "الصين 🇨🇳", "إيران 🇮🇷",
            "روسيا 🇷🇺", "كازاخستان 🇰🇿",
            "طاجيكستان 🇹🇯", "تركمانستان 🇹🇲",
            "الهند 🇮🇳"
        ],
        'zh': [
            "中国 🇨🇳", "伊朗 🇮🇷",
            "俄罗斯 🇷🇺", "哈萨克斯坦 🇰🇿",
            "塔吉克斯坦 🇹🇯", "土库曼斯坦 🇹🇲", 
            "印度 🇮🇳"
        ]
    }
    
    country_list = countries.get(lang, countries['uz'])
    buttons = []
    
    for i in range(0, len(country_list), 2):
        if i + 1 < len(country_list):
            buttons.append([country_list[i], country_list[i + 1]])
        else:
            buttons.append([country_list[i]])
    
    buttons.append([BUTTONS[lang]['back']])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def logistics_phone_keyboard(lang):
    contact_btn = KeyboardButton(CONTACT_TEXTS[lang], request_contact=True)
    return ReplyKeyboardMarkup([
        [contact_btn],
        [BUTTONS[lang]['back']]
    ], resize_keyboard=True)

async def send_broadcast_message(context: ContextTypes.DEFAULT_TYPE, message_data, content_type, caption=""):
    """Xabarni barcha foydalanuvchilarga yuborish"""
    try:
        user_chat_ids = [user['chat_id'] for user in get_all_users()]
        success_count = 0
        fail_count = 0
        
        for chat_id in user_chat_ids:
            if chat_id:
                try:
                    if content_type == 'text':
                        await context.bot.send_message(chat_id=chat_id, text=message_data)
                    elif content_type == 'photo':
                        await context.bot.send_photo(chat_id=chat_id, photo=message_data, caption=caption)
                    elif content_type == 'video':
                        await context.bot.send_video(chat_id=chat_id, video=message_data, caption=caption)
                    success_count += 1
                except Exception as e:
                    print(f"Xabar yuborishda xatolik {chat_id}: {e}")
                    fail_count += 1
        
        return success_count, fail_count
        
    except Exception as e:
        print(f"Xabarni yuborishda xatolik: {e}")
        return 0, 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_data[chat_id] = {'contact_sent': False}
    
    user_info = {
        'chat_id': chat_id,
        'first_name': update.effective_user.first_name,
        'username': update.effective_user.username,
        'phone_number': None,
        'language': None,
        'timestamp': datetime.datetime.now().isoformat()
    }
    save_user_data(user_info)
    
    await update.message.reply_text(
        "Iltimos, tilni tanlang / Select language",
        reply_markup=lang_keyboard()
    )
    return LANG

async def lang_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text
    
    lang_map = {
        'Oʻzbekcha 🇺🇿': 'uz',
        'Русский 🇷🇺': 'ru',
        'English 🇬🇧': 'en',
        'فارسی 🇮🇷': 'fa',
        'العربية 🇸🇦': 'ar',
        '中文 🇨🇳': 'zh'
    }
    
    if text not in lang_map:
        await update.message.reply_text("Iltimos, tilni tanlang.", reply_markup=lang_keyboard())
        return LANG
    
    user_data[chat_id]['lang'] = lang_map[text]
    lang = user_data[chat_id]['lang']
    
    users = get_all_users()
    for user in users:
        if user.get('chat_id') == chat_id:
            user['language'] = lang
            break
    
    if not user_data[chat_id].get('contact_sent', False):
        contact_btn = KeyboardButton(CONTACT_TEXTS[lang], request_contact=True)
        back_btn = KeyboardButton(BUTTONS[lang]['back'])
        await update.message.reply_text(
            "Telefon raqamingizni yuboring:" if lang == 'uz' else "Share your phone number:",
            reply_markup=ReplyKeyboardMarkup([[contact_btn], [back_btn]], resize_keyboard=True)
        )
        return CONTACT

    await update.message.reply_text(
        "Asosiy menyu" if lang == 'uz' else "Main menu", 
        reply_markup=main_menu_keyboard(lang, chat_id)
    )
    return MENU

async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    lang = user_data.get(chat_id, {}).get('lang', 'uz')
    if update.message.text == BUTTONS[lang]['back']:
        await update.message.reply_text("Tilni tanlang", reply_markup=lang_keyboard())
        return LANG
    
    contact = update.message.contact
    if contact and contact.user_id == chat_id:
        user_data[chat_id]['contact_sent'] = True
        user_data[chat_id]['phone_number'] = contact.phone_number
        lang = user_data[chat_id].get('lang', 'uz')
        
        users = get_all_users()
        for user in users:
            if user.get('chat_id') == chat_id:
                user['phone_number'] = contact.phone_number
                break
        
        try:
            await context.bot.send_message(
                ADMIN_CHAT_IDS[0],
                f"🆕 Yangi kontakt:\n"
                f"👤 Ism: {contact.first_name}\n"
                f"📞 Telefon: {contact.phone_number}\n"
                f"🆔 Chat ID: {chat_id}\n"
                f"🌐 Til: {lang}"
            )
        except Exception as e:
            print(f"Adminga xabar yuborishda xatolik: {e}")
        
        await update.message.reply_text(
            "Kontakt qabul qilindi!" if lang == 'uz' else "Contact received!",
            reply_markup=main_menu_keyboard(lang, chat_id)
        )
        return MENU
    else:
        await update.message.reply_text(
            "Iltimos, o'zingizning kontaktni yuboring." if lang == 'uz' else "Please share your own contact."
        )
        return CONTACT

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    text = update.message.text
    b = BUTTONS[lang]

    if text == b['back']:
        if user_data.get(chat_id, {}).get('in_admin_panel'):
            user_data[chat_id]['in_admin_panel'] = False
            await update.message.reply_text(
                "Asosiy menyu" if lang == 'uz' else "Main menu", 
                reply_markup=main_menu_keyboard(lang, chat_id)
            )
            return MENU
        else:
            await update.message.reply_text("Tilni tanlang", reply_markup=lang_keyboard())
            return LANG

    if text == b['products']:
        product_select_text = {
            'uz': "🛒 Mahsulotlardan birini tanlang:",
            'ru': "🛒 Выберите один из продуктов:",
            'en': "🛒 Choose one of the products:",
            'fa': "🛒 یکی از محصولات را انتخاب کنید:",
            'ar': "🛒 اختر أحد المنتجات:",
            'zh': "🛒 选择其中一个产品:"
        }
        await update.message.reply_text(
            product_select_text.get(lang, "🛒 Choose a product:"),
            reply_markup=products_keyboard(lang)
        )
        return PRODUCTS

    elif text == b['contact']:
        contact_text = {
            'uz': "📞 Biz bilan bog'laning:\n\n👤 Bahodir - 994187772\n👤 Shahzod - 994187778\n👤 Jahongir - 914187777",
            'ru': "📞 Свяжитесь с нами:\n\n👤 Баходир - 994187772\n👤 Шахзод - 994187778\n👤 Джахонгир - 914187777",
            'en': "📞 Contact us:\n\n👤 Bahodir - 994187772\n👤 Shahzod - 994187778\n👤 Jahongir - 914187777",
            'fa': "📞 با ما تماس بگیرید:\n\n👤 بهادر - 994187772\n👤 شاهزاد - 994187778\n👤 جهانگیر - 914187777",
            'ar': "📞 اتصل بنا:\n\n👤 بهادير - 994187772\n👤 شاهزاد - 994187778\n👤 جهانغير - 914187777",
            'zh': "📞 联系我们:\n\n👤 巴赫季尔 - 994187772\n👤 沙赫佐德 - 994187778\n👤 贾洪吉尔 - 914187777"
        }
        await update.message.reply_text(
            contact_text.get(lang, contact_text['uz']),
            reply_markup=main_menu_keyboard(lang, chat_id)
        )
        return MENU

    elif text == b['address']:
        addr = ADDRESS.get(lang, ADDRESS['uz'])
        address_text = {
            'uz': f"📍 Bizning manzilimiz:\n\n{addr}",
            'ru': f"📍 Наш адрес:\n\n{addr}",
            'en': f"📍 Our address:\n\n{addr}",
            'fa': f"📍 آدرس ما:\n\n{addr}",
            'ar': f"📍 عنواننا:\n\n{addr}",
            'zh': f"📍 我们的位置:\n\n{addr}"
        }
        await update.message.reply_text(
            address_text.get(lang, address_text['uz'])
        )
        
        await update.message.reply_location(
            latitude=LOCATION['latitude'],
            longitude=LOCATION['longitude'],
            reply_markup=main_menu_keyboard(lang, chat_id)
        )
        return MENU

    elif text == b['order']:
        order_start_text = {
            'uz': "📝 Buyurtma berish jarayoni boshlandi!\n\n1. Ism familiyangiz va kompaniya nomingizni kiriting:\n(Misol: Alijon Valijonov, Master Brother MChJ)",
            'ru': "📝 Процесс заказа начался!\n\n1. Введите ваше имя, фамилию и название компании:\n(Пример: Алижон Валижонов, Master Brother MChJ)",
            'en': "📝 Order process started!\n\n1. Enter your full name and company name:\n(Example: Alijon Valijonov, Master Brother LLC)",
            'fa': "📝 فرآیند سفارش شروع شد!\n\n1. نام کامل و نام شرکت خود را وارد کنید:\n(مثال: علیجان ولیجانوف، شرکت مستر برادر)",
            'ar': "📝 بدأت عملية الطلب!\n\n1. أدخل اسمك الكامل واسم الشركة:\n(مثال: عليجان فاليجانوف، شركة ماستر براذر)",
            'zh': "📝 订单流程开始!\n\n1. 输入您的全名和公司名称:\n(示例: 阿利容·瓦利容诺夫, Master Brother 有限责任公司)"
        }
        await update.message.reply_text(
            order_start_text.get(lang, order_start_text['uz']),
            reply_markup=order_cancel_keyboard(lang)
        )
        return ORDER_NAME

    elif text == b['about']:
        about_text = {
            'uz': "👑 MASTER BROTHER\n\n🏢 Kompaniyasi Haqida\n\n📅 Kompaniya 2021 yil may oyida tashkil topgan. Kompaniya qurilish soxasiga oid tovar i xizmatlarni bozorida o`z o`rniga ega bo`lishni o`zining asosiy missiyasi qilib belgilagan.\n\n💼 Kompaniya ishlab chiqarish, savdo, ekport-import, logistika soxalari bilan shug`ullanib kelmoqda. Ayni paytda kompaniya 100 dan ortiq turdagi tovarlar realizatsiyasi bilan shug`ullanib kelmoqda.\n\n🎯 Kompaniyaning 2025 yildagi rejalari:\n⚙️ 10 dan ortiq mini va o`rta ishlab chiqarish liniyalari\n👥 100 dan ortiq o`rta, malakali va professional xodimlar\n🤝 1000 dan ortiq doimiy va vositachi mijozlar",
            'ru': "👑 MASTER BROTHER\n\n🏢 О компании\n\n📅 Компания была основана в мае 2021 года. Основной миссией компании является занять свое место на рынке товаров и услуг в строительной сфере.\n\n💼 Компания занимается производством, торговлей, экспортно-импортными операциями и логистикой. В настоящее время компания занимается реализацией более 100 видов товаров.\n\n🎯 Планы компании на 2025 год:\n⚙️ Более 10 мини и средних производственных линий\n👥 Более 100 средних, квалифицированных и профессиональных сотрудников\n🤝 Более 1000 постоянных и посреднических клиентов",
            'en': "👑 MASTER BROTHER\n\n🏢 About the Company\n\n📅 The company was founded in May 2021. The company has set its main mission to establish its place in the market of goods and services in the construction sector.\n\n💼 The company is engaged in production, trade, export-import, and logistics. Currently, the company is engaged in the sale of more than 100 types of products.\n\n🎯 Company plans for 2025:\n⚙️ More than 10 mini and medium production lines\n👥 More than 100 medium, qualified and professional employees\n🤝 More than 1000 permanent and intermediary clients",
            'fa': "👑 MASTER BROTHER\n\n🏢 درباره شرکت\n\n📅 این شرکت در ماه می 2021 تأسیس شد. مأموریت اصلی شرکت، ایجاد جایگاه خود در بازار کالا و خدمات در بخش ساخت و ساز است.\n\n💼 شرکت در زمینه تولید، تجارت، صادرات-واردات و لجستیک فعالیت می‌کند. در حال حاضر شرکت در زمینه فروش بیش از 100 نوع محصول فعالیت می‌کند.\n\n🎯 برنامه‌های شرکت برای سال 2025:\n⚙️ بیش از 10 خط تولید مینی و متوسط\n👥 بیش از 100 کارمند متوسط، qualified و حرفه‌ای\n🤝 بیش از 1000 مشتری دائمی و واسطه",
            'ar': "👑 MASTER BROTHER\n\n🏢 عن الشركة\n\n📅 تأسست الشركة في مايو 2021. حددت الشركة مهمتها الرئيسية في تأسيس مكانها في سوق السلع والخدمات في قطاع البناء.\n\n💼 تعمل الشركة في مجال الإنتاج، التجارة، الاستيراد والتصدير، والخدمات اللوجستية. حاليًا، تعمل الشركة في بيع أكثر من 100 نوع من المنتجات.\n\n🎯 خطط الشركة لعام 2025:\n⚙️ أكثر من 10 خطوط إنتاج صغيرة ومتوسطة\n👥 أكثر من 100 موظف متوسط، مؤهل ومحترف\n🤝 أكثر من 1000 عميل دائم ووسيط",
            'zh': "👑 MASTER BROTHER\n\n🏢 关于公司\n\n📅 公司成立于2021年5月。公司的主要使命是在建筑行业的商品和服务市场中确立自己的地位。\n\n💼 公司从事生产、贸易、进出口和物流业务。目前，公司从事100多种产品的销售。\n\n🎯 公司2025年计划：\n⚙️ 超过10条小型和中型生产线\n👥 超过100名中级、合格和专业员工\n🤝 超过1000名永久和中介客户"
        }
        await update.message.reply_text(
            about_text.get(lang, about_text['uz']),
            reply_markup=main_menu_keyboard(lang, chat_id)
        )
        return MENU

    elif text == b['logistics']:
        logistics_text = {
            'uz': "🚚 Logistika xizmatlari\n\nQuyidagi logistika xizmatlaridan birini tanlang:",
            'ru': "🚚 Логистические услуги\n\nВыберите одну из логистических услуг:",
            'en': "🚚 Logistics Services\n\nChoose one of the logistics services:",
            'fa': "🚚 خدمات لجستیکی\n\nیکی از خدمات لجستیکی را انتخاب کنید:",
            'ar': "🚚 الخدمات اللوجستية\n\nاختر إحدى الخدمات اللوجستية:",
            'zh': "🚚 物流服务\n\n选择其中一项物流服务:"
        }
        await update.message.reply_text(
            logistics_text.get(lang, logistics_text['uz']),
            reply_markup=logistics_type_keyboard(lang)
        )
        return LOGISTICS_TYPE

    elif text == b['price']:
        try:
            with open("price_list.jpg", "rb") as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=""
                )
            
            price_text = {
                'uz': "💰 Narxnoma: Quyidagi rasmda mahsulotlarimiz narxlari ko'rsatilgan",
                'ru': "💰 Прайс-лист: На изображении ниже указаны цены на наши продукты",
                'en': "💰 Price list: The image below shows the prices of our products",
                'fa': "💰 لیست قیمت: تصویر زیر قیمت محصولات ما را نشان می‌دهد",
                'ar': "💰 قائمة الأسعار: تظهر الصورة أدناه أسعار منتجاتنا",
                'zh': "💰 价目表：下图显示了我们产品的价格"
            }
            await update.message.reply_text(
                price_text.get(lang, price_text['uz']),
                reply_markup=main_menu_keyboard(lang, chat_id)
            )
        except FileNotFoundError:
            error_text = {
                'uz': "❌ Narxnoma rasmi topilmadi. Iltimos, admin bilan bog'laning.",
                'ru': "❌ Изображение прайс-листа не найдено. Пожалуйста, свяжитесь с администратором.",
                'en': "❌ Price list image not found. Please contact admin.",
                'fa': "❌ تصویر لیست قیمت یافت نشد. لطفا با ادمین تماس بگیرید.",
                'ar': "❌ لم يتم العثور على صورة قائمة الأسعار. يرجى الاتصال بالمسؤول.",
                'zh': "❌ 未找到价目表图片。请联系管理员。"
            }
            await update.message.reply_text(
                error_text.get(lang, error_text['uz']),
                reply_markup=main_menu_keyboard(lang, chat_id)
            )
        return MENU

    elif text == b['admin_panel']:
        if chat_id not in ADMIN_CHAT_IDS:
            await update.message.reply_text(
                "Sizga ruxsat yo'q." if lang == 'uz' else "Access denied.",
                reply_markup=main_menu_keyboard(lang, chat_id)
            )
            return MENU
        
        user_data[chat_id]['in_admin_panel'] = True
        
        admin_panel_text = {
            'uz': "👑 Boshqaruv paneliga xush kelibsiz!\n\nQuyidagi imkoniyatlardan foydalaning:",
            'ru': "👑 Добро пожаловать в панель управления!\n\nИспользуйте следующие возможности:",
            'en': "👑 Welcome to Admin Panel!\n\nUse the following options:",
            'fa': "👑 به پنل مدیریت خوش آمدید!\n\nاز گزینه های زیر استفاده کنید:",
            'ar': "👑 مرحبًا بك في لوحة التحكم!\n\nاستخدم الخيارات التالية:",
            'zh': "👑 欢迎来到管理面板!\n\n使用以下选项:"
        }
        await update.message.reply_text(
            admin_panel_text.get(lang, admin_panel_text['uz']),
            reply_markup=admin_panel_keyboard(lang)
        )
        return MENU

    elif text == b['update_price']:
        if chat_id not in ADMIN_CHAT_IDS:
            await update.message.reply_text(
                "Sizga ruxsat yo'q." if lang == 'uz' else "Access denied.",
                reply_markup=main_menu_keyboard(lang, chat_id)
            )
            return MENU
        
        update_price_text = {
            'uz': "📊 Narxnoma yangilash\n\nYangi narxnoma rasmini yuboring:",
            'ru': "📊 Обновление прайс-листа\n\nОтправьте новое изображение прайс-листа:",
            'en': "📊 Update Price List\n\nSend new price list image:",
            'fa': "📊 بروزرسانی لیست قیمت\n\nتصویر جدید لیست قیمت را ارسال کنید:",
            'ar': "📊 تحديث قائمة الأسعار\n\nأرسل صورة قائمة الأسعار الجديدة:",
            'zh': "📊 更新价目表\n\n发送新的价目表图片:"
        }
        
        await update.message.reply_text(
            update_price_text.get(lang, update_price_text['uz']),
            reply_markup=order_cancel_keyboard(lang)
        )
        
        return UPDATE_PRICE

    elif text == b['broadcast']:
        if chat_id not in ADMIN_CHAT_IDS:
            await update.message.reply_text(
                "Sizga ruxsat yo'q." if lang == 'uz' else "Access denied.",
                reply_markup=main_menu_keyboard(lang, chat_id)
            )
            return MENU
        
        broadcast_text = {
            'uz': "📢 Foydalanuvchilarga xabar yuborish\n\nIltimos, barcha foydalanuvchilarga yubormoqchi bo'lgan xabaringizni yuboring (matn, rasm yoki video):",
            'ru': "📢 Отправка сообщения пользователям\n\nПожалуйста, отправьте сообщение, которое хотите отправить всем пользователям (текст, изображение или видео):",
            'en': "📢 Send message to users\n\nPlease send the message you want to send to all users (text, image or video):",
            'fa': "📢 ارسال پیام به کاربران\n\nلطفا پیامی را که می‌خواهید به همه کاربران ارسال کنید (متن، تصویر یا ویدیو) ارسال کنید:",
            'ar': "📢 إرسال رسالة للمستخدمين\n\nيرجى إرسال الرسالة التي تريد إرسالها إلى جميع المستخدمين (نص، صورة أو فيديو):",
            'zh': "📢 向用户发送消息\n\n请发送您想要发送给所有用户的消息（文本、图片或视频）:"
        }
        
        await update.message.reply_text(
            broadcast_text.get(lang, broadcast_text['uz']),
            reply_markup=order_cancel_keyboard(lang)
        )
        
        return BROADCAST_MESSAGE

    elif text == b['applications']:
        if chat_id not in ADMIN_CHAT_IDS:
            await update.message.reply_text(
                "Sizga ruxsat yo'q." if lang == 'uz' else "Access denied.",
                reply_markup=main_menu_keyboard(lang, chat_id)
            )
            return MENU
        
        applications_menu_text = {
            'uz': "📋 Zayavkalar bo'limi\n\nQuyidagi amallardan birini tanlang:",
            'ru': "📋 Раздел заявок\n\nВыберите одно из действий:",
            'en': "📋 Applications Section\n\nChoose one of the actions:",
            'fa': "📋 بخش درخواست‌ها\n\nیکی از اقدامات را انتخاب کنید:",
            'ar': "📋 قسم الطلبات\n\nاختر أحد الإجراءات:",
            'zh': "📋 申请部分\n\n选择其中一个操作:"
        }
        await update.message.reply_text(
            applications_menu_text.get(lang, applications_menu_text['uz']),
            reply_markup=applications_keyboard(lang)
        )
        return MENU

    elif text == b['delete_order']:
        if chat_id not in ADMIN_CHAT_IDS:
            await update.message.reply_text(
                "Sizga ruxsat yo'q." if lang == 'uz' else "Access denied.",
                reply_markup=main_menu_keyboard(lang, chat_id)
            )
            return MENU
        
        orders = get_all_orders()
        
        if not orders:
            no_orders_text = {
                'uz': "📭 Hozircha hech qanday buyurtma topilmadi.",
                'ru': "📭 Пока заказов не найдено.",
                'en': "📭 No orders found yet.",
                'fa': "📭 هنوز سفارشی یافت نشد.",
                'ar': "📭 لم يتم العثور على طلبات حتى الآن.",
                'zh': "📭 尚未找到任何订单。"
            }
            await update.message.reply_text(
                no_orders_text.get(lang, no_orders_text['uz']),
                reply_markup=applications_keyboard(lang)
            )
            return MENU
        
        orders_text = {
            'uz': f"🗑️ O'CHIRISH UCHUN BUYURTMALAR RO'YXATI:\n\nBuyurtmalar soni: {len(orders)}\n\nO'chirish uchun buyurtma raqamini yuboring:\n",
            'ru': f"🗑️ СПИСОК ЗАКАЗОВ ДЛЯ УДАЛЕНИЯ:\n\nКоличество заказов: {len(orders)}\n\nОтправьте номер заказа для удаления:\n",
            'en': f"🗑️ ORDERS LIST FOR DELETION:\n\nNumber of orders: {len(orders)}\n\nSend order number to delete:\n",
            'fa': f"🗑️ لیست سفارشات برای حذف:\n\nتعداد سفارشات: {len(orders)}\n\nشماره سفارش را برای حذف ارسال کنید:\n",
            'ar': f"🗑️ قائمة الطلبات للحذف:\n\nعدد الطلبات: {len(orders)}\n\nأرسل رقم الطلب للحذف:\n",
            'zh': f"🗑️ 要删除的订单列表:\n\n订单数量: {len(orders)}\n\n发送要删除的订单编号:\n"
        }
        
        full_message = orders_text.get(lang, orders_text['uz'])
        
        for i, order in enumerate(orders, 1):
            order_details = (
                f"{i}. 👤 {order.get('client_name', 'Noma\'lum')}\n"
                f"   🛒 {order.get('product', 'Noma\'lum')}\n"
                f"   📞 {order.get('phone', 'Noma\'lum')}\n"
                f"   🆔 {order.get('chat_id', 'Noma\'lum')}\n"
            )
            if order.get('quantity'):
                order_details += f"   ⚖️ {order.get('quantity')} tonna\n"
            order_details += f"   ⏰ {order.get('timestamp', '')[:16]}\n\n"
            
            full_message += order_details
        
        if len(full_message) > 4000:
            parts = [full_message[i:i+4000] for i in range(0, len(full_message), 4000)]
            for part in parts:
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(full_message)
        
        user_data[chat_id]['delete_mode'] = 'order'
        
        await update.message.reply_text(
            "O'chirish uchun buyurtma raqamini kiriting yoki 'Orqaga' tugmasini bosing:" if lang == 'uz' else "Enter order number to delete or press 'Back':",
            reply_markup=order_cancel_keyboard(lang)
        )
        return MENU

    elif text == b['delete_logistics']:
        if chat_id not in ADMIN_CHAT_IDS:
            await update.message.reply_text(
                "Sizga ruxsat yo'q." if lang == 'uz' else "Access denied.",
                reply_markup=main_menu_keyboard(lang, chat_id)
            )
            return MENU
        
        logistics_requests = get_all_logistics_requests()
        
        if not logistics_requests:
            no_requests_text = {
                'uz': "📭 Hozircha hech qanday logistika so'rovi topilmadi.",
                'ru': "📭 Пока логистических запросов не найдено.",
                'en': "📭 No logistics requests found yet.",
                'fa': "📭 هنوز درخواست لجستیکی یافت نشد.",
                'ar': "📭 لم يتم العثور على طلبات الخدمات اللوجستية حتى الآن.",
                'zh': "📭 尚未找到任何物流请求。"
            }
            await update.message.reply_text(
                no_requests_text.get(lang, no_requests_text['uz']),
                reply_markup=applications_keyboard(lang)
            )
            return MENU
        
        requests_text = {
            'uz': f"🗑️ O'CHIRISH UCHUN LOGISTIKA SO'ROVLARI RO'YXATI:\n\nSo'rovlar soni: {len(logistics_requests)}\n\nO'chirish uchun so'rov raqamini yuboring:\n",
            'ru': f"🗑️ СПИСОК ЛОГИСТИЧЕСКИХ ЗАПРОСОВ ДЛЯ УДАЛЕНИЯ:\n\nКоличество запросов: {len(logistics_requests)}\n\nОтправьте номер запроса для удаления:\n",
            'en': f"🗑️ LOGISTICS REQUESTS LIST FOR DELETION:\n\nNumber of requests: {len(logistics_requests)}\n\nSend request number to delete:\n",
            'fa': f"🗑️ لیست درخواست‌های لجستیکی برای حذف:\n\nتعداد درخواست‌ها: {len(logistics_requests)}\n\nشماره درخواست را برای حذف ارسال کنید:\n",
            'ar': f"🗑️ قائمة طلبات الخدمات اللوجستية للحذف:\n\nعدد الطلبات: {len(logistics_requests)}\n\nأرسل رقم الطلب للحذف:\n",
            'zh': f"🗑️ 要删除的物流请求列表:\n\n请求数量: {len(logistics_requests)}\n\n发送要删除的请求编号:\n"
        }
        
        full_message = requests_text.get(lang, requests_text['uz'])
        
        for i, request in enumerate(logistics_requests, 1):
            request_details = (
                f"{i}. 📊 {request.get('logistics_type', 'Noma\'lum')}\n"
                f"   🌍 {request.get('country', 'Noma\'lum')}\n"
                f"   📞 {request.get('phone', 'Noma\'lum')}\n"
                f"   🆔 {request.get('chat_id', 'Noma\'lum')}\n"
                f"   ⏰ {request.get('timestamp', '')[:16]}\n\n"
            )
            full_message += request_details
        
        if len(full_message) > 4000:
            parts = [full_message[i:i+4000] for i in range(0, len(full_message), 4000)]
            for part in parts:
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(full_message)
        
        user_data[chat_id]['delete_mode'] = 'logistics'
        
        await update.message.reply_text(
            "O'chirish uchun so'rov raqamini kiriting yoki 'Orqaga' tugmasini bosing:" if lang == 'uz' else "Enter request number to delete or press 'Back':",
            reply_markup=order_cancel_keyboard(lang)
        )
        return MENU

    elif text == b['bot_users']:
        if chat_id not in ADMIN_CHAT_IDS:
            await update.message.reply_text(
                "Sizga ruxsat yo'q." if lang == 'uz' else "Access denied.",
                reply_markup=main_menu_keyboard(lang, chat_id)
            )
            return MENU
        
        users_menu_text = {
            'uz': "👥 Bot foydalanuvchilari bo'limi\n\nQuyidagi amallardan birini tanlang:",
            'ru': "👥 Раздел пользователей бота\n\nВыберите одно из действий:",
            'en': "👥 Bot Users Section\n\nChoose one of the actions:",
            'fa': "👥 بخش کاربران ربات\n\nیکی از اقدامات را انتخاب کنید:",
            'ar': "👥 قسم مستخدمي البوت\n\nاختر أحد الإجراءات:",
            'zh': "👥 机器人用户部分\n\n选择其中一个操作:"
        }
        await update.message.reply_text(
            users_menu_text.get(lang, users_menu_text['uz']),
            reply_markup=users_keyboard(lang)
        )
        return MENU

    elif text == b['delete_user']:
        if chat_id not in ADMIN_CHAT_IDS:
            await update.message.reply_text(
                "Sizga ruxsat yo'q." if lang == 'uz' else "Access denied.",
                reply_markup=main_menu_keyboard(lang, chat_id)
            )
            return MENU
        
        users = get_all_users()
        
        if not users:
            no_users_text = {
                'uz': "🤷‍♂️ Hozircha hech qanday foydalanuvchi topilmadi.",
                'ru': "🤷‍♂️ Пока пользователей не найдено.",
                'en': "🤷‍♂️ No users found yet.",
                'fa': "🤷‍♂️ هنوز کاربری یافت نشد.",
                'ar': "🤷‍♂️ لم يتم العثور على مستخدمين حتى الآن.",
                'zh': "🤷‍♂️ 尚未找到任何用户。"
            }
            await update.message.reply_text(
                no_users_text.get(lang, no_users_text['uz']),
                reply_markup=users_keyboard(lang)
            )
            return MENU
        
        users_text = {
            'uz': f"🗑️ O'CHIRISH UCHUN FOYDALANUVCHILAR RO'YXATI:\n\nFoydalanuvchilar soni: {len(users)}\n\nO'chirish uchun foydalanuvchi raqamini yuboring:\n",
            'ru': f"🗑️ СПИСОК ПОЛЬЗОВАТЕЛЕЙ ДЛЯ УДАЛЕНИЯ:\n\nКоличество пользователей: {len(users)}\n\nОтправьте номер пользователя для удаления:\n",
            'en': f"🗑️ USERS LIST FOR DELETION:\n\nNumber of users: {len(users)}\n\nSend user number to delete:\n",
            'fa': f"🗑️ لیست کاربران برای حذف:\n\nتعداد کاربران: {len(users)}\n\nشماره کاربر را برای حذف ارسال کنید:\n",
            'ar': f"🗑️ قائمة المستخدمين للحذف:\n\nعدد المستخدمين: {len(users)}\n\nأرسل رقم المستخدم للحذف:\n",
            'zh': f"🗑️ 要删除的用户列表:\n\n用户数量: {len(users)}\n\n发送要删除的用户编号:\n"
        }
        
        full_message = users_text.get(lang, users_text['uz'])
        
        for i, user in enumerate(users, 1):
            user_details = (
                f"{i}. 👤 Ism: {user.get('first_name', 'Noma\'lum')}\n"
                f"   📞 Telefon: {user.get('phone_number', 'Kiritilmagan')}\n"
                f"   🆔 ID: {user.get('chat_id', 'Noma\'lum')}\n"
            )
            if user.get('username'):
                user_details += f"   👤 Username: @{user.get('username')}\n"
            if user.get('language'):
                user_details += f"   🌐 Til: {user.get('language')}\n"
            user_details += f"   📅 Ro'yxatdan o'tgan: {user.get('timestamp', '')[:16]}\n\n"
            
            full_message += user_details
        
        if len(full_message) > 4000:
            parts = [full_message[i:i+4000] for i in range(0, len(full_message), 4000)]
            for part in parts:
                await update.message.reply_text(part)
        else:
            await update.message.reply_text(full_message)
        
        user_data[chat_id]['delete_mode'] = 'user'
        
        await update.message.reply_text(
            "O'chirish uchun foydalanuvchi raqamini kiriting yoki 'Orqaga' tugmasini bosing:" if lang == 'uz' else "Enter user number to delete or press 'Back':",
            reply_markup=order_cancel_keyboard(lang)
        )
        return MENU

    else:
        if user_data.get(chat_id, {}).get('delete_mode'):
            delete_mode = user_data[chat_id]['delete_mode']
            
            try:
                index = int(text) - 1
                
                if delete_mode == 'order':
                    deleted_order = delete_order_by_index(index)
                    if deleted_order:
                        success_text = {
                            'uz': f"✅ Buyurtma muvaffaqiyatli o'chirildi!\n\n👤 Mijoz: {deleted_order.get('client_name', 'Noma\'lum')}\n🛒 Mahsulot: {deleted_order.get('product', 'Noma\'lum')}",
                            'ru': f"✅ Заказ успешно удален!\n\n👤 Клиент: {deleted_order.get('client_name', 'Неизвестно')}\n🛒 Продукт: {deleted_order.get('product', 'Неизвестно')}",
                            'en': f"✅ Order successfully deleted!\n\n👤 Client: {deleted_order.get('client_name', 'Unknown')}\n🛒 Product: {deleted_order.get('product', 'Unknown')}",
                            'fa': f"✅ سفارش با موفقیت حذف شد!\n\n👤 مشتری: {deleted_order.get('client_name', 'ناشناس')}\n🛒 محصول: {deleted_order.get('product', 'ناشناس')}",
                            'ar': f"✅ تم حذف الطلب بنجاح!\n\n👤 العميل: {deleted_order.get('client_name', 'غير معروف')}\n🛒 المنتج: {deleted_order.get('product', 'غير معروف')}",
                            'zh': f"✅ 订单已成功删除!\n\n👤 客户: {deleted_order.get('client_name', '未知')}\n🛒 产品: {deleted_order.get('product', '未知')}"
                        }
                        await update.message.reply_text(
                            success_text.get(lang, success_text['uz']),
                            reply_markup=applications_keyboard(lang)
                        )
                    else:
                        error_text = {
                            'uz': "❌ Noto'g'ri buyurtma raqami kiritildi.",
                            'ru': "❌ Введен неверный номер заказа.",
                            'en': "❌ Invalid order number entered.",
                            'fa': "❌ شماره سفارش نامعتبر وارد شد.",
                            'ar': "❌ تم إدخال رقم طلب غير صالح.",
                            'zh': "❌ 输入的订单编号无效。"
                        }
                        await update.message.reply_text(
                            error_text.get(lang, error_text['uz']),
                            reply_markup=applications_keyboard(lang)
                        )
                
                elif delete_mode == 'logistics':
                    deleted_request = delete_logistics_by_index(index)
                    if deleted_request:
                        success_text = {
                            'uz': f"✅ Logistika so'rovi muvaffaqiyatli o'chirildi!\n\n📊 Turi: {deleted_request.get('logistics_type', 'Noma\'lum')}\n🌍 Davlat: {deleted_request.get('country', 'Noma\'lum')}",
                            'ru': f"✅ Логистический запрос успешно удален!\n\n📊 Тип: {deleted_request.get('logistics_type', 'Неизвестно')}\n🌍 Страна: {deleted_request.get('country', 'Неизвестно')}",
                            'en': f"✅ Logistics request successfully deleted!\n\n📊 Type: {deleted_request.get('logistics_type', 'Unknown')}\n🌍 Country: {deleted_request.get('country', 'Unknown')}",
                            'fa': f"✅ درخواست لجستیکی با موفقیت حذف شد!\n\n📊 نوع: {deleted_request.get('logistics_type', 'ناشناس')}\n🌍 کشور: {deleted_request.get('country', 'ناشناس')}",
                            'ar': f"✅ تم حذف طلب الخدمات اللوجستية بنجاح!\n\n📊 النوع: {deleted_request.get('logistics_type', 'غير معروف')}\n🌍 الدولة: {deleted_request.get('country', 'غير معروف')}",
                            'zh': f"✅ 物流请求已成功删除!\n\n📊 类型: {deleted_request.get('logistics_type', '未知')}\n🌍 国家: {deleted_request.get('country', '未知')}"
                        }
                        await update.message.reply_text(
                            success_text.get(lang, success_text['uz']),
                            reply_markup=applications_keyboard(lang)
                        )
                    else:
                        error_text = {
                            'uz': "❌ Noto'g'ri so'rov raqami kiritildi.",
                            'ru': "❌ Введен неверный номер запроса.",
                            'en': "❌ Invalid request number entered.",
                            'fa': "❌ شماره درخواست نامعتبر وارد شد.",
                            'ar': "❌ تم إدخال رقم طلب غير صالح.",
                            'zh': "❌ 输入的请求编号无效。"
                        }
                        await update.message.reply_text(
                            error_text.get(lang, error_text['uz']),
                            reply_markup=applications_keyboard(lang)
                        )
                
                elif delete_mode == 'user':
                    deleted_user = delete_user_by_index(index)
                    if deleted_user:
                        success_text = {
                            'uz': f"✅ Foydalanuvchi muvaffaqiyatli o'chirildi!\n\n👤 Ism: {deleted_user.get('first_name', 'Noma\'lum')}\n📞 Telefon: {deleted_user.get('phone_number', 'Kiritilmagan')}",
                            'ru': f"✅ Пользователь успешно удален!\n\n👤 Имя: {deleted_user.get('first_name', 'Неизвестно')}\n📞 Телефон: {deleted_user.get('phone_number', 'Не указан')}",
                            'en': f"✅ User successfully deleted!\n\n👤 Name: {deleted_user.get('first_name', 'Unknown')}\n📞 Phone: {deleted_user.get('phone_number', 'Not provided')}",
                            'fa': f"✅ کاربر با موفقیت حذف شد!\n\n👤 نام: {deleted_user.get('first_name', 'ناشناس')}\n📞 تلفن: {deleted_user.get('phone_number', 'ارائه نشده')}",
                            'ar': f"✅ تم حذف المستخدم بنجاح!\n\n👤 الاسم: {deleted_user.get('first_name', 'غير معروف')}\n📞 الهاتف: {deleted_user.get('phone_number', 'غير مقدم')}",
                            'zh': f"✅ 用户已成功删除!\n\n👤 姓名: {deleted_user.get('first_name', '未知')}\n📞 电话: {deleted_user.get('phone_number', '未提供')}"
                        }
                        await update.message.reply_text(
                            success_text.get(lang, success_text['uz']),
                            reply_markup=users_keyboard(lang)
                        )
                    else:
                        error_text = {
                            'uz': "❌ Noto'g'ri foydalanuvchi raqami kiritildi.",
                            'ru': "❌ Введен неверный номер пользователя.",
                            'en': "❌ Invalid user number entered.",
                            'fa': "❌ شماره کاربر نامعتبر وارد شد.",
                            'ar': "❌ تم إدخال رقم مستخدم غير صالح.",
                            'zh': "❌ 输入的用户编号无效。"
                        }
                        await update.message.reply_text(
                            error_text.get(lang, error_text['uz']),
                            reply_markup=users_keyboard(lang)
                        )
                
                user_data[chat_id]['delete_mode'] = None
                
            except ValueError:
                error_text = {
                    'uz': "❌ Iltimos, raqam kiriting.",
                    'ru': "❌ Пожалуйста, введите число.",
                    'en': "❌ Please enter a number.",
                    'fa': "❌ لطفا یک عدد وارد کنید.",
                    'ar': "❌ يرجى إدخال رقم.",
                    'zh': "❌ 请输入一个数字。"
                }
                await update.message.reply_text(
                    error_text.get(lang, error_text['uz']),
                    reply_markup=admin_panel_keyboard(lang)
                )
            return MENU
        
        await update.message.reply_text(
            "Iltimos, menyudan tanlang." if lang == 'uz' else "Please choose from menu.",
            reply_markup=main_menu_keyboard(lang, chat_id)
        )
        return MENU

async def update_price_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Narxnoma rasmini qabul qilish uchun alohida handler"""
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    b = BUTTONS[lang]
    
    if update.message.text == b['cancel']:
        await update.message.reply_text(
            "Narxnoma yangilash bekor qilindi." if lang == 'uz' else "Price list update cancelled.",
            reply_markup=admin_panel_keyboard(lang)
        )
        return MENU
    
    if update.message.photo:
        # Rasmni saqlash
        photo_file = await update.message.photo[-1].get_file()
        await photo_file.download_to_drive('price_list.jpg')
        
        success_text = {
            'uz': "✅ Narxnoma muvaffaqiyatli yangilandi!",
            'ru': "✅ Прайс-лист успешно обновлен!",
            'en': "✅ Price list successfully updated!",
            'fa': "✅ لیست قیمت با موفقیت بروزرسانی شد!",
            'ar': "✅ تم تحديث قائمة الأسعار بنجاح!",
            'zh': "✅ 价目表已成功更新！"
        }
        
        await update.message.reply_text(
            success_text.get(lang, success_text['uz']),
            reply_markup=admin_panel_keyboard(lang)
        )
        
        return MENU
    else:
        error_text = {
            'uz': "❌ Iltimos, rasm yuboring yoki 'Bekor qilish' tugmasini bosing.",
            'ru': "❌ Пожалуйста, отправьте изображение или нажмите 'Отмена'.",
            'en': "❌ Please send an image or press 'Cancel'.",
            'fa': "❌ لطفا یک تصویر ارسال کنید یا 'لغو' را فشار دهید.",
            'ar': "❌ يرجى إرسال صورة أو الضغط على 'إلغاء'.",
            'zh': "❌ 请发送图片或按'取消'。"
        }
        await update.message.reply_text(
            error_text.get(lang, error_text['uz']),
            reply_markup=order_cancel_keyboard(lang)
        )
        return UPDATE_PRICE

async def broadcast_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xabarni qabul qilish va tasdiqlash"""
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    b = BUTTONS[lang]
    
    if update.message.text == b['cancel']:
        await update.message.reply_text(
            "Xabar yuborish bekor qilindi." if lang == 'uz' else "Message sending cancelled.",
            reply_markup=admin_panel_keyboard(lang)
        )
        return MENU
    
    # Xabarni saqlash
    if update.message.text:
        user_data[chat_id]['broadcast_content'] = update.message.text
        user_data[chat_id]['broadcast_type'] = 'text'
        user_data[chat_id]['broadcast_caption'] = update.message.text
        
        preview_text = {
            'uz': f"📋 Xabar ko'rinishi:\n\n{update.message.text}\n\n✅ Xabarni barcha foydalanuvchilarga yuborish uchun 'Foydalanuvchilarga xabar yuborish' tugmasini bosing:",
            'ru': f"📋 Предварительный просмотр сообщения:\n\n{update.message.text}\n\n✅ Нажмите 'Отправить сообщение пользователям' для отправки сообщения всем пользователям:",
            'en': f"📋 Message preview:\n\n{update.message.text}\n\n✅ Press 'Send message to users' to send the message to all users:",
            'fa': f"📋 پیش نمایش پیام:\n\n{update.message.text}\n\n✅ برای ارسال پیام به همه کاربران، 'ارسال پیام به کاربران' را فشار دهید:",
            'ar': f"📋 معاينة الرسالة:\n\n{update.message.text}\n\n✅ اضغط على 'إرسال رسالة للمستخدمين' لإرسال الرسالة إلى جميع المستخدمين:",
            'zh': f"📋 消息预览:\n\n{update.message.text}\n\n✅ 按'向用户发送消息'将消息发送给所有用户:"
        }
        
        await update.message.reply_text(
            preview_text.get(lang, preview_text['uz']),
            reply_markup=broadcast_confirm_keyboard(lang)
        )
        
    elif update.message.photo:
        user_data[chat_id]['broadcast_content'] = update.message.photo[-1].file_id
        user_data[chat_id]['broadcast_type'] = 'photo'
        user_data[chat_id]['broadcast_caption'] = update.message.caption or ""
        
        caption_preview = update.message.caption or ("Yo'q" if lang == 'uz' else "None" if lang == 'en' else "Нет" if lang == 'ru' else "ندارد" if lang == 'fa' else "لا شيء" if lang == 'ar' else "无")
        
        preview_text = {
            'uz': f"🖼️ Rasm yuboriladi\n\nSarlavha: {caption_preview}\n\n✅ Rasmni barcha foydalanuvchilarga yuborish uchun 'Foydalanuvchilarga xabar yuborish' tugmasini bosing:",
            'ru': f"🖼️ Будет отправлено изображение\n\nПодпись: {caption_preview}\n\n✅ Нажмите 'Отправить сообщение пользователям' для отправки изображения всем пользователям:",
            'en': f"🖼️ Image will be sent\n\nCaption: {caption_preview}\n\n✅ Press 'Send message to users' to send the image to all users:",
            'fa': f"🖼️ تصویر ارسال خواهد شد\n\nعنوان: {caption_preview}\n\n✅ برای ارسال تصویر به همه کاربران، 'ارسال پیام به کاربران' را فشار دهید:",
            'ar': f"🖼️ سيتم إرسال الصورة\n\nالتسمية: {caption_preview}\n\n✅ اضغط على 'إرسال رسالة للمستخدمين' لإرسال الصورة إلى جميع المستخدمين:",
            'zh': f"🖼️ 将发送图片\n\n标题: {caption_preview}\n\n✅ 按'向用户发送消息'将图片发送给所有用户:"
        }
        
        await update.message.reply_text(
            preview_text.get(lang, preview_text['uz']),
            reply_markup=broadcast_confirm_keyboard(lang)
        )
        
    elif update.message.video:
        user_data[chat_id]['broadcast_content'] = update.message.video.file_id
        user_data[chat_id]['broadcast_type'] = 'video'
        user_data[chat_id]['broadcast_caption'] = update.message.caption or ""
        
        caption_preview = update.message.caption or ("Yo'q" if lang == 'uz' else "None" if lang == 'en' else "Нет" if lang == 'ru' else "ندارد" if lang == 'fa' else "لا شيء" if lang == 'ar' else "无")
        
        preview_text = {
            'uz': f"🎥 Video yuboriladi\n\nSarlavha: {caption_preview}\n\n✅ Videoni barcha foydalanuvchilarga yuborish uchun 'Foydalanuvchilarga xabar yuborish' tugmasini bosing:",
            'ru': f"🎥 Будет отправлено видео\n\nПодпись: {caption_preview}\n\n✅ Нажмите 'Отправить сообщение пользователям' для отправки видео всем пользователям:",
            'en': f"🎥 Video will be sent\n\nCaption: {caption_preview}\n\n✅ Press 'Send message to users' to send the video to all users:",
            'fa': f"🎥 ویدیو ارسال خواهد شد\n\nعنوان: {caption_preview}\n\n✅ برای ارسال ویدیو به همه کاربران، 'ارسال پیام به کاربران' را فشار دهید:",
            'ar': f"🎥 سيتم إرسال الفيديو\n\nالتسمية: {caption_preview}\n\n✅ اضغط على 'إرسال رسالة للمستخدمين' لإرسال الفيديو إلى جميع المستخدمين:",
            'zh': f"🎥 将发送视频\n\n标题: {caption_preview}\n\n✅ 按'向用户发送消息'将视频发送给所有用户:"
        }
        
        await update.message.reply_text(
            preview_text.get(lang, preview_text['uz']),
            reply_markup=broadcast_confirm_keyboard(lang)
        )
    
    else:
        error_text = {
            'uz': "❌ Iltimos, matn, rasm yoki video yuboring yoki 'Bekor qilish' tugmasini bosing.",
            'ru': "❌ Пожалуйста, отправьте текст, изображение или видео, или нажмите 'Отмена'.",
            'en': "❌ Please send text, image or video, or press 'Cancel'.",
            'fa': "❌ لطفا متن، تصویر یا ویدیو ارسال کنید یا 'لغو' را فشار دهید.",
            'ar': "❌ يرجى إرسال نص، صورة أو فيديو، أو الضغط على 'إلغاء'.",
            'zh': "❌ 请发送文本、图片或视频，或按'取消'。"
        }
        await update.message.reply_text(
            error_text.get(lang, error_text['uz']),
            reply_markup=order_cancel_keyboard(lang)
        )
        return BROADCAST_MESSAGE
    
    return BROADCAST_CONFIRM

async def broadcast_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xabarni yuborishni tasdiqlash"""
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    b = BUTTONS[lang]
    
    if update.message.text == b['cancel']:
        await update.message.reply_text(
            "Xabar yuborish bekor qilindi." if lang == 'uz' else "Message sending cancelled.",
            reply_markup=admin_panel_keyboard(lang)
        )
        return MENU
    
    if update.message.text == b['broadcast']:
        # Xabarni yuborish
        sending_text = {
            'uz': "⏳ Xabar barcha foydalanuvchilarga yuborilmoqda...",
            'ru': "⏳ Сообщение отправляется всем пользователям...",
            'en': "⏳ Sending message to all users...",
            'fa': "⏳ در حال ارسال پیام به همه کاربران...",
            'ar': "⏳ جاري إرسال الرسالة إلى جميع المستخدمين...",
            'zh': "⏳ 正在向所有用户发送消息..."
        }
        
        await update.message.reply_text(
            sending_text.get(lang, sending_text['uz'])
        )
        
        success_count, fail_count = await send_broadcast_message(
            context, 
            user_data[chat_id]['broadcast_content'],
            user_data[chat_id]['broadcast_type'],
            user_data[chat_id]['broadcast_caption']
        )
        
        # Natijani xabar qilish
        result_text = {
            'uz': f"✅ Xabar yuborish yakunlandi!\n\n📊 Natijalar:\n✅ Muvaffaqiyatli: {success_count} ta\n❌ Muvaffaqiyatsiz: {fail_count} ta\n👥 Jami: {success_count + fail_count} ta",
            'ru': f"✅ Рассылка завершена!\n\n📊 Результаты:\n✅ Успешно: {success_count}\n❌ Неудачно: {fail_count}\n👥 Всего: {success_count + fail_count}",
            'en': f"✅ Broadcast completed!\n\n📊 Results:\n✅ Successful: {success_count}\n❌ Failed: {fail_count}\n👥 Total: {success_count + fail_count}",
            'fa': f"✅ ارسال پیام تکمیل شد!\n\n📊 نتایج:\n✅ موفق: {success_count}\n❌ ناموفق: {fail_count}\n👥 کل: {success_count + fail_count}",
            'ar': f"✅ اكتمل البث!\n\n📊 النتائج:\n✅ ناجح: {success_count}\n❌ فاشل: {fail_count}\n👥 الإجمالي: {success_count + fail_count}",
            'zh': f"✅ 广播完成!\n\n📊 结果:\n✅ 成功: {success_count}\n❌ 失败: {fail_count}\n👥 总计: {success_count + fail_count}"
        }
        
        await update.message.reply_text(
            result_text.get(lang, result_text['uz']),
            reply_markup=admin_panel_keyboard(lang)
        )
        
        # Ma'lumotlarni tozalash
        if 'broadcast_content' in user_data[chat_id]:
            del user_data[chat_id]['broadcast_content']
        if 'broadcast_type' in user_data[chat_id]:
            del user_data[chat_id]['broadcast_type']
        if 'broadcast_caption' in user_data[chat_id]:
            del user_data[chat_id]['broadcast_caption']
            
        return MENU
    
    return BROADCAST_CONFIRM

async def logistics_type_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    text = update.message.text
    b = BUTTONS[lang]

    if text == b['back']:
        await update.message.reply_text(
            "Asosiy menyu" if lang == 'uz' else "Main menu", 
            reply_markup=main_menu_keyboard(lang, chat_id)
        )
        return MENU

    if text in [b['import'], b['export']]:
        user_data[chat_id]['logistics_type'] = text
        
        country_text = {
            'uz': f"🌍 {text} qilmoqchi bo'lgan davlatni tanlang:",
            'ru': f"🌍 Выберите страну для {text.lower()}:",
            'en': f"🌍 Select country for {text.lower()}:",
            'fa': f"🌍 کشور مورد نظر برای {text.lower()} را انتخاب کنید:",
            'ar': f"🌍 اختر الدولة لل{text.lower()}:",
            'zh': f"🌍 选择{text.lower()}的国家:"
        }
        
        await update.message.reply_text(
            country_text.get(lang, country_text['uz']),
            reply_markup=logistics_country_keyboard(lang)
        )
        return LOGISTICS_COUNTRY

    await update.message.reply_text(
        "Iltimos, import yoki exportni tanlang." if lang == 'uz' else "Please choose import or export.",
        reply_markup=logistics_type_keyboard(lang)
    )
    return LOGISTICS_TYPE

async def logistics_country_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    text = update.message.text
    b = BUTTONS[lang]

    if text == b['back']:
        await update.message.reply_text(
            "Logistika xizmatlari" if lang == 'uz' else "Logistics services",
            reply_markup=logistics_type_keyboard(lang)
        )
        return LOGISTICS_TYPE

    countries = {
        'uz': ["Xitoy 🇨🇳", "Eron 🇮🇷", "Rossiya 🇷🇺", "Qozog'iston 🇰🇿", "Tojikiston 🇹🇯", "Turkmaniston 🇹🇲", "Hindiston 🇮🇳"],
        'ru': ["Китай 🇨🇳", "Иран 🇮🇷", "Россия 🇷🇺", "Казахстан 🇰🇿", "Таджикистан 🇹🇯", "Туркменистан 🇹🇲", "Индия 🇮🇳"],
        'en': ["China 🇨🇳", "Iran 🇮🇷", "Russia 🇷🇺", "Kazakhstan 🇰🇿", "Tajikistan 🇹🇯", "Turkmenistan 🇹🇲", "India 🇮🇳"],
        'fa': ["چین 🇨🇳", "ایران 🇮🇷", "روسیه 🇷🇺", "قزاقستان 🇰🇿", "تاجیکستان 🇹🇯", "ترکمنستان 🇹🇲", "هند 🇮🇳"],
        'ar': ["الصين 🇨🇳", "إيران 🇮🇷", "روسيا 🇷🇺", "كازاخستان 🇰🇿", "طاجيكستان 🇹🇯", "تركمانستان 🇹🇲", "الهند 🇮🇳"],
        'zh': ["中国 🇨🇳", "伊朗 🇮🇷", "俄罗斯 🇷🇺", "哈萨克斯坦 🇰🇿", "塔吉克斯坦 🇹🇯", "土库曼斯坦 🇹🇲", "印度 🇮🇳"]
    }
    
    country_list = countries.get(lang, countries['uz'])
    
    if text in country_list:
        user_data[chat_id]['logistics_country'] = text
        
        phone_text = {
            'uz': "📞📲 Telefon raqamingizni yuboring:\n\nIltimos, quyidagi tugma orqali kontaktni yuboring yoki raqamni yozing:",
            'ru': "📞📲 Отправьте ваш номер телефона:\n\nПожалуйста, отправьте контакт с помощью кнопки ниже или напишите номер:",
            'en': "📞📲 📝 Please leave your phone number 📱\n\n💬 You can share your contact using the button below or type your phone number:",
            'fa': "📞📲 لطفا شماره تلفن خود را وارد کنید:\n\nبا استفاده از دکمه زیر مخاطب را ارسال کنید یا شماره را تایپ کنید:",
            'ar': "📞📲 يرجى ترك رقم هاتفك:\n\nشارك جهة الاتصال باستخدام الزر أدناه أو اكتب الرقم:",
            'zh': "📞📲 请留下您的电话号码:\n\n使用下面的按钮分享联系方式或输入您的电话号码:"
        }
        
        await update.message.reply_text(
            phone_text.get(lang, phone_text['en']),
            reply_markup=logistics_phone_keyboard(lang)
        )
        return LOGISTICS_PHONE

    await update.message.reply_text(
        "Iltimos, davlatlardan birini tanlang." if lang == 'uz' else "Please choose one of the countries.",
        reply_markup=logistics_country_keyboard(lang)
    )
    return LOGISTICS_COUNTRY

async def logistics_phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    text = update.message.text
    b = BUTTONS[lang]

    if text == b['back']:
        await update.message.reply_text(
            "🌍 Davlatni tanlang:" if lang == 'uz' else "🌍 Select country:",
            reply_markup=logistics_country_keyboard(lang)
        )
        return LOGISTICS_COUNTRY

    phone_number = None
    
    if update.message.contact:
        phone_number = update.message.contact.phone_number
        user_data[chat_id]['logistics_phone'] = phone_number
    elif text and not text == b['back']:
        phone_number = text
        user_data[chat_id]['logistics_phone'] = phone_number
    else:
        await update.message.reply_text(
            "Iltimos, telefon raqamingizni yuboring." if lang == 'uz' else "📝 Please leave your phone number 📱",
            reply_markup=logistics_phone_keyboard(lang)
        )
        return LOGISTICS_PHONE

    request_data = {
        'chat_id': chat_id,
        'logistics_type': user_data[chat_id]['logistics_type'],
        'country': user_data[chat_id]['logistics_country'],
        'phone': phone_number,
        'language': lang,
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    save_logistics_request(request_data)
    
    try:
        logistics_type_uz = "Import" if user_data[chat_id]['logistics_type'] == BUTTONS['uz']['import'] else "Export"
        logistics_type_en = "Import" if user_data[chat_id]['logistics_type'] == BUTTONS['en']['import'] else "Export"
        
        admin_message = (
            f"🚚 YANGI LOGISTIKA SO'ROVI!\n"
            f"📊 Turi: {logistics_type_uz}\n"
            f"🌍 Davlat: {user_data[chat_id]['logistics_country']}\n"
            f"📞 Telefon: {phone_number}\n"
            f"🌐 Til: {lang}\n"
            f"🆔 Chat ID: {chat_id}\n"
            f"⏰ Vaqt: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"👤 Foydalanuvchi: {update.effective_user.first_name or 'Noma\'lum'}"
        )
        await context.bot.send_message(ADMIN_CHAT_IDS[0], admin_message)
    except Exception as e:
        print(f"Adminga logistika so'rovini yuborishda xatolik: {e}")
    
    success_text = {
        'uz': "🎉🤝 Murojaatingiz ko'rib chiqilmoqda! 📋\n\n💼 Siz bilan tez orada managerlarimiz bog'lanishadi 📞\n\n⏳ Iltimos, kutib turing... 🙏\n\n✅ Rahmat!",
        'ru': "🎉🤝 Ваша заявка рассматривается! 📋\n\n💼 Наши менеджеры свяжутся с вами в ближайшее время 📞\n\n⏳ Пожалуйста, подождите... 🙏\n\n✅ Спасибо!",
        'en': "🎉🤝 Your request is being reviewed! 📋\n\n💼 Our managers will contact you shortly 📞\n\n⏳ Please wait... 🙏\n\n✅ Thank you!",
        'fa': "🎉🤝 درخواست شما در حال بررسی است! 📋\n\n💼 مدیران ما به زودی با شما تماس خواهند گرفت 📞\n\n⏳ لطفا صبر کنید... 🙏\n\n✅ متشکرم!",
        'ar': "🎉🤝 طلبك قيد المراجعة! 📋\n\n💼 سيتصل بك مديرونا قريبًا 📞\n\n⏳ يرجى الانتظار... 🙏\n\n✅ شكرا!",
        'zh': "🎉🤝 您的请求正在审核中！ 📋\n\n💼 我们的经理很快就会与您联系 📞\n\n⏳ 请稍候... 🙏\n\n✅ 谢谢！"
    }
    
    await update.message.reply_text(
        success_text.get(lang, success_text['uz']),
        reply_markup=main_menu_keyboard(lang, chat_id)
    )
    
    if 'logistics_type' in user_data[chat_id]:
        del user_data[chat_id]['logistics_type']
    if 'logistics_country' in user_data[chat_id]:
        del user_data[chat_id]['logistics_country']
    if 'logistics_phone' in user_data[chat_id]:
        del user_data[chat_id]['logistics_phone']
            
    return MENU

async def products_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    text = update.message.text
    
    if text == BUTTONS[lang]['back']:
        await update.message.reply_text(
            "Asosiy menyu" if lang == 'uz' else "Main menu", 
            reply_markup=main_menu_keyboard(lang, chat_id)
        )
        return MENU

    prods = PRODUCTS_DICT.get(lang, PRODUCTS_DICT['uz'])
    
    if text in prods:
        user_data[chat_id]['selected_product'] = text
        
        product_images = {
            prods[0]: ["photo_1_2025-10-11_18-39-59.jpg", "photo_2_2025-10-11_18-39-59.jpg"],
            prods[1]: ["photo_6_2025-10-11_14-01-27.jpg", "photo_4_2025-10-11_14-01-27.jpg", "photo_2025-10-12_19-02-31.jpg", "photo_10_2025-10-11_14-01-27.jpg"],
            prods[3]: ["photo_2025-10-12_19-40-07.jpg", "photo_2025-10-12_19-40-15.jpg"],
            prods[5]: ["photo_1_2025-10-12_20-08-30.jpg", "photo_2_2025-10-12_20-08-30.jpg", "photo_3_2025-10-12_20-08-30.jpg"],
            prods[6]: ["photo_1_2025-10-13_09-14-19.jpg", "photo_2_2025-10-13_09-14-19.jpg"],
            prods[7]: ["photo_1_2025-10-13_10-21-21.jpg", "photo_2_2025-10-13_10-21-21.jpg"],
            prods[8]: ["photo_1_2025-10-13_10-48-33.jpg", "photo_2_2025-10-13_10-48-33.jpg", "photo_3_2025-10-13_10-48-33.jpg"],
            prods[9]: ["photo_2202.jpg"],
            prods[10]: ["photo_1_2025-10-13_12-43-28.jpg", "photo_3_2025-10-13_12-43-28.jpg", "photo_2_2025-10-13_12-43-28.jpg"],
            prods[11]: ["photo_2025-10-13_17-11-05.jpg"]
        }
        
        try:
            images = product_images.get(text, [])
            
            for image_file in images:
                try:
                    with open(image_file, "rb") as photo:
                        await update.message.reply_photo(
                            photo=photo,
                            caption=""
                        )
                except FileNotFoundError:
                    print(f"Rasm topilmadi: {image_file}")
                    continue
            
            packaging_text = "IBC/DRUM"
            if any(keyword in text.lower() for keyword in ["caustic", "bicarbonate", "сода", "бикарбонат", "سود", "بيكربونات", "氢氧化钠", "碳酸氢钠"]):
                packaging_text = "25kg/1250 Jambo"
            
            product_info = {
                'uz': f"⚠️ DIQQAT, ELON!\n\n🛒 Tovar: {text}\n🏭 Ishlab chiqaruvchi: {'Xitoy' if 'Xitoy' in text or 'China' in text else 'Eron'}\n🤝 Yetkazib beruvchi: MASTER BROTHER\n📅 Ishlab chiqarilgan vaqti: 2025-YIL\n📜 Sertifikatlar: mavjud\n💳 To'lov shartlari: Ixtiyoriy\n📦 Upakovka: {packaging_text}\n📍 Ortish manzili: Buxoro viloyati, Peshku tumani",
                'ru': f"⚠️ ВНИМАНИЕ, ОБЪЯВЛЕНИЕ!\n\n🛒 Товар: {text}\n🏭 Производитель: {'Китай' if 'Китай' in text or 'China' in text else 'Иран'}\n🤝 Поставщик: MASTER BROTHER\n📅 Дата производства: 2025 ГОД\n📜 Сертификаты: имеются\n💳 Условия оплаты: Любые\n📦 Упаковка: {packaging_text}\n📍 Адрес отгрузки: Бухарская область, Пешку район",
                'en': f"⚠️ ATTENTION, ANNOUNCEMENT!\n\n🛒 Product: {text}\n🏭 Manufacturer: {'China' if 'China' in text or 'Xitoy' in text else 'Iran'}\n🤝 Supplier: MASTER BROTHER\n📅 Production date: 2025 YEAR\n📜 Certificates: available\n💳 Payment terms: Optional\n📦 Packaging: {packaging_text}\n📍 Shipping address: Bukhara region, Peshku district",
                'fa': f"⚠️ توجه، اطلاعیه!\n\n🛒 کالا: {text}\n🏭 تولید کننده: {'چین' if 'چین' in text or 'China' in text else 'ایران'}\n🤝 تامین کننده: MASTER BROTHER\n📅 تاریخ تولید: سال 2025\n📜 گواهی‌ها: موجود\n💳 شرایط پرداخت: اختیاری\n📦 بسته‌بندی: {packaging_text}\n📍 آدرس حمل: استان بخارا، منطقه پشتک",
                'ar': f"⚠️ انتباه، إعلان!\n\n🛒 المنتج: {text}\n🏭 الصانع: {'الصين' if 'الصين' in text or 'China' in text else 'إيران'}\n🤝 المورد: MASTER BROTHER\n📅 تاريخ الإنتاج: عام 2025\n📜 الشهادات: متوفرة\n💳 شروط الدفع: اختياري\n📦 التعبئة: {packaging_text}\n📍 عنوان الشحن: منطقة بخارى، منطقة بيشكو",
                'zh': f"⚠️ 注意，公告!\n\n🛒 产品: {text}\n🏭 制造商: {'中国' if '中国' in text or 'China' in text else '伊朗'}\n🤝 供应商: MASTER BROTHER\n📅 生产日期: 2025年\n📜 证书: 可用\n💳 付款条件: 可选\n📦 包装: {packaging_text}\n📍 发货地址: 布哈拉州，佩什库区"
            }
            
            await update.message.reply_text(
                product_info.get(lang, product_info['en'])
            )
            
            order_menu_text = {
                'uz': "🎯 Agar ushbu mahsulotni buyurtma qilmoqchi bo'lsangiz, quyidagi tugmani bosing:",
                'ru': "🎯 Если вы хотите заказать этот продукт, нажмите кнопку ниже:",
                'en': "🎯 If you want to order this product, press the button below:",
                'fa': "🎯 اگر می‌خواهید این محصول را سفارش دهید، دکمه زیر را فشار دهید:",
                'ar': "🎯 إذا كنت ترغب في طلب هذا المنتج، اضغط على الزر أدناه:",
                'zh': "🎯 如果您想订购此产品，请按下面的按钮:"
            }
            
            await update.message.reply_text(
                order_menu_text.get(lang, order_menu_text['en']),
                reply_markup=order_menu_keyboard(lang)
            )
            
        except Exception as e:
            error_text = {
                'uz': f"❌ Rasm topilmadi. Iltimos, admin bilan bog'laning.\n\nSiz tanlagan mahsulot: {text}",
                'ru': f"❌ Изображение не найдено. Пожалуйста, свяжитесь с администратором.\n\nВыбранный продукт: {text}",
                'en': f"❌ Image not found. Please contact admin.\n\nSelected product: {text}",
                'fa': f"❌ تصویر یافت نشد. لطفا با ادمین تماس بگیرید.\n\nمحصول انتخاب شده: {text}",
                'ar': f"❌ الصورة غير موجودة. يرجى الاتصال بالمسؤول.\n\nالمنتج المحدد: {text}",
                'zh': f"❌ 图片未找到。请联系管理员。\n\n选择的产品: {text}"
            }
            await update.message.reply_text(
                error_text.get(lang, error_text['en']),
                reply_markup=products_keyboard(lang)
            )
        return MENU

    await update.message.reply_text(
        "Iltimos, mahsulotlardan tanlang yoki 'Orqaga' tugmasini bosing." if lang == 'uz' else "Please choose a product or press 'Back'.",
        reply_markup=products_keyboard(lang)
    )
    return PRODUCTS

async def order_name_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    text = update.message.text
    
    if text == BUTTONS[lang]['cancel']:
        await update.message.reply_text(
            "Buyurtma bekor qilindi." if lang == 'uz' else "Order cancelled.",
            reply_markup=main_menu_keyboard(lang, chat_id)
        )
        return MENU
    
    user_data[chat_id]['order_name'] = text
    
    if user_data[chat_id].get('selected_product'):
        product_name = user_data[chat_id]['selected_product']
        
        if any(keyword in product_name for keyword in ["Longi panel", "Панель Longi", "پنل Longi", "لوحة Longi", "隆基面板"]):
            phone_text = {
                'uz': "✅ Mijoz ma'lumotlari qabul qilindi! 🎉\n\n2. 📞 Telefon raqamingizni kiriting:",
                'ru': "✅ Данные клиента приняты! 🎉\n\n2. 📞 Введите ваш номер телефона:",
                'en': "✅ Client information received! 🎉\n\n2. 📞 Enter your phone number:",
                'fa': "✅ اطلاعات مشتری دریافت شد! 🎉\n\n2. 📞 شماره تلفن خود را وارد کنید:",
                'ar': "✅ تم استلام معلومات العميل! 🎉\n\n2. 📞 أدخل رقم هاتفك:",
                'zh': "✅ 客户信息已收到! 🎉\n\n2. 📞 输入您的电话号码:"
            }
            
            await update.message.reply_text(
                phone_text.get(lang, phone_text['en']),
                reply_markup=order_cancel_keyboard(lang)
            )
            user_data[chat_id]['order_product'] = product_name
            user_data[chat_id]['is_longi'] = True
            return ORDER_PHONE
        else:
            user_data[chat_id]['order_product'] = product_name
            quantity_text = {
                'uz': "✅ Mijoz ma'lumotlari qabul qilindi! 🎉\n\n2. Mahsulot miqdorini kiriting (tonnada):",
                'ru': "✅ Данные клиента приняты! 🎉\n\n2. Введите количество продукта (в тоннах):",
                'en': "✅ Client information received! 🎉\n\n2. Enter product quantity (in tons):",
                'fa': "✅ اطلاعات مشتری دریافت شد! 🎉\n\n2. مقدار محصول را وارد کنید (بر حسب تن):",
                'ar': "✅ تم استلام معلومات العميل! 🎉\n\n2. أدخل كمية المنتج (بالأطنان):",
                'zh': "✅ 客户信息已收到! 🎉\n\n2. 输入产品数量 (按吨):"
            }
            await update.message.reply_text(
                quantity_text.get(lang, quantity_text['uz']),
                reply_markup=order_cancel_keyboard(lang)
            )
            return ORDER_QUANTITY
    else:
        product_text = {
            'uz': "✅ Mijoz ma'lumotlari qabul qilindi! 🎉\n\n2. Mahsulot nomini kiriting (to'liq):",
            'ru': "✅ Данные клиента приняты! 🎉\n\n2. Введите название продукта (полностью):",
            'en': "✅ Client information received! 🎉\n\n2. Enter product name (full):",
            'fa': "✅ اطلاعات مشتری دریافت شد! 🎉\n\n2. نام محصول را وارد کنید (کامل):",
            'ar': "✅ تم استلام معلومات العميل! 🎉\n\n2. أدخل اسم المنتج (كامل):",
            'zh': "✅ 客户信息已收到! 🎉\n\n2. 输入产品名称 (完整):"
        }
        await update.message.reply_text(
            product_text.get(lang, product_text['uz']),
            reply_markup=order_cancel_keyboard(lang)
        )
        return ORDER_PRODUCT

async def order_product_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    text = update.message.text
    
    if text == BUTTONS[lang]['cancel']:
        await update.message.reply_text(
            "Buyurtma bekor qilindi." if lang == 'uz' else "Order cancelled.",
            reply_markup=main_menu_keyboard(lang, chat_id)
        )
        return MENU
    
    user_data[chat_id]['order_product'] = text
    
    if any(keyword in text for keyword in ["Longi panel", "Панель Longi", "پنل Longi", "لوحة Longi", "隆基面板"]):
        phone_text = {
            'uz': "✅ Mahsulot nomi qabul qilindi! 🎉\n\n2. 📞 Telefon raqamingizni kiriting:",
            'ru': "✅ Название продукта принято! 🎉\n\n2. 📞 Введите ваш номер телефона:",
            'en': "✅ Product name received! 🎉\n\n2. 📞 Enter your phone number:",
            'fa': "✅ نام محصول دریافت شد! 🎉\n\n2. 📞 شماره تلفن خود را وارد کنید:",
            'ar': "✅ تم استلام اسم المنتج! 🎉\n\n2. 📞 أدخل رقم هاتفك:",
            'zh': "✅ 产品名称已收到! 🎉\n\n2. 📞 输入您的电话号码:"
        }
        
        await update.message.reply_text(
            phone_text.get(lang, phone_text['en']),
            reply_markup=order_cancel_keyboard(lang)
        )
        user_data[chat_id]['is_longi'] = True
        return ORDER_PHONE
    else:
        quantity_text = {
            'uz': "✅ Mahsulot nomi qabul qilindi! 🎉\n\n3. Mahsulot miqdorini kiriting (tonnada):",
            'ru': "✅ Название продукта принято! 🎉\n\n3. Введите количество продукта (в тоннах):",
            'en': "✅ Product name received! 🎉\n\n3. Enter product quantity (in tons):",
            'fa': "✅ نام محصول دریافت شد! 🎉\n\n3. مقدار محصول را وارد کنید (بر حسب تن):",
            'ar': "✅ تم استلام اسم المنتج! 🎉\n\n3. أدخل كمية المنتج (بالأطنان):",
            'zh': "✅ 产品名称已收到! 🎉\n\n3. 输入产品数量 (按吨):"
        }
        await update.message.reply_text(
            quantity_text.get(lang, quantity_text['uz']),
            reply_markup=order_cancel_keyboard(lang)
        )
        return ORDER_QUANTITY

async def order_quantity_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    text = update.message.text
    
    if text == BUTTONS[lang]['cancel']:
        await update.message.reply_text(
            "Buyurtma bekor qilindi." if lang == 'uz' else "Order cancelled.",
            reply_markup=main_menu_keyboard(lang, chat_id)
        )
        return MENU
    
    user_data[chat_id]['order_quantity'] = text
    
    phone_text = {
        'uz': "✅ Mahsulot miqdori qabul qilindi! 🎉\n\n4. 📞 Telefon raqamingizni kiriting:",
        'ru': "✅ Количество продукта принято! 🎉\n\n4. 📞 Введите ваш номер телефона:",
        'en': "✅ Product quantity received! 🎉\n\n4. 📞 Enter your phone number:",
        'fa': "✅ مقدار محصول دریافت شد! 🎉\n\n4. 📞 شماره تلفن خود را وارد کنید:",
        'ar': "✅ تم استلام كمية المنتج! 🎉\n\n4. 📞 أدخل رقم هاتفك:",
        'zh': "✅ 产品数量已收到! 🎉\n\n4. 📞 输入您的电话号码:"
    }
    await update.message.reply_text(
        phone_text.get(lang, phone_text['uz']),
        reply_markup=order_cancel_keyboard(lang)
    )
    return ORDER_PHONE

async def order_phone_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    lang = user_data[chat_id].get('lang', 'uz')
    text = update.message.text
    
    if text == BUTTONS[lang]['cancel']:
        await update.message.reply_text(
            "Buyurtma bekor qilindi." if lang == 'uz' else "Order cancelled.",
            reply_markup=main_menu_keyboard(lang, chat_id)
        )
        return MENU
    
    user_data[chat_id]['order_phone'] = text
    
    product_name = user_data[chat_id].get('selected_product', user_data[chat_id]['order_product'])
    
    order_data = {
        'chat_id': chat_id,
        'client_name': user_data[chat_id]['order_name'],
        'product': product_name,
        'phone': user_data[chat_id]['order_phone'],
        'language': lang,
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    if user_data[chat_id].get('is_longi'):
        order_data['is_longi'] = True
    else:
        order_data['quantity'] = user_data[chat_id]['order_quantity']
    
    save_order(order_data)
    
    try:
        admin_message = (
            f"🆕 YANGI BUYURTMA!\n"
            f"👤 Mijoz: {order_data['client_name']}\n"
            f"🛒 Mahsulot: {order_data['product']}\n"
        )
        
        if user_data[chat_id].get('is_longi'):
            admin_message += f"📋 Turi: Longi panel (o'rnatish uchun zayavka)\n"
        else:
            admin_message += f"⚖️ Miqdor: {order_data['quantity']} tonna\n"
        
        admin_message += (
            f"📞 Telefon: {order_data['phone']}\n"
            f"🌐 Til: {order_data['language']}\n"
            f"🆔 Chat ID: {order_data['chat_id']}\n"
            f"⏰ Vaqt: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        
        await context.bot.send_message(ADMIN_CHAT_IDS[0], admin_message)
    except Exception as e:
        print(f"Adminga buyurtma xabarini yuborishda xatolik: {e}")
    
    success_text = {
        'uz': "🎉 Buyurtmangiz qabul qilindi! 🤝\n\nTez orada siz bilan bog'lanamiz. 📞\n\n📋 Buyurtma tafsilotlari:\n👤 Mijoz: {name}\n🛒 Mahsulot: {product}\n{quantity}📞 Telefon: {phone}",
        'ru': "🎉 Ваш заказ принят! 🤝\n\nСкоро свяжемся с вами. 📞\n\n📋 Детали заказа:\n👤 Клиент: {name}\n🛒 Продукт: {product}\n{quantity}📞 Телефон: {phone}",
        'en': "🎉 Your order has been received! 🤝\n\nWe will contact you soon. 📞\n\n📋 Order details:\n👤 Client: {name}\n🛒 Product: {product}\n{quantity}📞 Phone: {phone}",
        'fa': "🎉 سفارش شما دریافت شد! 🤝\n\nبه زودی با شما تماس خواهیم گرفت. 📞\n\n📋 جزئیات سفارش:\n👤 مشتری: {name}\n🛒 محصول: {product}\n{quantity}📞 تلفن: {phone}",
        'ar': "🎉 تم استلام طلبك! 🤝\n\nسنتصل بك قريبًا. 📞\n\n📋 تفاصيل الطلب:\n👤 العميل: {name}\n🛒 المنتج: {product}\n{quantity}📞 الهاتف: {phone}",
        'zh': "🎉 您的订单已收到! 🤝\n\n我们会尽快与您联系。 📞\n\n📋 订单详情:\n👤 客户: {name}\n🛒 产品: {product}\n{quantity}📞 电话: {phone}"
    }
    
    quantity_info = ""
    if not user_data[chat_id].get('is_longi'):
        quantity_text = {
            'uz': "⚖️ Miqdor: {quantity} tonna\n",
            'ru': "⚖️ Количество: {quantity} тонн\n",
            'en': "⚖️ Quantity: {quantity} tons\n",
            'fa': "⚖️ مقدار: {quantity} تن\n",
            'ar': "⚖️ الكمية: {quantity} طن\n",
            'zh': "⚖️ 数量: {quantity} 吨\n"
        }
        quantity_info = quantity_text.get(lang, quantity_text['en']).format(
            quantity=user_data[chat_id]['order_quantity']
        )
    
    await update.message.reply_text(
        success_text.get(lang, success_text['uz']).format(
            name=order_data['client_name'],
            product=order_data['product'],
            quantity=quantity_info,
            phone=order_data['phone']
        ),
        reply_markup=main_menu_keyboard(lang, chat_id)
    )
    
    keys_to_delete = ['order_name', 'order_product', 'order_quantity', 'order_phone', 'selected_product', 'is_longi']
    for key in keys_to_delete:
        if key in user_data[chat_id]:
            del user_data[chat_id][key]
    
    return MENU

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    conv = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANG: [MessageHandler(filters.TEXT & ~filters.COMMAND, lang_handler)],
            CONTACT: [
                MessageHandler(filters.CONTACT, contact_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, contact_handler)
            ],
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)],
            PRODUCTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, products_handler)],
            ORDER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_name_handler)],
            ORDER_PRODUCT: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_product_handler)],
            ORDER_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_quantity_handler)],
            ORDER_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, order_phone_handler)],
            LOGISTICS_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, logistics_type_handler)],
            LOGISTICS_COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, logistics_country_handler)],
            LOGISTICS_PHONE: [
                MessageHandler(filters.CONTACT, logistics_phone_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, logistics_phone_handler)
            ],
            UPDATE_PRICE: [
                MessageHandler(filters.PHOTO, update_price_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, update_price_handler)
            ],
            BROADCAST_MESSAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_message_handler),
                MessageHandler(filters.PHOTO, broadcast_message_handler),
                MessageHandler(filters.VIDEO, broadcast_message_handler)
            ],
            BROADCAST_CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_confirm_handler)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
        allow_reentry=True
    )
    
    app.add_handler(conv)
    
    print("🤖 Bot ishga tushdi...")
    app.run_polling()

if __name__ == '__main__':
    main()
