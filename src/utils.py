import json
import os
from datetime import datetime
from typing import List

import requests
from dotenv import load_dotenv
from pandas import DataFrame

from src.decorators import log
from src.decorators import logger

load_dotenv()


@log()
def get_time_for_greeting():
    """Функция приветствия в зависимости от времени суток"""

    user_current_hour = datetime.now().hour
    logger.info("Вывод приветствия.")
    if 5 <= user_current_hour < 12:
        return "Доброе утро"
    elif 12 <= user_current_hour < 18:
        return "Добрый день"
    elif 18 <= user_current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


@log()
def get_list_cards(datafile: DataFrame) -> list:
    """Функция, которая принимает DataFrame и возвращает список карт с расходами"""
    filter_df = datafile[datafile["Сумма платежа"] < 0]
    group_df = filter_df.groupby("Номер карты")
    summary_df = group_df["Сумма платежа"].sum().abs()
    dict_df = summary_df.to_dict()

    logger.info("Вывод списка карт.")
    df_list = []

    for key, value in dict_df.items():
        df_list.append(
            {
                "last_digits": str(key[-4:]),
                "total_spent": round(float(value), 2),
                "cashback": round(float(value) / 100, 2),
            }
        )

    return df_list


@log()
def top_transactions(df: DataFrame) -> list:
    """Функция, которая принимает DataFrame и возвращает список Top-5 платежей"""
    sort_df = df.loc[df["Сумма платежа"] < 0].sort_values(by="Сумма платежа")
    list_top = sort_df[:5].to_dict(orient="records")

    logger.info("Вывод списка Топ-5 платежей.")
    df_list = []

    for i in list_top:
        df_list.append(
            {
                "date": i["Дата платежа"],
                "amount": i["Сумма платежа"] * (-1),
                "category": i["Категория"],
                "description": i["Описание"],
            }
        )

    return df_list


@log()
def get_curs_currency(currency: str) -> List[dict]:
    """Функция, которая возвращает курс валют по API запросу"""

    base = "RUB"
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={currency}&base={base}"

    headers = {"apikey": os.getenv("API_KEY_C")}

    logger.info("Запрос на сайт: https://api.apilayer.com")
    data = requests.get(url, headers=headers, timeout=10)

    status = data.status_code

    if status != 200:
        logger.error(f"Сайт не доступен: {status}")

        return []

    try:
        data = data.json()
        rates = data.get("rates", {})

        result = []

        for k, v in rates.items():
            result.append({"currency": k, "rate": round(1 / v, 2)})
        logger.info("Вывод курса валют: %s", currency)

        return result

    except json.decoder.JSONDecodeError:
        logger.exception("Неверный формат файла JSON")

        return []


@log()
def stock_prices(stock: str) -> list[dict[str, float | str]]:
    """Функция, которая возвращает стоимость акций по API запросу"""

    api_key = os.getenv("API_KEY_S")

    url = "https://api.twelvedata.com/price"
    params = {"symbol": stock, "apikey": api_key}

    logger.info("Запрос на сайт: https://api.twelvedata.com")
    data = requests.get(url, params=params)
    status = data.status_code

    if status != 200:
        logger.error(f"Сайт не доступен: {status}")

        return []

    try:
        data = data.json()
        result = []

        for k, v in data.items():
            result.append({"stock": k, "price": round(float(v["price"]), 2)})

        logger.info("Вывод курса акций: %s", stock)

        return result

    except json.decoder.JSONDecodeError:
        logger.exception("Неверный формат файла JSON")

        return []
