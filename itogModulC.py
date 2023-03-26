import telebot
from extensions import APIException, CryptoConverter
from config import keys, TOKEN
import traceback

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в следующем формате:\n<имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\nУвидеть список всех доступных валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Слишком много параметров ввода')

        new_base = CryptoConverter.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        traceback.print_tb((e.__traceback__))
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        bot.reply_to(message, new_base)


bot.polling()
