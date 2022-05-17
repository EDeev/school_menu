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

    def upd_stat_group(self, group_id, var, count):
        """Обновляем статистику"""
        with self.connection:
            self.cursor.execute("SELECT `zav`, `obe`, `pol` FROM `main` WHERE `main_group_id` = ?", (group_id,))
            if var == "z":
                return self.cursor.execute("UPDATE `main` SET `zav` = ? WHERE `main_group_id` = ?",
                                           ((self.cursor.fetchone()[0] + count), group_id))
            elif var == 'o':
                return self.cursor.execute("UPDATE `main` SET `obe` = ? WHERE `main_group_id` = ?",
                                           ((self.cursor.fetchone()[1] + count), group_id))
            elif var == 'p':
                return self.cursor.execute("UPDATE `main` SET `pol` = ? WHERE `main_group_id` = ?",
                                           ((self.cursor.fetchone()[2] + count), group_id))

    def stat_group(self, group_id):
        """Получение данных группы"""
        with self.connection:
            return self.cursor.execute("SELECT `zav`, `obe`, `pol` FROM `main` WHERE `main_group_id` = ?",
                                       (group_id,)).fetchone()

    # ПРОЦЕСС
    def check_group_inproc(self, group_id):
        """Проверка на наличие таблицы с заказами"""
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM `proc` WHERE `group_id` = ?', (group_id,)).fetchall()
            return bool(len(result))

    def add_group(self, group_id):
        """Добавляем нового пользователя из транзита"""
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `proc` (`group_id`) VALUES(?)", (group_id,))

    def reset_proc(self):
        """Удаление всех групп"""
        with self.connection:
            return self.cursor.execute('DELETE FROM `proc`')

    def del_group(self, group_id):
        """Удаление ненужного транзита"""
        with self.connection:
            return self.cursor.execute(f'DELETE FROM `proc` WHERE `group_id` = ?', (group_id,))

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

    def upd_stat_user(self, group_id, user_id, var, count):
        """Обновляем статистику"""
        with self.connection:
            self.cursor.execute(f"SELECT `zav`, `obe`, `pol` FROM `{group_id}` WHERE `user_id` = ?", (user_id,))
            if var == "z":
                return self.cursor.execute(f"UPDATE `{group_id}` SET `zav` = ? WHERE `user_id` = ?",
                                           (str(self.cursor.fetchone()[0] + count), user_id))
            elif var == 'o':
                return self.cursor.execute(f"UPDATE `{group_id}` SET `obe` = ? WHERE `user_id` = ?",
                                           (str(self.cursor.fetchone()[1] + count), user_id))
            elif var == 'p':
                return self.cursor.execute(f"UPDATE `{group_id}` SET `pol` = ? WHERE `user_id` = ?",
                                           (str(self.cursor.fetchone()[2] + count), user_id))

    def stat_all_users(self, group_id):
        """Список имён"""
        with self.connection:
            return self.cursor.execute(f'SELECT `first_name`, `zav`, `obe`, `pol` FROM `{group_id}`').fetchall()

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
                                            ord_id       STRING     NOT NULL
                                            );""")

    def add_user(self, group_id, user_id, main_mess, set_mess, ord_id):
        """Добавляем нового пользователя"""
        with self.connection:
            return self.cursor.execute(f"INSERT INTO `{group_id}` (`user_id`, `main_mess_id`, `set_mess_id`, `ord_id`)"
                                       f" VALUES(?,?,?,?)", (user_id, main_mess, set_mess, ord_id))

    def del_user(self, group_id, user_id):
        """Удаление пользователя"""
        with self.connection:
            return self.cursor.execute(f'DELETE FROM `{group_id}` WHERE `user_id` = ?', (user_id,))

    def delete_group(self, group_id):
        """Удаление таблицы с информацией"""
        with self.connection:
            return self.cursor.execute(f"DROP TABLE IF EXISTS [{group_id}]")

    def check_user(self, group_id, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute(f'SELECT * FROM `{group_id}` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def get_ord_id(self, group_id, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            return self.cursor.execute(f'SELECT `ord_id` FROM `{group_id}` WHERE `user_id` = ?',
                                       (user_id,)).fetchone()[0]

    def get_message(self, group_id, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            return self.cursor.execute(f'SELECT `main_mess_id`, `set_mess_id` FROM `{group_id}` WHERE `user_id` = ?',
                                       (user_id,)).fetchone()

    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()
