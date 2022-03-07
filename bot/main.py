from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pafy

from bot.config import TOKEN
from bot.database import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def get_title_video(url: str):
    vid = pafy.new(url)
    title = vid.title
    return title


def get_author_video(url: str):
    vid = pafy.new(url)
    author = vid.author
    return author


def get_duration_video(url: str):
    vid = pafy.new(url)
    duration = vid.duration
    return duration


def get_list_video(url):
    """Функція,яка створює нову сесію,по url-адресі знаходить відео в ютуб
    і створює словник з доступиними розширеннями відео.
    Повертає словник з розширеннями відео"""
    video = pafy.new(url=url)
    streams = video.streams

    available_streams = {}
    count = 1

    for stream in streams:
        available_streams[count] = stream
        count += 1
    return available_streams


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привіт!Я допоможу тобі скачати відео з ютуб')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply("""Привіт! Ось команди,які я вмію виконувати:\n
    1)/help - Цю команду ти зараз читаєш\n
    2)/start - Команда для запуску бота \n
    3)/search - Введіть після команди url-адресу відео,яке хочете скачти,
    пілся цього через декілька секунд у вас буде список розширень цього відео""")


@dp.message_handler(commands=['search'])
async def search_video(message: types.Message):
    url = message.text.split()[-1]
    title = get_title_video(url=url)
    author = get_author_video(url=url)
    duration = get_duration_video(url=url)
    await message.reply(f'Назва відео - {title}\n'
                        f'Автор - {author}\n'
                        f'Тривалість - {duration}\n'
                        f'Щоб завантажити введіть /download')


@dp.message_handler(commands=['download'])
async def download_video(message: types.Message):
    pass


if __name__ == '__main__':
    executor.start_polling(dp)
