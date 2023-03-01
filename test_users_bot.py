import json
from secrets import token_urlsafe

from faker import Faker
from telebot import TeleBot, types


TOKEN = '6145366549:AAEvju55Xh2Wzgpn2ZyuUSvsMF9PTa9AM4A'
bot = TeleBot(TOKEN, parse_mode='html')

faker = Faker('ru_RU')

# объект клавиатуры
main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="1️⃣"), types.KeyboardButton(text="2️⃣")
)
# второй ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="5️⃣"), types.KeyboardButton(text="🔟")
)
 # третий ряд кнопок   
main_menu_reply_markup.row(
    types.KeyboardButton(text="Жми, если все получилось!👍")
)

# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def welcome(message):
    sti=open('welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(message.chat.id, "Привет,{0.first_name}!😉\nНе хватает тестовых данных? Тогда тебе сюда."\
        "Выбери сколько пользователей тебе нужно 👇🏻".format(message.from_user, bot.get_me()),
        parse_mode='html', reply_markup=main_menu_reply_markup)

# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    
    payload_len = 0
    if message.text == "1️⃣":
        payload_len = 1
    elif message.text == "2️⃣":
        payload_len = 2
    elif message.text == "5️⃣":
        payload_len = 5
    elif message.text == "🔟":
        payload_len = 10
    elif message.text == "Жми, если все получилось!👍":
        sti=open('final.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(
        chat_id=message.chat.id,
        text="Если нужны еще данные, можешь выбрать еще раз 👇🏻",
        reply_markup=main_menu_reply_markup
        )
        return
    else:
        bot.send_message(chat_id=message.chat.id, text="Не понимаю тебя :(")
        return

    # генерируем тестовые данные для выбранного количества пользователей
    # при помощи метода simple_profile
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+7{faker.msisdn()[3:]}'
        # при помощи библиотеки secrets генерируем пароль
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    # сериализуем данные в строку
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str
    )

    # отправляем результат
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Данные {payload_len} тестовых пользователей:\n<code>"\
        f"{payload_str}</code>"
    )

    bot.send_message(
        chat_id=message.chat.id,
        text="Если нужны еще данные, можешь выбрать еще раз 👇🏻",
        reply_markup=main_menu_reply_markup
    )
    

# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
