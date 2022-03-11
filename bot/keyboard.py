from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

button_help = KeyboardButton('/help')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
greet_kb.add(button_help)

button_start = KeyboardButton('/start')
greet_kb2 = ReplyKeyboardMarkup(resize_keyboard=True).add(button_start)


markup = ReplyKeyboardMarkup()
markup.add(button_start).add(button_help)