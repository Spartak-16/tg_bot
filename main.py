import random
import time
import operator


from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

import config
import buttons
import keyboards
from custom_filters import button_filter, inline_button_filters
from weather import get_current_weather, get_forecast
from database import Database

class Client(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.database = Database()

    def stop(self, *args, **kwargs):
        self.database.close()
        return super().stop(*args, **kwargs)


bot = Client(
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    name="my_bot"
)

@bot.on_message(filters=filters.command("start") | button_filter(buttons.back_button))
async def start_command(client: Client, message: Message):
    user = client.database.get_user(message.from_user.id)
    print(user.__dict__ if user else None)
    if user is None:
        client.database.create_user(message.from_user.id)

    await message.reply(f"Привет, {message.from_user.username}! Я бот, который умеет считать и показывать время.\n"
                        f"Нажми на кнопку {buttons.help_button.text} для получения списка команд.",
    reply_markup=keyboards.main_keyboard
    )

@bot.on_message(filters=filters.command("time") | button_filter(buttons.time_button))
async def time_command(client: Client, message: Message):
    current_time = time.strftime("%H:%M:%S")
    await message.reply(current_time, reply_markup=keyboards.main_keyboard)


@bot.on_message(filters=filters.command("calc"))
async def calc_command(client: Client, message: Message):
    ops = {
        "+": operator.add, "-": operator.sub,
        "*": operator.mul, "/": operator.truediv,
    }
    if len(message.command) != 4:
        return await message.reply(
            "Неверное количество аргументов\n"
            "Пример использования:\n"
            "/calc 1 + 2\n"
        )
    _, left, op, right = message.command
    op = ops.get(op)
    if op is None:
        return await message.reply("Неизвестный оператор")
    if not left.isnumeric or not right.isnumeric():
        return await message.reply("Аргументы должны быть числами")
    left, right = float(left), float(right)
    await message.reply(f"Результат: {op(left, right)}")


@bot.on_message(filters=filters.command("help") | button_filter(buttons.help_button))
async def help_command(client: Client, message: Message):
    commands = await client.get_bot_commands()
    text_commands = "Список доступных команд: \n\n"
    for command in commands:
        text_commands += f"/{command.command}: {command.description}\n"
    await message.reply(text_commands, reply_markup=keyboards.main_keyboard)

@bot.on_message(filters=filters.command("weather") | button_filter(buttons.weather_button))
async def weather_command(client: Client, message: Message):
    if message.command and len(message.command) > 1:
        city = message.command[1]
    else:
        city = "Москва"
    weather = get_current_weather(city)
    await message.reply(weather, reply_markup=keyboards.weather_inline_keyboard)

@bot.on_message(filters=filters.command("forecast") | button_filter(buttons.forecast_button))
async def forecast_command(client: Client, message: Message):
    if message.command and len(message.command) > 1:
        city = message.command[1]
    else:
        city = "Москва"
    forecast = get_forecast(city)
    await message.reply(forecast, reply_markup=keyboards.weather_inline_keyboard)

@bot.on_callback_query(filters=inline_button_filters(buttons.weather_current_inline_button))
async def weather_current_inline_button_callback(client: Client, query: CallbackQuery):
    city = "Москва"
    weather = get_current_weather(city)
    if weather == query.message.text:
        return
    await query.message.edit_text(weather, reply_markup=keyboards.weather_inline_keyboard)

@bot.on_callback_query(filters=inline_button_filters(buttons.weather_forecast_inline_button))
async def weather_forecast_inline_button_callback(client: Client, query: CallbackQuery):
    city = "Москва"
    weather = get_forecast(city)
    if weather == query.message.text:
        return
    await query.message.edit_text(weather, reply_markup=keyboards.weather_inline_keyboard)

@bot.on_message()
async def echo(client: Client, message: Message):
    choice = random.randint(0, 1)
    if choice == 0:
        await message.reply(message.text)
    else:
        await message.reply(message.text[::-1])


bot.run()