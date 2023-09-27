import telebot
from telebot import types

# Вставьте ваш токен бота сюда
BOT_TOKEN = '1970038095:AAHNMn8OI76c9r2Fd1lmoutD41VNxyf_98A'

# ID пользователя, на которого будут пересылаться фотографии
TARGET_USER_ID = '6431923675'

CHANNEL_ID = '-1001637096422'
# Инициализируем бота
bot = telebot.TeleBot(BOT_TOKEN)


text = ''' 
Привет ✌️ \n❗️Когда вы отправляете объявления на публикацию, пожалуйста придерживайтесь нескольких правил:
✅ Описание
✅ Цена
✅ Контакты для связи покупателя и продавца (тел. номер, ник в тг)
✅ Фото

✅ *Так же, если у Вас его фото, то текст должен быть вложен в фото, иначе у Вас будет ошибка и мы не примим объявление.*

_Если у Вас больше 3 товаров, то это реклама. Объявление это отслеживают._
                  
📌По поводу рекламы обращаться к @smokeee0.
✅Условия и цены так же в ЛС.
'''


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    bot.send_message(user_id, text=text, parse_mode='Markdown')
    bot.send_message(user_id, "Слудующее сообщение будет отправлено. \nЗа попытку спама, Вы будете забанены навсегда.")

# Обработчик фотографий
# Обработчик фотографий и текста
@bot.message_handler(content_types=['photo', 'text'])
def forward_message(message):
    user_id = message.from_user.id

    if message.content_type == 'photo':
        caption = message.caption

        if caption is None or caption.strip() == "":
            bot.send_message(user_id, "Ошибка: к фотографии должна быть приложена подпись.")
        else:
            # Отправляем фотографию с встроенной клавиатурой "Принять" и "Отклонить"
            markup = types.InlineKeyboardMarkup()
            accept_button = types.InlineKeyboardButton("Принять", callback_data=f"accept_{message.message_id}")
            reject_button = types.InlineKeyboardButton("Отклонить", callback_data=f"reject_{message.message_id}")
            markup.add(accept_button, reject_button)

            bot.send_photo(TARGET_USER_ID, message.photo[-1].file_id, reply_markup=markup)
    
    elif message.content_type == 'text':
        text = message.text

        if text:
            # Отправляем текст с встроенной клавиатурой "Принять" и "Отклонить"
            markup = types.InlineKeyboardMarkup()
            accept_button = types.InlineKeyboardButton("Принять", callback_data=f"accept_{message.message_id}")
            reject_button = types.InlineKeyboardButton("Отклонить", callback_data=f"reject_{message.message_id}")
            markup.add(accept_button, reject_button)

            bot.send_message(TARGET_USER_ID, text, reply_markup=markup)

# Обработчик инлайн-кнопок
@bot.callback_query_handler(lambda query: query.data.startswith(('accept_', 'reject_')))
def handle_inline_buttons(query):
    user_id = query.from_user.id

    print(user_id)

    if query.data.startswith('accept_'):
        # Если нажата кнопка "Принять", отправляем уведомление о принятии в канал
        bot.forward_message(TARGET_USER_ID, CHANNEL_ID, )
        bot.answer_callback_query(query.id, "Вы успешно приняли объявление!")

    elif query.data.startswith('reject_'):
        # Если нажата кнопка "Отклонить", отправляем уведомление о отклонении пользователю
        bot.send_message(user_id, "Извините, ваше объявление было отклонено.")
        bot.answer_callback_query(query.id, "Вы отклонили объявление.")

# Ожидание входящих сообщений
if __name__ == '__main__':
    bot.polling(none_stop=True)