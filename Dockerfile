# Школьный Telegram-бот столовой (aiogram 2). pymorphy2 0.9 не работает на Python 3.11+
FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY code code
# базы из репозитория — в том /app/db при первом запуске
COPY db /opt/db-seed
COPY docker/entrypoint.sh /entrypoint.sh
VOLUME ["/app/db"]
WORKDIR /app/code
ENTRYPOINT ["sh", "/entrypoint.sh"]
