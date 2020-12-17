from bot import bot
from messages import HELLO_MESSAGE
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import random
import os
import io


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, HELLO_MESSAGE)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


@bot.message_handler(content_types=['photo'])
def handle_docs_document(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    chat_id = message.chat.id
    downloaded_file = bot.download_file(file_info.file_path)
    photo_to_change = io.BytesIO(downloaded_file)
    img = Image.open(photo_to_change)
    (width, height) = img.size
    drawing = ImageDraw.Draw(img)
    random_phrase = random.choice(list(open('lyrics/meat.txt', encoding="utf8")))
    bot.send_message(chat_id, random_phrase)
    number_of_symbols = len(random_phrase)
    font = ImageFont.truetype('font.Ttf', int((width / number_of_symbols) * 1.8))
    font_color = (255, 255, 255)
    shadow_color = (0, 0, 0)
    x, y = (width / 20, height / 1.3)
    drawing.text((x - 1, y - 1), random_phrase, font=font, fill=shadow_color)
    drawing.text((x + 1, y - 1), random_phrase, font=font, fill=shadow_color)
    drawing.text((x - 1, y + 1), random_phrase, font=font, fill=shadow_color)
    drawing.text((x + 1, y + 1), random_phrase, font=font, fill=shadow_color)
    drawing.text((x, y), random_phrase, font=font, fill=font_color)
    bot.send_photo(chat_id, photo=img)


if __name__ == '__main__':
    bot.polling(none_stop=True)
