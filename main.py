import telebot
import requests

CUTTLY_API_KEY = 'my key is secret'

bot = telebot.TeleBot("my telegram bot api is secret too")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Я бот для скорочення посилань. Надішліть посилання для скорочення")


@bot.message_handler(func=lambda message: True)
def shorten_link(message):
    try:
        original_link = message.text

        response = requests.get('https://cutt.ly/api/api.php',
                                params={'key': CUTTLY_API_KEY, 'short': original_link})
        data = response.json()
        if data["url"]["status"] == 7:
            shortened_link = data["url"]["shortLink"]
            bot.reply_to(message, f"Скорочене посилання: {shortened_link}")
        else:
            bot.reply_to(message, "Не вдалося скоротити посилання. Спробуйте ще раз.")
    except Exception as e:
        bot.reply_to(message, f"Виникла помилка: {e}")


bot.polling()
