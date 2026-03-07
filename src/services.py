"""
Сервисы
"""

import json
import re
from typing import Dict

import pandas as pd
from pandas import DataFrame

from src.decorators import log
from src.decorators import logger


def normalize_phone(value: str) -> str:
    """Оставляет только цифры в номере телефона."""
    return re.sub(r"\D", "", value)


@log()
def find_transactions_by_phone(df: DataFrame, phone: str) -> list:
    """Возвращает JSON со всеми транзакциями, содержащими указанный номер телефона."""

    normalized_phone = normalize_phone(phone)
    if not normalized_phone:
        logger.warning("Ошибка ввода номера телефона: тел.=%s", phone)
        return []

    normalized_search = df["Описание"].astype(str).str.replace(r"\D", "", regex=True)

    mask = normalized_search.str.contains(normalized_phone)

    if not mask.any():
        logger.warning("Введенный номер телефона не найден: тел.=%s", phone)
        return []

    result_df = df.loc[mask, ["Дата операции", "Сумма платежа", "Категория", "Описание"]]

    logger.info("Вывод транзакций по номеру телефона: тел.=%s", phone)
    return result_df.to_json(orient="records", force_ascii=False, indent=4)


@log()
def cashback_analysis(df: DataFrame, year: int, month: int) -> Dict[str, float]:
    """Анализирует категории повышенного кэшбека."""

    df = df.copy()

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    filter_data = df[
        (df["Дата операции"].dt.year == year)
        & (df["Дата операции"].dt.month == month)
        & (df["Кэшбэк"] > 0)
        & (df["Сумма платежа"] < 0)
    ]

    expenses_by_category = filter_data.groupby("Категория")["Сумма платежа"].sum()

    cashback_by_category = (abs(expenses_by_category) / 100).round(2)
    result = {k: float(v) for k, v in cashback_by_category.items()}
    logger.info("Вывод кэшбэка за год=%s, месяц=%s", year, month)

    return json.dumps(result, ensure_ascii=False, indent=4)
