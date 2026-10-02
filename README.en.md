# School Menu Bot

[Русский](README.md) · **English**

[![CI](https://github.com/EDeev/school_menu/actions/workflows/ci.yml/badge.svg)](https://github.com/EDeev/school_menu/actions/workflows/ci.yml)

A school cafeteria Telegram bot: every morning it posts the menu from the school website, takes breakfast,
lunch and snack orders by class and compiles a summary for the cafeteria.

**Status:** school project (2021–2022), completed, archived

**Stack:** Python 3.10 · aiogram 2 · SQLite · openpyxl (menu from Excel) · pymorphy2

- Today's and tomorrow's menu (`/today`, `/tomorrow`) and a 06:00 broadcast
- Ordering with buttons, cancelling and changing an order
- Class registration by code, separate groups for students and the cafeteria
- Order summary by class with correct Russian word forms

## Running

```bash
pip install -r requirements.txt
cd code && BOT_TOKEN=token BOT_ID=bot_id TECH_GROUP_ID=group_id python bot.py
```

Portion weights and calories from Excel are parsed without `eval`: only numbers and `+ - * /` are allowed.

## License

School project (2021–2022). The code is open for study; there is no separate license.

## Author

**Egor Deev** — [GitHub](https://github.com/EDeev) · [Telegram](https://t.me/DeevEgor) · [egor@deev.space](mailto:egor@deev.space)

---

<div align="center">
  <sub>⭐ If you find this project useful, give it a star on GitHub!</sub>
  <p><sub>Made with ❤️ — <a href="https://deev.space">deev.space</a></sub></p>
</div>
