from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode
from aiogram.utils.emoji import emojize
import pafy
import pyshorteners
from os import getenv

from bot.keyboard import markup

bot_token = getenv('BOT_TOKEN')
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
urls = ' '


def get_title_video(url: str) -> str:
    """Функція,яка повертає назву відео з YouTube
    На вхід отримує посилання на відео з YouTube,повертає назву цього відео"""
    vid = pafy.new(url)
    title = vid.title
    return title


def get_author_video(url: str) -> str:
    """Функція,яка визначає автора відео на YouTube через посилання на нього
    На вхід отримує посилання на відео,повертає автора цього відео"""
    vid = pafy.new(url)
    author = vid.author
    return author


def get_duration_video(url: str) -> str:
    """Функція,яка визначає тривалість відео
    На вхід отримує посилання на відео,повертає його тривалість у форматі HH:MM:SS"""
    vid = pafy.new(url)
    duration = vid.duration
    return duration


def get_download_video(url: str):
    """Функція,яка надає посилання для скачування відео з YouTube
    На вхід отримує посилання відео,повертає посилання на його скачування"""
    video = pafy.new(url=url)
    best_video = video.getbest()
    return best_video.url_https


def get_download_audio(url: str):
    """Функція для скачування аудіо із YouTube-відео
    На вхід отримує посилання на відео,повертає посилання на скачування аудіо з YouTube"""
    audio = pafy.new(url=url)
    best_audio = audio.getbestaudio()
    return best_audio.url_https


def short_link(link: str) -> str:
    """Функція для скорочування посилань на скачування відео
    Отримує посилання на скачування,повертає його скаорочену версію"""
    s = pyshorteners.Shortener().tinyurl.short(link)
    return s


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply('Привіт!Я допоможу тобі скачати відео з ютуб', reply_markup=markup)


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    msg = emojize("""":wave:Привіт! Ось команди,які я вмію виконувати:
    1)/help - Цю команду ти зараз читаєш\n
    2)/start - Команда для запуску бота \n
    3)/search - Після команди через пробіл введіть посилання 
    на відео у форматі "youtube.com/..." для отримання інформації 
      про відео і підтвердження скачування\n
    4)/download - Якщо ця команда вводиться після команди 
      search,то url можна не вказувати після неї,
      якщо ж вводиться сама по собі,тоді потрібно після команди 
      вставити url-адресу відео.Після цього буде отримане 
      посилання на скачування відео\n
    5)/audio - Команда для скачування аудіо із відео""")
    await message.reply(msg, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)


@dp.message_handler(commands=['search'])
async def search_video(message: types.Message):
    try:
        global urls
        urls = message.text.split()[-1]
        title = get_title_video(url=urls)
        author = get_author_video(url=urls)
        duration = get_duration_video(url=urls)
        await message.reply(f'Назва відео - {title}\n'
                            f'Автор - {author}\n'
                            f'Тривалість - {duration}\n'
                            f'Щоб завантажити введіть /download')
    except ValueError:
        await message.reply('Перевірте посилання')


@dp.message_handler(commands=['download'])
async def download_video(message: types.Message):
    try:
        link = message.text.split()[-1]
        if link:
            https = get_download_video(url=link)
            short_https = short_link(https)
            await message.reply(f'Посилання на скачування відео - {short_https}')
        else:
            global urls
            https = get_download_video(url=urls)
            short_http = short_link(https)
            await message.reply(f'Посилання на скачування відео - {short_http}')
    except ValueError:
        await message.reply('Перевірте посилання')


@dp.message_handler(commands=['audio'])
async def download_audio(message: types.Message):
    try:
        link = message.text.split()[-1]
        if link:
            https = get_download_audio(url=link)
            short_https = short_link(https)
            await message.reply(f'Посилання на скачування аудіо - {short_https}')
        else:
            global urls
            https = get_download_audio(url=urls)
            short_https = short_link(https)
            await message.reply(f'Посилання на скачування аудіо - {short_https}')
    except ValueError:
        await message.reply('Перевірте посилання на відео')

if __name__ == '__main__':
     executor.start_polling(dp)