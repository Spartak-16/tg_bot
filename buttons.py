from pyrogram.types import KeyboardButton, InlineKeyboardButton
from pyrogram import emoji

# Общие кнопки:
back_button = KeyboardButton(f"{emoji.BACK_ARROW} Назад")

# Кнопки главного меню
time_button = KeyboardButton(f"{emoji.ALARM_CLOCK} Время")
help_button = KeyboardButton(f"{emoji.WHITE_QUESTION_MARK} Помощь")
settings_button = KeyboardButton(f"{emoji.GEAR} Настройки")
weather_button = KeyboardButton(f"{emoji.SUN} Погода")
forecast_button = KeyboardButton(f"{emoji.CALENDAR} Прогноз погоды")





weather_current_inline_button = InlineKeyboardButton(f"{emoji.FIVE_O_CLOCK} Погода сейчас",
                                                     "weacher_current")
weather_forecast_inline_button = InlineKeyboardButton(f"{emoji.CALENDAR} Прогноз погоды",
                                                     "weacher_forecast")