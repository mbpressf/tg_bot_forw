import telebot
from telebot import types
import json

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

    user_json = {
        "user" : {
            "user_id" : user_id,
            "message_id" : message.id,
            "statys" : None
        }
    }
    with open('data.json', 'w+') as f:
        json.dump(user_json, f, indent=4)

# Обработчик фотографий
# Обработчик фотографий и текста
# @bot.message_handler(content_types=['photo', 'text'])
# def forward_message(message):
#     pass





if __name__ == '__main__':
    bot.polling(none_stop=True)