import requests
import datetime
from scrap_youtube import Get_end_video
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])  # обработчик команды /start
async def start_command(message: types.Message):  # функция для самой команды
    await message.reply("Привет! Напиши мне название города и я пришлю тебе сводку погоды.")  # вывод текста на команду


@dp.message_handler()  # обработчик всех входящих сообщений, сейчас настроены на погоду
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thundershtorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }  # словарь с погодой и смайликом

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )  # запрос по API на сайт с погодой
        data = r.json()  # читаем выходищий json файл

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно"
            # если типа погоды нет в словаре, выводим сообщение с просьбой посмотреть в окно
            # если есть, то вставляем русскую интерпритацию погоды со смайликом

        humidity = data["main"]["humidity"]
        cur_weather_max = data["main"]["temp_max"]
        cur_weather_min = data["main"]["temp_min"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        # разбираем json файл по нужным ключам

        await bot.send_message(message.from_user.id,
                               f"*** {datetime.datetime.now().strftime('%d - %m - %Y / %H:%M')} ***\n"
                               f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                               f"Относительная влажность: {humidity}%\nСкорость ветра: {wind} м/с.\n"
                               f"Рассвет в: {sunrise_timestamp}\nЗакат в: {sunset_timestamp}\n"
                               f"Продолжительность светового дня: {sunset_timestamp - sunrise_timestamp}"
                               )  # отправляем обычное сообщение с погодой

    except Exception as ex:
        await message.reply("\U00002620 Проверьте название города \U00002620")
        # если введена какая-то дичь, то просим проверить правильнотсь написания города


if __name__ == '__main__':  # запуск бота
    executor.start_polling(dp)
