import asyncio
import logging
import os
import re

import nest_asyncio
from database import add_schedule, create_db, get_schedule
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(level=logging.INFO)
nest_asyncio.apply()

# Замените 'YOUR_TOKEN' на токен вашего бота
# from .env
load_dotenv()
TOKEN = os.getenv("API_KEY")

# Регулярное выражение для проверки формата даты (ДД.ММ.ГГГГ)
DATE_REGEX = r"^\d{2}\.\d{2}\.\d{4}$"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Я бот для расписания. Отправьте дату в формате ДД.ММ.ГГГГ для получения расписания или дату и предмет для добавления."
    )


# async def dispAll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text(
#         'Привет! Я бот для расписания. Отправьте дату в формате ДД.ММ.ГГГГ для получения расписания или дату и предмет для добавления.')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text.strip()
    parts = message_text.split(" ", 1)  # Разделяем на дату и предмет (если есть)

    if len(parts) == 0:
        return

    date = parts[0]
    for index, part in enumerate(parts):
        logging.info(f"data{index} {part}")

    # Проверка формата даты
    if re.match(DATE_REGEX, date):
        if len(parts) == 1:
            # Запрос расписания
            subjects = await get_schedule(date)
            if subjects:
                subjects_list = "\n".join([f"{subject[0]}" for subject in subjects])
                await update.message.reply_text(
                    f"Расписание на {date}:\n{subjects_list}"
                )
            else:
                await update.message.reply_text(f"Нет расписания на {date}.")
        elif len(parts) == 2:
            # Добавление предмета
            def add_item(date: str, item: str) -> str:
                """Добавляет предмет в расписание на указанный день."""

            subject = parts[1]
            await add_schedule(date, subject)
            await update.message.reply_text(f"Добавлено: {subject} на {date}.")
    else:
        await update.message.reply_text("Неверный формат даты. Используйте ДД.ММ.ГГГГ.")


async def main():
    await create_db()  # Создаем базу данных и таблицы
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    # app.add_handler(CommandHandler('all', dispAll))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )  # Обрабатываем текстовые сообщения

    app.run_polling()  # Запускаем бота


if __name__ == "__main__":
    asyncio.run(main())
