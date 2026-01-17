

from src.decorators import log, logger

import pandas as pd
import json

from src.views import main_info
from src.services import find_transactions_by_phone
from src.reports import spending_by_category
from datetime import datetime
from src.services import cashback_analysis



df = pd.read_excel("data/operations.xlsx")
with open("data/user_settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
    stocks = ",".join(settings["user_stocks"])
    currency = ",".join(settings["user_currencies"])


if __name__ == '__main__':

    print(main_info(df, currency, stocks))
    user_input = input("Проверить транзакции по номеру телефона? да/нет - ").lower()
    if user_input == "да":
        phone = input("Введите номер телефона или первые цифры: ").strip()

        print(find_transactions_by_phone(df, phone))
    else:

        print("Операция отменена.")

    user_input = input("Проверить транзакции по категории за 3 месяца? да/нет - ").strip().lower()
    if user_input == "да":
        user_category = input("Введите категорию: ")
        user_date = input("Введите дату конца периода в формате, по умолчанию дата-сегодня: гггг.мм.дд: ").strip()


        try:
            user_date = datetime.strptime(user_date, "%Y.%m.%d") if user_date else datetime.today()
        except ValueError:
            user_date = datetime.today()

        print(spending_by_category(df, user_category, user_date))

    else:

        print("Операция отменена")

    user_input = input("Проверить выгодные категории повышенного кешбэка за месяц? да/нет - ").strip().lower()
    if user_input == "да":
        input_year = int(input("введите год в формате: гггг - ").strip())
        input_month = int(input("введите месяц в формате: мм - ").strip())

        print(cashback_analysis(df, input_year, input_month))
        print("Конец работы программы.")
    else:

        print("Операция отменена")
        print("Конец работы программы.")


