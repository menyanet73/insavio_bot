import os
import re
import logging
from telebot import TeleBot, types
from scraper import InstaLoader


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(
        message.chat.id,
        "👋 Привет! Я готов помочь посмотреть видосики из инстаграм!")


@bot.message_handler(content_types=['text'])
def get_text_messages(message: types.Message):
    message_text = message.text

    instagram_regex = r"(?:http(?:s)?:\/\/)?(?:www\.)?(?:instagram\.com|instagr\.am)\/([A-Za-z0-9-_]+)"
    match = re.search(instagram_regex, message_text)

    if match:
        try:
            url = match.string
            logger.info(f'Instagram url getted {url}')
            instaloader = InstaLoader(url=url)
            filename = instaloader.download_video()
            logger.info(f'video downloaded')

            with open(file=filename, mode='rb') as file:
                video = file.read()
                bot.send_video(message.chat.id, video=video)
            logger.info(f'video sended')

            os.remove(filename)
            logger.info(f'video deleted')
        except Exception as err:
            logger.error(err)

bot.polling(none_stop=True, interval=0)