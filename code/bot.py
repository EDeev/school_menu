import logging, asyncio, random, pymorphy2
import base, pars, sql, os
import datetime as dt

from aiogram import Bot, Dispatcher, executor, types

# log level
logging.basicConfig(level=logging.INFO)
morph = pymorphy2.MorphAnalyzer()

# bot init
bot = Bot(token=base.TOKEN)
dp = Dispatcher(bot)

# create now.db
file = open('../db/now.db', 'w+')
file.close()

# db init
db = sql.Base('../db/base.db')
du = sql.User('../db/users.db')
dg = sql.Group('../db/groups.db')
dn = sql.Now('../db/now.db')


@dp.message_handler(commands="start")
async def start(message: types.Message):
    if 0 < int(message.chat.id):
        await message.answer("Ghdbtn", types.ParseMode.MARKDOWN)


# ОБНОВЛЕНИЕ АЙДИ ГРУППЫ
@dp.message_handler(content_types=['migrate_to_chat_id', 'migrate_from_chat_id'])
async def chat_reload(message: types.Message):
    if du.group_exists(message.migrate_from_chat_id):
        du.update_group_id(message.migrate_from_chat_id, message.migrate_to_chat_id)


# КОМАНДЫ
@dp.message_handler(commands="help")
async def hlp(message: types.Message):
    if 0 < int(message.chat.id):
        await message.answer("*Инструкция использования:*\n\n"
                             "*/eat* - с помощью этой команды вы можете заказать питание\n"
                             "*/today* - команда выдающая меню на сегодня\n"
                             "*/tomorrow* - команда выдающая меню на завтра\n\n"
                             "*/add_group* - команда выдающая меню на завтра\n"
                             "*/del_group* - команда выдающая меню на завтра\n", types.ParseMode.MARKDOWN)
    else:
        await message.answer("*Инструкция использования:*\n\n"
                             "*/eat* - с помощью этой команды вы можете заказать питание\n"
                             "*/today* - команда выдающая меню на сегодня\n"
                             "*/tomorrow* - команда выдающая меню на завтра\n", types.ParseMode.MARKDOWN)


@dp.message_handler(commands="stat")
async def stat(message: types.Message):
    if 0 > int(message.chat.id):
        group_id = message.chat.id
        if du.group_exists(group_id):
            group_id = du.get_group_id(group_id)
            if db.main_group_exists(group_id):
                overall = db.stat_group(group_id)
                all_users = dg.stat_all_users(group_id)

                z = [[user[1], user[0]] for user in all_users if user[1] != 0]
                o = [[user[2], user[0]] for user in all_users if user[2] != 0]
                p = [[user[3], user[0]] for user in all_users if user[3] != 0]

                txt = f"<i><b>Всего было сделано заказов - {sum(overall)}</b></i>\n"
                line = morph.parse('заказ')[0]

                lst = [[f"\n\t<b>* Завтраков - {str(overall[0])}</b>\n", z], [f"\n\t<b>* Обедов - {str(overall[1])}</b>\n", o],
                       [f"\n\t<b>* Полдников - {str(overall[2])}</b>\n", p]]
                for i in lst:
                    txt = txt + i[0]
                    if i[1]:
                        for n, j in enumerate(i[1][:3]):
                            txt = txt + "\t\t\t<b>" + str(n + 1) + ". " + j[1] + "</b> " + str(j[0]) + " " + line.make_agree_with_number(j[0]).word + "\n"

                await message.answer(txt, types.ParseMode.HTML)
            else:
                await message.answer("Ваша группа не зарегистрирована!")
        else:
            await message.answer("Ваша группа не зарегистрирована!")


@dp.message_handler(commands="eat")
async def eat(message: types.Message):
    if 0 > int(message.chat.id):
        keyboard1 = {"inline_keyboard":
                        [[{"text": "Завтрак", "callback_data": "z"}, {"text": "Обед", "callback_data": "o"},
                          {"text": "Полдник", "callback_data": "p"}], [{"text": "Завтрак / Обед", "callback_data": "zo"}],
                         [{"text": "Завтрак / Полдник", "callback_data": "zp"}],
                         [{"text": "Обед / Полдник", "callback_data": "op"}],
                         [{"text": "Завтрак / Обед / Полдник", "callback_data": "zop"}]]}

        await bot.send_message(chat_id=message.chat.id,
                               text='*Это меню выбора притания!* Всё, что вам надо сделать, это лишь выбрать '
                                    'необходимый заказ.\n\nEсли после нажатия бот написал, что вы выбрали, то всё '
                                    'прошло успешно и вы можете не беспокоиться!', parse_mode=types.ParseMode.MARKDOWN,
                               reply_markup=keyboard1)

        keyboard2 = {"inline_keyboard": [[{"text": "Отменить заказ", "callback_data": "cancel"}]]}
        await bot.send_message(chat_id=message.chat.id,
                               text='Если вы хотите сменить заказ, то отмените действующий заказ по кнопке ниже и '
                                    'закажите заново!', parse_mode=types.ParseMode.MARKDOWN,
                               reply_markup=keyboard2)
    else:
        await message.answer("Эта команда доступна к использованию *только в чатах*", types.ParseMode.MARKDOWN)


