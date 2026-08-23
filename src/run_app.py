import json
from datetime import datetime

import pandas as pd

from src.reports import spending_by_category
from src.services import cashback_analysis
from src.services import find_transactions_by_phone
from views import main_info

df = pd.read_excel("data/operations.xlsx")
with open("data/user_settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
    stocks = ",".join(settings["user_stocks"])
    currency = ",".join(settings["user_currencies"])


def run_app():
    """Основная функция запуска приложения."""

    print(main_info(df, currency, stocks))

    user_input = input("Проверить транзакции по номеру телефона? да/нет - ").strip().lower()
    if user_input == "да":
        phone = input("Введите номер телефона или первые цифры: ").strip()

        print(find_transactions_by_phone(df, phone))
    else:

        print("Операция отменена.")

    user_input = input("Проверить транзакции по категории за 3 месяца? да/нет - ").strip().lower()

    if user_input == "да":
        user_category = input("Введите категорию: ").strip()
        user_date = input("Введите дату конца периода в формате, по умолчанию дата-сегодня: гггг.мм.дд: ").strip()

        try:
            user_date = datetime.strptime(user_date, "%Y.%m.%d") if user_date else datetime.today()

        except ValueError:
            print("Неверный формат даты. Используется сегодняшняя дата.")
            user_date = datetime.today()

        print(spending_by_category(df, user_category, user_date))

    else:

        print("Операция отменена")

    user_input = input("Проверить выгодные категории повышенного кешбэка за месяц? да/нет - ").strip().lower()

    if user_input == "да":

        try:
            input_year = int(input("введите год в формате: гггг - ").strip())
            input_month = int(input("введите месяц в формате: мм - ").strip())

            if not 1 <= input_month <= 12:
                raise ValueError("Месяц должен быть от 1 до 12.")

            print(cashback_analysis(df, input_year, input_month))
            print("Конец работы программы.")

        except ValueError:
            print("Ошибка: год и месяц должны быть числом.")


    else:

        print("Операция отменена")
        print("Конец работы программы.")
