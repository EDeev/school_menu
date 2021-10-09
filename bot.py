import logging
import base, pars
import asyncio
import datetime as dt

from aiogram import Bot, Dispatcher, executor, types

# log level
logging.basicConfig(level=logging.INFO)

# bot init
bot = Bot(token=base.TOKEN)
dp = Dispatcher(bot)


# events
@dp.message_handler(commands="today")
async def today(message: types.Message):
    food = pars.eating(0)
    if food:
        eat = f"<b>Питание за {'.'.join(reversed(str(dt.date.today()).split('-')))}</b>\n\n"
        for j in food:
            eat = eat + "<i><b>" + j + ":</b></i>\n"
            for i in food[j]:
                eat = eat + "<b>* " + i[0] + "</b> <i>[ " +\
                      str(int(eval(i[1][0]))) + " г. " + str(i[1][1]) + " ккал. ]</i>" + "\n"
            eat = eat + "\n\n"
        await message.answer(eat, types.ParseMode.HTML)
    else:
        await message.answer(f"<b>Ошибка при выводе данных</b>\n\nВероятнее всего, либо вы вызываете команду в "
                             f"воскресенье, либо же данные о меню отсутствуют", types.ParseMode.HTML)


@dp.message_handler(commands="tomorrow")
async def tomorrow(message: types.Message):
    food = pars.eating(1)
    if food:
        eat = f"<b>Питание за {'.'.join(reversed(str(dt.date.today() + dt.timedelta(days=1)).split('-')))}</b>\n\n"
        for j in food:
            eat = eat + "<i><b>" + j + ":</b></i>\n"
            for i in food[j]:
                eat = eat + "<b>* " + i[0] + "</b> <i>[ " +\
                      str(int(eval(i[1][0]))) + " г. " + str(i[1][1]) + " ккал. ]</i>" + "\n"
            eat = eat + "\n\n"
        await message.answer(eat, types.ParseMode.HTML)
    else:
        await message.answer(f"<b>Ошибка при выводе данных</b>\n\nВероятнее всего, либо вы вызываете команду на "
                             f"воскресенье, либо же данные о меню отсутствуют", types.ParseMode.HTML)


@dp.message_handler(commands="eat")
async def vote(message: types.Message):
    await bot.send_message(chat_id=base.GROUP_ID,
                           text=f'*{message.chat.title}* >> '
                                f'[{message.from_user.first_name}](tg://user?id={message.from_user.id})\n'
                                f'*Заказывет:* {" ".join(message.text.split()[1:])}',
                           parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(commands="help")
async def help(message: types.Message):
    await message.answer('*Инструкция использования:*\n\n'
                         '*/eat {завтрак / обед / полдник}* - с помощью этой команды вы можете заказать питание\n'
                         '*/today* - команда выдающая меню на сегодня\n'
                         '*/tomorrow* - команда выдающая меню на завтра', types.ParseMode.MARKDOWN)


# ОТДЕЛЕНИЕ ДНЯ В ГРУППЕ
async def time(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        hour = dt.datetime.now().hour
        date = dt.datetime.now().day
        wkd = dt.datetime.today().weekday()

        file = open('day.txt', 'r')
        data = file.read()
        file.close()

        if date != int(data) and hour == 10:
            if wkd == 5:
                await bot.send_message(chat_id=base.GROUP_ID,
                                       text=f'<b>Питание на {".".join(reversed(str(dt.date.today() + dt.timedelta(days=2)).split("-")))}</b>',
                                       parse_mode=types.ParseMode.HTML)
            elif wkd != 6:
                await bot.send_message(chat_id=base.GROUP_ID,
                                       text=f'<b>Питание на {".".join(reversed(str(dt.date.today() + dt.timedelta(days=1)).split("-")))}</b>',
                                       parse_mode=types.ParseMode.HTML)

            file = open('day.txt', 'w')
            file.write(str(date))
            file.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(time(60))  # ПРОВЕРКА КАЖДУЮ МИНУТУ
    executor.start_polling(dp, skip_updates=True)
