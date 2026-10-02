import os

# Токен бота от @BotFather — из переменной окружения BOT_TOKEN
TOKEN = os.environ.get("BOT_TOKEN", "")

# Числовой ID бота и ID технической группы для служебных сообщений — тоже из окружения
ID_BOT = int(os.environ.get("BOT_ID", "0"))
TEX_GROUP = os.environ.get("TECH_GROUP_ID", "")
