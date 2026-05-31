import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib.parse
import os
import ssl

# 1. Сначала создаем бота (инициализация)
TOKEN = '8971183383:AAF8MsNTIAAd32cvc5sRC2E_ekN6IAeHOsc'
bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()

# 2. Теперь функции
def get_main_menu():
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("Бумажечка на ножках (15★)", callback_data="opt_1")
    btn2 = InlineKeyboardButton("Рисунок на ляжечках (50★)", callback_data="opt_2")
    btn3 = InlineKeyboardButton("В полный рост с листочком А4 (100★)", callback_data="opt_3")
    btn4 = InlineKeyboardButton("Стоя на коленках / вид сверху / ваши варианты поз (100★)", callback_data="opt_4")
    btn5 = InlineKeyboardButton("Приветствие от фембоя (В разработке...)", callback_data="opt_5")
    btn6 = InlineKeyboardButton("Техподдержка", callback_data="support")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6) # И не забудь добавить btn6 в список
    return markup

# 3. Теперь обработчики (декораторы)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Привет! Это фемботик моргана:3 Тут ты можешь заказать или посмотреть "
        "цены на услуги моргана^^ Ня~\n\n"
        "У меня сейчас доступно 4 варианта услуги, а 5-й пока ещё "
        "готовится в разработке... Выбирай кнопочку ниже, чтобы посмотреть прайс!"
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
        welcome_text = (
            "Привет! Это фемботик моргана:3 Тут ты можешь заказать или посмотреть "
            "цены на услуги моргана^^ Ня~\n\n"
            "Выбирай вариант услуги ниже:"
        )
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        bot.send_message(call.message.chat.id, welcome_text, reply_markup=get_main_menu())
        return

    msg = ""
    prefilled_text = ""

    if call.data == "opt_1":
        msg = ("Вариант 1: Бумажечка с вашим текстом на ножках\n\n"
               "Стоимость: 15 звёзд\n"
               "Как заказать: кидать звёзды сюда — @Morgan_shnps")
        prefilled_text = "Привет, Морган! Хочу заказать: Бумажечка на ножках (15★)"
    elif call.data == "opt_2":
        msg = ("Вариант 2: Рисунок вашего текста на ляжечках\n\n"
               "Стоимость: 50 звёзд\n"
               "Как заказать: кидать звёзды сюда — @Morgan_shnps")
        prefilled_text = "Привет, Морган! Хочу заказать: Рисунок на ляжечках (50★)"
    elif call.data == "opt_3":
        msg = ("Вариант 3: В полный рост с бумажкой А4\n\n"
               "Стоимость: 100 звёзд\n"
               "Как заказать: кидать звёзды сюда — @Morgan_shnps")
        prefilled_text = "Привет, Морган! Хочу заказать: В полный рост с А4 (100★)"
    elif call.data == "opt_4":
        msg = ("Вариант 4: Стоя на коленях (вид сверху)\n\n"
               "Стоимость: 100 звёзд\n"
               "Как заказать: кидать звёзды сюда — @Morgan_shnps")
        prefilled_text = "Привет, Морган! Хочу заказать: Стоя на коленках / вид сверху (100★)"
    elif call.data == "opt_5":
        msg = ("Упс! Этот вариант ещё в разработке...")

    sub_markup = InlineKeyboardMarkup(row_width=1)
    if call.data != "opt_5":
        safe_text = urllib.parse.quote(prefilled_text)
        sub_markup.add(InlineKeyboardButton("Заказать у Моргана", url=f"https://t.me/Morgan_shnps?text={safe_text}"))
    sub_markup.add(InlineKeyboardButton("Назад к услугам", callback_data="back_to_menu"))

    photo_path = f"{call.data}.jpg"
    if os.path.exists(photo_path):
        with open(photo_path, "rb") as photo:
            bot.send_photo(call.message.chat.id, photo, caption=msg, reply_markup=sub_markup)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=msg, reply_markup=sub_markup)

# 4. Запуск в самом конце
print("Фемботик успешно запущен!")
if __name__ == '__main__':
    bot.polling(none_stop=True)

    if call.data == "opt_1":
        msg = ("Вариант 1: Бумажечка с вашим текстом на ножках\n\n"
               "Стоимость: 15 звёзд\n"
               "Примеры сигн можно посмотреть выше в чатике\n\n"
               "Как заказать: кидать звёзды сюда — @Morgan_shnps\n"
               "Сигна будет сделана в течении двух дней после заказа! Жду тебя в ЛС")
        prefilled_text = "Привет, Морган! Хочу заказать: Бумажечка на ножках (15★)"
    elif call.data == "opt_2":
        msg = ("Вариант 2: Рисунок вашего текста на ляжечках\n\n"
               "Стоимость: 50 звёзд\n"
               "Примеры сигн выше~ Нарисую твой текст прямо на милых ляжках!\n\n"
               "Как заказать: кидать звёзды сюда — @Morgan_shnps\n"
               "Сигна будет сделана в течении двух дней после заказа! Ня~")
        prefilled_text = "Привет, Морган! Хочу заказать: Рисунок на ляжечках (50★)"
    elif call.data == "opt_3":
        msg = ("Вариант 3: В полный рост с бумажкой А4 (без лица)\n\n"
               "Стоимость: 100 звёзд\n"
               "Примеры сигн выше! Очень красивый и эстетичный ракурс~\n\n"
               "Как заказать: кидать звёзды сюда — @Morgan_shnps\n"
               "Сигна будет сделана в течении двух дней после заказа! Запрыгивай в ЛС")
        prefilled_text = "Привет, Морган! Хочу заказать: В полный рост с А4 (100★)"
    elif call.data == "opt_4":
        msg = ("Вариант 4: Стоя на коленях (вид сверху)\n\n"
               "Стоимость: 100 звёзд\n"
               "Типо сидя, ножки в разные стороны, вид сверху на ляжках!\n"
               "Можно заказать несколько вариантов сигны (только не интимные сигны, ня!)\n\n"
               "Примеры сигн выше~\n\n"
               "Как заказать: кидать звёзды сюда — @Morgan_shnps\n"
               "Сигна будет сделана в течении двух дней после заказа! Жду твой заказик")
        prefilled_text = "Привет, Морган! Хочу заказать: Стоя на коленках / вид сверху (100★)"
    elif call.data == "opt_5":
        msg = ("Упс! Этот вариант ещё в разработке...\n\n"
               "Морган усердно придумывает кое-что очень горячее и милое!\n"
               "Загляни сюда чуточку позже, ладно? Ня~")

    sub_markup = InlineKeyboardMarkup(row_width=1)

    if call.data != "opt_5":
        safe_text = urllib.parse.quote(prefilled_text)
        sub_markup.add(InlineKeyboardButton("Заказать у Моргана", url=f"https://t.me/Morgan_shnps?text={safe_text}"))

    sub_markup.add(InlineKeyboardButton("Назад к услугам", callback_data="back_to_menu"))

    photo_path = f"{call.data}.jpg"
    if os.path.exists(photo_path):
        with open(photo_path, "rb") as photo:
            bot.send_photo(
                call.message.chat.id,
                photo,
                caption=msg,
                reply_markup=sub_markup
            )
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
    else:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=msg,
            reply_markup=sub_markup
        )