@dp.message_handler(commands="del_group")
async def delg(message: types.Message):
    if 0 < int(message.chat.id):
        user_id = message.from_user.id
        if du.user_exists(user_id):
            user_id = du.get_user_id(user_id)
            if db.user_main_exists(user_id):
                keyboard = {"inline_keyboard": [[{"text": "Подтвердить удаление", "callback_data": "del"}]]}
                await bot.send_message(chat_id=message.chat.id,
                                       text='Вы точно хотите удалить статистику и связку групп?',
                                       parse_mode=types.ParseMode.MARKDOWN, reply_markup=keyboard)
            else:
                await message.answer("У вас нет связки групп для их удаления!")
        else:
            await message.answer("У вас нет связки групп для их удаления!")
    else:
        await message.answer("Эта команда доступна к использованию *только в личном чате*", types.ParseMode.MARKDOWN)


@dp.message_handler(commands="add_group")
async def addg(message: types.Message):
    if 0 < int(message.chat.id):
        user_id = message.from_user.id
        flag = False

        if not du.user_exists(user_id):
            du.add_user(user_id)

            user_id = du.get_user_id(user_id)
            all_cods = db.all_cods()

            cod1 = random.randint(1000, 9999)
            while cod1 in all_cods[0]:
                cod1 = random.randint(1000, 9999)

            cod2 = random.randint(1000, 9999)
            while cod2 in all_cods[1]:
                cod2 = random.randint(1000, 9999)

            db.add_user_tranzit(user_id, cod1, cod2)
            await message.answer(f"Введите этот код в группе с учениками - *{str(cod1)}*, а этот в личной для "
                                 f"фиксации заказа - *{str(cod2)}*", types.ParseMode.MARKDOWN)
            flag = True
        else:
            user_id = du.get_user_id(user_id)
            if db.user_tranzit_exists(user_id):
                cods = db.get_cods(user_id)
                await message.answer(f"Введите этот код в основной группе с учениками - *{str(cods[0])}*, а этот в "
                                     f"личной для фиксации заказа - *{str(cods[1])}*", types.ParseMode.MARKDOWN)
                flag = True
            else:
                if not db.user_main_exists(user_id):
                    all_cods = db.all_cods()

                    cod1 = random.randint(1000, 9999)
                    while cod1 in all_cods[0]:
                        cod1 = random.randint(1000, 9999)

                    cod2 = random.randint(1000, 9999)
                    while cod2 in all_cods[1]:
                        cod2 = random.randint(1000, 9999)

                    db.add_user_tranzit(user_id, cod1, cod2)
                    await message.answer(f"Введите этот код в группе с учениками - *{str(cod1)}*, а этот в личной для "
                                         f"фиксации заказа - *{str(cod2)}*", types.ParseMode.MARKDOWN)
                    flag = True
                else:
                    await message.answer("У вас уже есть связка группы, вам надо её удалить, прежде чем верифицировать "
                                         "новую!", types.ParseMode.MARKDOWN)

        if flag:
            keyboard = {"inline_keyboard": [[{"text": "Отменить верификацию", "callback_data": "cnl"}]]}
            await bot.send_message(chat_id=message.chat.id,
                                   text='*Вы можете отменить заявку* если не хотите связывать группы для сбора '
                                        'заказов питания!', parse_mode=types.ParseMode.MARKDOWN, reply_markup=keyboard)
    else:
        await message.answer("Эта команда доступна к использованию *только в личном чате*", types.ParseMode.MARKDOWN)


