# School Menu Bot

**Русский** · [English](README.en.md)

[![CI](https://github.com/EDeev/school_menu/actions/workflows/ci.yml/badge.svg)](https://github.com/EDeev/school_menu/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/EDeev/school_menu)](https://github.com/EDeev/school_menu/releases)

Telegram-бот школьной столовой: каждое утро присылает меню с сайта школы, принимает заказы завтраков,
обедов и полдников по классам и собирает сводку для столовой.

**Статус:** школьный проект (2021–2022), завершён, в архиве

**Стек:** Python 3.10 · aiogram 2 · SQLite · openpyxl (меню из Excel) · pymorphy2

- Меню на сегодня и завтра (`/today`, `/tomorrow`) и рассылка в 06:00
- Заказ питания кнопками, отмена и изменение заказа
- Регистрация класса по коду, отдельные группы для учеников и для столовой
- Сводка заказов по классам с правильным склонением слов

## Запуск

```bash
pip install -r requirements.txt
cd code && BOT_TOKEN=токен BOT_ID=id_бота TECH_GROUP_ID=id_группы python bot.py
```

Граммовка и калорийность из Excel разбираются без `eval`: допускаются только числа и `+ - * /`.

**Docker:** `docker run -d -e BOT_TOKEN=токен -e BOT_ID=id_бота -e TECH_GROUP_ID=id_группы -v school-menu-db:/app/db ghcr.io/edeev/school_menu`
(то же — `git.deev.su/edeev/school_menu`); при первом запуске в том копируются базы из репозитория.

## Лицензия

Школьный проект (2021–2022). Код открыт для изучения, отдельной лицензии нет.

## Автор

**Деев Егор Викторович** — [GitHub](https://github.com/EDeev) · [Telegram](https://t.me/DeevEgor) · [egor@deev.space](mailto:egor@deev.space)

---

<div align="center">
  <sub>⭐ Если проект оказался полезным, поставьте звёздочку на GitHub!</sub>
  <p><sub>Сделано с ❤️ — <a href="https://deev.space">deev.space</a></sub></p>
</div>
