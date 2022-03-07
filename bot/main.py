from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import pafy

from bot.config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def get_list_video(url):
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
    2)/start - Команда для запуску бота""")


@dp.message_handler(commands=['search'])
async def search_video(message: types.Message):
    url = message.text.split()[-1]
    dict_streams = get_list_video(url=url)
    list_streams = []
    for i in dict_streams.values():
        list_streams.append(i)
    first_one = list_streams.pop(0)
    await message.reply(message.from_user.id, first_one)


if __name__ == '__main__':
    executor.start_polling(dp)