@dp.message_handler(commands=["today", "tomorrow"])
async def todtom(message: types.Message):
    food = pars.eating(0 if "today" in message.text else 1)
    if food[0]:
        food = food[1]

        if "today" in message.text:
            et = f"<b>Питание за {'.'.join(reversed(str(dt.date.today()).split('-')))}</b>\n\n"
        else:
            et = f"<b>Питание за {'.'.join(reversed(str(dt.date.today() + dt.timedelta(days=1)).split('-')))}</b>\n\n"

        for j in food:
            et = et + "<i><b>" + str(j) + ":</b></i>\n"
            for i in food[j]:
                et = et + "<b>* " + str(i[0]) + "</b> <i>[ "
                et = et + str(i[1][0]) + " г. " + str(i[1][1]) + " ккал. ]</i>" + "\n"
            et = et + "\n\n"

        await message.answer(et, types.ParseMode.HTML)
    else:
        if food[1]:
            await message.answer(f"<b>Ошибка в системе бота!</b>\n\nОна будет в скором времени исправлена...",
                                 types.ParseMode.HTML)
            await bot.send_message(chat_id=base.TEX_GROUP, text=f"<b>[ {str(dt.datetime.now())[:-10]} ]</b> "
                                                                f"<b><i>=></i></b> <i>{food[3]}</i> (ошибка в системе)",
                                   parse_mode=types.ParseMode.HTML)
        else:
            if food[2] != 6:
                await message.answer(f"<b>Нет данных по питанию!</b>\n\nКак только данные появятся вы сможете "
                                     f"их получить этой же командой!", types.ParseMode.HTML)
                await bot.send_message(chat_id=base.TEX_GROUP, text=f"<b>[ {str(dt.datetime.now())[:-10]} ]</b> "
                                                                    f"<b><i>=></i></b> <i>{food[3]}</i> (нет данных по "
                                                                    f"питанию)", parse_mode=types.ParseMode.HTML)
            else:
                await message.answer(f"<b>Вы вызывете команду в воскресенье!</b>\n\nНа что вы надеетесь?",
                                     types.ParseMode.HTML)


# ИЛАЙН КЛАВИАТУРА
@dp.callback_query_handler(text=["z", "o", "p", "zo", "zp", "op", "zop"])
async def var(call: types.CallbackQuery):
    et = {"z": "завтрак", "o": "обед", "p": "полдник", "zo": "завтрак / обед", "zp": "завтрак / полдник",
          "op": "обед / полдник", "zop": "завтрак / обед / полдник"}

    group_id = call.message.chat.id
    if du.group_exists(group_id):
        group_id = du.get_group_id(group_id)
        if db.main_group_exists(group_id):
            user_id = call.from_user.id
            if du.user_exists(user_id):
                user_id = du.get_user_id(user_id)
            else:
                du.add_user(user_id)
                user_id = du.get_user_id(user_id)

            if db.check_group_inproc(group_id):
                if not dn.check_user(group_id, user_id):
                    flag = True
                else:
                    await call.message.answer(f"{call.from_user.first_name}, вы уже сделали заказ! Отмените его с "
                                              f"помощью кнопки отмены!")
                    flag = False
            else:
                dn.created_group(group_id)
                db.add_group(group_id)
                flag = True

            if flag:
                for i in str(call.data):
                    db.upd_stat_group(group_id, i, 1)
                    dg.upd_stat_user(group_id, user_id, i, 1)

                ids = db.get_spec_group(group_id)
                msg1 = await bot.send_message(chat_id=str(du.get_first_group_id(ids)),
                                              text=f'[{call.from_user.first_name}](tg://user?id={call.from_user.id}) >> '
                                                   f'*{et[call.data].title()}*', parse_mode=types.ParseMode.MARKDOWN)

                msg2 = await call.message.answer(text=f'{call.from_user.first_name}, всё принято, вы заказили - '
                                                      f'*{"и".join(et[call.data].split("/"))}*',
                                                 parse_mode=types.ParseMode.MARKDOWN)

                dn.add_user(group_id, user_id, msg2.message_id, msg1.message_id, str(call.data))
        else:
            await call.message.answer('Вы должны через личные сообщения зарегистрировать этот чат у бота вместе с '
                                      'дополнительным для отправки списка!')
    else:
        await call.message.answer('Вы должны через личные сообщения зарегистрировать этот чат у бота вместе с '
                                  'дополнительным для отправки списка!')


@dp.callback_query_handler(text=["cnl"])
async def cnl(call: types.CallbackQuery):
    user_id = du.get_user_id(call.from_user.id)
    if db.user_tranzit_exists(user_id):
        db.delete_tranzit(user_id)
        await call.message.answer('<b>Заявка удалена!</b> Если ещё захотите связать группы, то зановой вызовите '
                                  'команду <b>/add_group</b>', types.ParseMode.HTML)
    else:
        await call.message.answer('У вас нет оставленных заявок!')


@dp.callback_query_handler(text=["del"])
async def ver_del(call: types.CallbackQuery):
    user_id = du.get_user_id(call.from_user.id)
    if db.user_main_exists(user_id):
        ids = db.get_main_group(user_id)
        db.delete_main_group(user_id)
        dg.delete_group(str(ids))
        db.del_group(str(ids))
        await call.message.answer('Всё успешно удалено!')
    else:
        await call.message.answer("У вас нет связки групп для их удаления!")


