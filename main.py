import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib.parse
import os
from flask import Flask
from threading import Thread

# 1. Инициализация
TOKEN = '8971183383:AAEOuF4d9VN2QyygyxbZlCByys_f_BfBmz8'
bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()

# Функции
def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Бумажечка на ножках (15★)", callback_data="opt_1")
    btn2 = InlineKeyboardButton("Рисунок на ляжечках (50★)", callback_data="opt_2")
    btn3 = InlineKeyboardButton("В полный рост с листочком А4 (100★)", callback_data="opt_3")
    btn4 = InlineKeyboardButton("Стоя на коленках / вид сверху (100★)", callback_data="opt_4")
    btn5 = InlineKeyboardButton("Приветствие от фембоя (В разработке...)", callback_data="opt_5")
    btn6 = InlineKeyboardButton("Техподдержка", callback_data="support")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    return markup

# Обработчики
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # --- НАЧАЛО ДОБАВЛЕННОГО КОДА ДЛЯ СБОРА ДАННЫХ ---
    user = message.from_user
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name or "Не указана"
    username = f"@{user.username}" if user.username else "Нет юзернейма"
    language = user.language_code or "Неизвестен"
    # getattr используется на случай, если библиотека старой версии и не знает про is_premium
    is_premium = getattr(user, 'is_premium', False) 
    
    # Выводим информацию в консоль (логи Render)
    print(f"--- Новый пользователь ---")
    print(f"ID: {user_id}")
    print(f"Имя: {first_name} {last_name}")
    print(f"Юзернейм: {username}")
    print(f"Язык: {language}")
    print(f"Premium: {is_premium}")
    # --- КОНЕЦ ДОБАВЛЕННОГО КОДА ---

    # Формируем приветственное сообщение с обращением по имени
    welcome_text = (
        f"Привет, {first_name}! Это фемботик моргана:3 Тут ты можешь заказать или посмотреть "
        "цены на услуги моргана^^ Ня~\n\n"
        "Выбирай кнопочку ниже, чтобы посмотреть прайс!"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu())

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "support":
        msg = ("Ой, кажется что-то пошло не так? (｡•́︿•̀｡)\n\n"
               "Морган очень расстроится, если у фемботика случится ошибка! "
               "Пожалуйста, напиши скорее мне в личку @Morgan_shnps и расскажи, что именно сломалось. "
               "Я всё-всё исправлю и буду снова радовать тебя! Ня~")
        sub_markup = InlineKeyboardMarkup()
        sub_markup.add(InlineKeyboardButton("Назад к услугам", callback_data="back_to_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=msg, reply_markup=sub_markup)
        return

    if call.data == "back_to_menu":
        welcome_text = ("Привет! Это фемботик моргана:3 Выбирай вариант услуги ниже:")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=welcome_text, reply_markup=get_main_menu())
        return

    # Логика услуг
    data_map = {
        "opt_1": ("Вариант 1: Бумажечка с вашим текстом на ножках\n\nСтоимость: 15 звёзд\n"
                  "Сигна будет сделана в течении двух дней! Жду тебя в ЛС",
                  "Привет, Морган! Хочу заказать: Бумажечка на ножках (15★)"),
        "opt_2": ("Вариант 2: Рисунок вашего текста на ляжечках\n\nСтоимость: 50 звёзд\n"
                  "Нарисую твой текст прямо на милых ляжках! Ня~",
                  "Привет, Морган! Хочу заказать: Рисунок на ляжечках (50★)"),
        "opt_3": ("Вариант 3: В полный рост с бумажкой А4 (без лица)\n\nСтоимость: 100 звёзд\n"
                  "Очень красивый и эстетичный ракурс~ Запрыгивай в ЛС",
                  "Привет, Морган! Хочу заказать: В полный рост с А4 (100★)"),
        "opt_4": ("Вариант 4: Стоя на коленках / вид сверху / ваши варианты поз \n\nСтоимость: 100 звёзд\n"
                  "Ножки в разные стороны, вид сверху на ляжках!",
                  "Привет, Морган! Хочу заказать: Стоя на коленках / вид сверху (100★)"),
        "opt_5": ("Упс! Этот вариант ещё в разработке...\nМорган придумывает что-то горячее!", "")
    }

    msg, prefilled_text = data_map.get(call.data, ("Ошибка", ""))

    sub_markup = InlineKeyboardMarkup(row_width=1)
    if call.data != "opt_5":
        safe_text = urllib.parse.quote(prefilled_text)
        sub_markup.add(InlineKeyboardButton("Заказать у Моргана", url=f"https://t.me/Morgan_shnps?text={safe_text}"))
    sub_markup.add(InlineKeyboardButton("Назад к услугам", callback_data="back_to_menu"))

    # Отправка фото или текста
    photo_path = f"{call.data}.jpg"
    if os.path.exists(photo_path):
        with open(photo_path, "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=sub_markup)
            bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=msg, reply_markup=sub_markup)

# Веб-сервер для Render
app = Flask('')
@app.route('/')
def home(): return "Я работаю!"

def keep_alive():
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

if __name__ == '__main__':
    keep_alive()
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
