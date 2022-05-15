import sqlite3


class Base:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    # ДЕНЬ
    def get_day(self):
        """Получаем день"""
        with self.connection:
            return self.cursor.execute(f'SELECT `day` FROM `day`').fetchone()[0]

    def update_day(self, day):
        """Обновляем день"""
        with self.connection:
            return self.cursor.execute("UPDATE `day` SET `day` = ?", (day,))

    # ТРАНЗИТ
    def user_tranzit_exists(self, user_id):
        """Проверяем, есть ли уже пользователь в базе"""
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM `tranz` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user_tranzit(self, user_id, main, sett):
        """Добавляем нового пользователя в транзит"""
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `tranz` (`user_id`, `main_group_cod`, `main_group`, "
                                       f"`set_group_cod`, `set_group`) VALUES(?,?,?,?,?)",
                                       (str(user_id), str(main), None, str(sett), None))

    def add_main_group(self, user_id, group_id):
        """Добавляем главную группу"""
        with self.connection:
            return self.cursor.execute("UPDATE `tranz` SET `main_group` = ? WHERE `user_id` = ?", (group_id, user_id))

    def add_set_group(self, user_id, group_id):
        """Добавляем дополнительную группу"""
        with self.connection:
            return self.cursor.execute("UPDATE `tranz` SET `set_group` = ? WHERE `user_id` = ?", (group_id, user_id))

    def all_cods(self):
        """Список всех выданных кодов"""
        with self.connection:
            main = [i[0] for i in self.cursor.execute(f'SELECT main_group_cod FROM `tranz`').fetchall()]
            sett = [i[0] for i in self.cursor.execute(f'SELECT set_group_cod FROM `tranz`').fetchall()]
            return [main, sett]

    def get_cods(self, user_id):
        """Выданные коды"""
        with self.connection:
            main = self.cursor.execute(f'SELECT main_group_cod FROM `tranz` WHERE `user_id` = ?',
                                       (user_id,)).fetchone()[0]
            sett = self.cursor.execute(f'SELECT set_group_cod FROM `tranz` WHERE `user_id` = ?',
                                       (user_id,)).fetchone()[0]
            return [main, sett]

    def user_tranzit(self, user_id):
        """Проверка на заполненость"""
        with self.connection:
            result = self.cursor.execute(f'SELECT `main_group`, `set_group` FROM `tranz` WHERE `user_id` = ?',
                                         (user_id,)).fetchone()
            return None not in result

    def get_groups_ids(self, user_id):
        """Получение айди групп"""
        with self.connection:
            return self.cursor.execute(f'SELECT `main_group`, `set_group` FROM `tranz` WHERE `user_id` = ?',
                                       (user_id,)).fetchone()

    def delete_tranzit(self, user_id):
        """Удаление ненужного транзита"""
        with self.connection:
            return self.cursor.execute(f'DELETE FROM `tranz` WHERE `user_id` = ?', (user_id,))

    # ОСНОВНА
    def add_active_groups(self, user_id, main, sett):
        """Добавляем нового пользователя из транзита"""
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `main` (`user_id`, `main_group_id`, `set_group_id`, `zav`, "
                                       f"`obe`, `pol`) VALUES(?,?,?,?,?,?)", (user_id, main, sett, 0, 0, 0))

    def main_group_exists(self, group_id):
        """Проверяем, есть ли уже пользователь в базе"""
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM `main` WHERE `main_group_id` = ?', (group_id,)).fetchall()
            return bool(len(result))

    def get_spec_group(self, group_id):
        """Получение айди групп"""
        with self.connection:
            return self.cursor.execute(f'SELECT `set_group_id` FROM `main` WHERE `main_group_id` = ?',
                                       (group_id,)).fetchone()[0]

    def get_main_group(self, user_id):
        """Получение айди групп"""
        with self.connection:
            return self.cursor.execute(f'SELECT `main_group_id` FROM `main` WHERE `user_id` = ?',
                                       (user_id,)).fetchone()[0]

    def get_spec_groups(self):
        """Получаем все технические группы"""
        with self.connection:
            return self.cursor.execute("SELECT `set_group_id` FROM `main`").fetchall()

    def user_main_exists(self, user_id):
        """Проверяем, есть ли уже пользователь в базе"""
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM `main` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def delete_main_group(self, user_id):
        """Удаление ненужного транзита"""
        with self.connection:
            return self.cursor.execute(f'DELETE FROM `main` WHERE `user_id` = ?', (user_id,))

    def upd_stat_group(self, group_id, var):
        """Обновляем статистику"""
        with self.connection:
            self.cursor.execute("SELECT `zav`, `obe`, `pol` FROM `main` WHERE `main_group_id` = ?", (group_id,))
            if var == "z":
                return self.cursor.execute("UPDATE `main` SET `zav` = ? WHERE `main_group_id` = ?",
                                           ((self.cursor.fetchone()[0] + 1), group_id))
            elif var == 'o':
                return self.cursor.execute("UPDATE `main` SET `obe` = ? WHERE `main_group_id` = ?",
                                           ((self.cursor.fetchone()[1] + 1), group_id))
            elif var == 'p':
                return self.cursor.execute("UPDATE `main` SET `pol` = ? WHERE `main_group_id` = ?",
                                           ((self.cursor.fetchone()[2] + 1), group_id))

    #
    def update_status_group(self, id_group, status):
        """Обновляем статус группы"""
        with self.connection:
            return self.cursor.execute("UPDATE `group` SET `status` = ? WHERE `id_group` = ?", (status, id_group))

    def get_group(self, status=True):
        """Получаем все активные группы"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `group` WHERE `status` = ?", (status,)).fetchall()

    def id_group_lst(self, status=True):
        """Список айди активных групп"""
        with self.connection:
            return [i[1] for i in self.cursor.execute("SELECT * FROM `group` WHERE `status` = ?", (status,)).fetchall()]

    def stat_element_group(self, id_group):
        """Получение данных группы"""
        with self.connection:
            self.cursor.execute("SELECT * FROM `group` WHERE `id_group` = ?", (id_group,))
            data = self.cursor.fetchone()
            time, message, reply, command, url = int(data[3]), int(data[4]), int(data[5]), int(data[6]), int(data[7])
            tik_tok, media, sticker, voice = int(data[8]), int(data[9]), int(data[10]), int(data[11])
            bol, cool = int(data[12]), int(data[13])
            return [message, reply, command, url, tik_tok, media, sticker, voice, time, bol, cool]

    def id_lst(self, db):
        """Список айди"""
        with self.connection:
            return [i[0] for i in self.cursor.execute(f'SELECT id_user FROM `{db}`').fetchall()]

    def name_lst(self, db):
        """Список имён"""
        with self.connection:
            return [i[0] for i in self.cursor.execute(f'SELECT first_name FROM `{db}`').fetchall()]

    # ЗАВЕРШЕНИЕ
    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


class User:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    # СВЯЗКА ПОЛЬЗОВАТЕЛЯ
    def user_exists(self, user_id):
        """Проверяем, есть ли уже пользователь в базе"""
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM `users` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id):
        """Добавляем нового пользователя"""
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `users` (`user_id`) VALUES(?)", (user_id,))

    def get_user_id(self, user_id):
        """Получаем короткое айди юзера"""
        with self.connection:
            return self.cursor.execute(f'SELECT `id` FROM `users` WHERE `user_id` = ?', (user_id,)).fetchone()[0]

    # СВЯЗКА ГРУППЫ
    def group_exists(self, group_id):
        """Проверяем, есть ли уже группа в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `groups` WHERE `group_id` = ?', (group_id,)).fetchall()
            return bool(len(result))

    def add_group(self, group_id):
        """Добавляем новую группу в таблицу"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `groups` (`group_id`) VALUES(?)", (group_id,))

    def get_group_id(self, group_id):
        """Получаем короткое айди юзера"""
        with self.connection:
            return self.cursor.execute(f'SELECT `id` FROM `groups` WHERE `group_id` = ?', (group_id,)).fetchone()[0]

    def get_first_group_id(self, group_id):
        """Получаем длинное айди юзера"""
        with self.connection:
            return self.cursor.execute(f'SELECT `group_id` FROM `groups` WHERE `id` = ?', (group_id,)).fetchone()[0]

    def update_group_id(self, from_id, to_id):
        """Заменяем на новый айди"""
        with self.connection:
            return self.cursor.execute("UPDATE `groups` SET `group_id` = ? WHERE `group_id` = ?", (to_id, from_id))

    # ЗАВЕРШЕНИЕ
    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


class Group:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def created_group(self, group_id):
        """Создаём новую таблицу"""
        with self.connection:
            return self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS [{group_id}] (
                                            user_id    INTEGER     NOT NULL,
                                            first_name STRING (40) NOT NULL,
                                            zav        INTEGER     NULL,
                                            obe        INTEGER     NULL,
                                            pol        INTEGER     NULL
                                            );""")

    def add_user(self, group_id, user_id, first_name):
        """Добавляем нового пользователя"""
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `{group_id}` (`user_id`, `first_name`, `zav`, `obe`, `pol`) "
                                       f"VALUES(?,?,?,?,?)", (user_id, first_name, 0, 0, 0))

    def update_name(self, user_id, name, group_id):
        """Обновляем имя пользователя"""
        with self.connection:
            return self.cursor.execute(f"UPDATE `{group_id}` SET `first_name` = ? WHERE `user_id` = ?", (name, user_id))

    def delete_group(self, group_id):
        """Удаление таблицы с информацией"""
        with self.connection:
            return self.cursor.execute(f"DROP TABLE IF EXISTS [{group_id}]")

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


class Now:
    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def created_group(self, group_id):
        """Создаём новую таблицу"""
        with self.connection:
            return self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS [{group_id}] (
                                            user_id      INTEGER    NOT NULL,
                                            main_mess_id INTEGER    NOT NULL,
                                            set_mess_id  INTEGER    NOT NULL,
                                            ord_id       STRING (1) NOT NULL
                                            );""")

    def add_user(self, group_id, user_id, main_mess, set_mess, ord_id):
        """Добавляем нового пользователя"""
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `{group_id}` (`user_id`, `main_mess_id`, `set_mess_id`, `ord_id `)"
                                       f" VALUES(?,?,?,?)", (user_id, main_mess, set_mess, ord_id))

    def delete_group(self, group_id):
        """Удаление таблицы с информацией"""
        with self.connection:
            return self.cursor.execute(f"DROP TABLE IF EXISTS [{group_id}]")

    def check_user(self, group_id, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM `{group_id}` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def check_group(self):
        """Проверка на наличие таблицы с заказами"""
        with self.connection:
            pass

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