@dp.callback_query_handler(text=["cancel"])
async def cancel(call: types.CallbackQuery):
    group_id = call.message.chat.id
    if du.group_exists(group_id):
        main_group_id = group_id
        group_id = du.get_group_id(group_id)
        if db.main_group_exists(group_id):
            user_id = call.from_user.id
            if du.user_exists(user_id):
                user_id = du.get_user_id(user_id)
            else:
                du.add_user(user_id)
                user_id = du.get_user_id(user_id)

            if db.check_group_inproc(group_id):
                if dn.check_user(group_id, user_id):
                    ord_id = dn.get_ord_id(group_id, user_id)

                    for i in ord_id:
                        db.upd_stat_group(group_id, i, -1)
                        dg.upd_stat_user(group_id, user_id, i, -1)

                    ids = db.get_spec_group(group_id)
                    set_group_id = str(du.get_first_group_id(ids))

                    main, sett = dn.get_message(group_id, user_id)
                    await bot.delete_message(chat_id=main_group_id, message_id=main)
                    await bot.delete_message(chat_id=set_group_id, message_id=sett)

                    dn.del_user(group_id, user_id)
                    await call.message.answer(f"{call.from_user.first_name}, ваш заказ отменён!")
                else:
                    await call.message.answer(f"{call.from_user.first_name}, у вас нет заказа!")
            else:
                await call.message.answer(f"{call.from_user.first_name}, у вас нет заказа!")
        else:
            await call.message.answer('Вы ещё не можете использовать бота, завершите процедуру регистрации!')
    else:
        await call.message.answer('Вы должны через личные сообщения зарегистрировать этот чат у бота вместе с '
                                  'дополнительным для отправки списка!')


# ТРЕКЕР НОВЫХ ПОЛЬЗОВАТЕЛЕЙ
@dp.message_handler(content_types=["text", "audio", "document", "photo", "sticker", "video",
                                   "video_note", "voice", "location", "contact"])
async def check(message: types.Message):
    if 0 > int(message.chat.id):
        if du.user_exists(message.from_user.id):
            user_id = du.get_user_id(message.from_user.id)
            if db.user_tranzit_exists(user_id) and len(message.text) == 4:
                cods = db.get_cods(user_id)

                flag = False

                if not du.group_exists(message.chat.id):
                    if message.text == str(cods[0]):
                        du.add_group(message.chat.id)
                        group_id = du.get_group_id(message.chat.id)
                        db.add_main_group(user_id, group_id)
                        flag = True
                    elif message.text == str(cods[1]):
                        du.add_group(message.chat.id)
                        group_id = du.get_group_id(message.chat.id)
                        db.add_set_group(user_id, group_id)
                        flag = True
                else:
                    group_id = du.get_group_id(message.chat.id)
                    if not db.main_group_exists(group_id):
                        if message.text == str(cods[0]):
                            db.add_main_group(user_id, group_id)
                            flag = True
                        elif message.text == str(cods[1]):
                            db.add_set_group(user_id, group_id)
                            flag = True

                if flag and db.user_tranzit(user_id):
                    ids = db.get_groups_ids(user_id)
                    db.add_active_groups(user_id, ids[0], ids[1])
                    db.delete_tranzit(user_id)
                    dg.created_group(ids[0])
                    dg.add_user(ids[0], user_id, message.from_user.first_name)
            else:
                if du.group_exists(message.chat.id):
                    group_id = du.get_group_id(message.chat.id)
                    if db.main_group_exists(group_id):
                        dg.update_name(user_id, message.from_user.first_name, group_id)
        else:
            if du.group_exists(message.chat.id):
                group_id = du.get_group_id(message.chat.id)
                if db.main_group_exists(group_id):
                    du.add_user(message.from_user.id)
                    user_id = du.get_user_id(message.from_user.id)
                    dg.add_user(group_id, user_id, message.from_user.first_name)


# ОТДЕЛЕНИЕ ДНЯ В ГРУППЕ
async def time(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        hour = dt.datetime.now().hour
        date = dt.datetime.now().day
        wkd = dt.datetime.today().weekday()

        data = db.get_day()

        if date != data and hour == 6:
            for ids in db.get_spec_groups():
                group = du.get_first_group_id(ids[0])

                if wkd == 5:
                    dat = ".".join(reversed(str(dt.date.today() + dt.timedelta(days=2)).split("-")))
                    await bot.send_message(chat_id=group, text=f'<b>Питание на {dat}</b>',
                                           parse_mode=types.ParseMode.HTML)
                elif wkd != 6:
                    dat = ".".join(reversed(str(dt.date.today() + dt.timedelta(days=1)).split("-")))
                    await bot.send_message(chat_id=group, text=f'<b>Питание на {dat}</b>',
                                           parse_mode=types.ParseMode.HTML)

            db.update_day(date)
            db.reset_proc()

            os.remove('../db/now.db')
            fle = open('../db/now.db', 'w+')
            fle.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(time(600))  # ПРОВЕРКА КАЖДЫЕ 10 МИНУТ
    executor.start_polling(dp, skip_updates=True)
