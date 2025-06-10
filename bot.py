import os
from dotenv import load_dotenv
load_dotenv()

import telebot

from utils import get_daily_horoscope

BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Halo, Bagaimana kabarnya?\nKetik /help untuk melihat daftar perintah yang tersedia.")


@bot.message_handler(commands=['horoscope'])
def sign_handler(message):
    text = "Zodiak kamu apa?\nChoose one: *Aries*, *Taurus*, *Gemini*, *Cancer,* *Leo*, *Virgo*, *Libra*, *Scorpio*, *Sagittarius*, *Capricorn*, *Aquarius*, and *Pisces*."
    sent_msg = bot.send_message(message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(sent_msg, day_handler)

@bot.message_handler(commands=['help'])
def help_handler(message):
    help_text = """
        *Commands yang Tersedia:*
        /start - Memulai percakapan
        /hello - Sapa pengguna
        /horoscope - Dapatkan ramalan zodiak harian
            
        *Petunjuk penggunaan:*
        1. Kirim /horoscope
        2. Ketik zodiak kamu
        3. Pilih untuk kapan? (TODAY/TOMORROW/YESTERDAY atau YYYY-MM-DD)

        *Available Zodiac Signs:*
        Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces
        """
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")
    
def day_handler(message):
    sign = message.text
    text = "Hari kapan untuk mau taunya?\nChoose one: *TODAY*, *TOMORROW*, *YESTERDAY*, atau tanggal dalam format YYYY-MM-DD."
    sent_msg = bot.send_message(
        message.chat.id, text, parse_mode="Markdown")
    bot.register_next_step_handler(
        sent_msg, fetch_horoscope, sign.capitalize())


def fetch_horoscope(message, sign):
    day = message.text
    horoscope = get_daily_horoscope(sign, day)
    data = horoscope["data"]
    horoscope_message = f'*Horoscope:* {data["horoscope_data"]}\n*Sign:* {sign}\n*Day:* {data["date"]}'
    bot.send_message(message.chat.id, "Berikut adalah ramalannya!")
    bot.send_message(message.chat.id, horoscope_message, parse_mode="Markdown")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()