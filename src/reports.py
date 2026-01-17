
import json

from datetime import datetime
from typing import Optional

import pandas as pd

from src.decorators import log, logger


@log()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[datetime] = None) -> str:
    """ Функция возвращает траты по заданной категории за последние три месяца. """

    logger.info("Запрос трат по категории: категория=%s, дата=%s", category, date)
    df = transactions.copy()

    date_end = date or datetime.today()
    date_end = pd.to_datetime(date_end)

    date_start = date_end - pd.DateOffset(months=3)

    df["Дата платежа"] = pd.to_datetime(
        df["Дата платежа"],
        format="%d.%m.%Y",
        dayfirst=True,
    )

    filtered = df[
        (df["Категория"] == category) &
        (df["Дата платежа"] >= date_start) &
        (df["Дата платежа"] <= date_end) &
        (df["Сумма платежа"] < 0)
    ]

    if filtered.empty:
        logger.warning("Траты по категории не найдены: категория=%s, период=%s - %s", category, date_start, date_end)
        result = {
            "Категория": category,
            "От": date_start.strftime("%Y.%m.%d"),
            "До": date_end.strftime("%Y.%m.%d"),
            "Потрачено": 0,
            "Сообщение": "Траты по данной категории за указанный период не найдены."
        }

        return json.dumps(result, ensure_ascii=False, indent=4)

    total_spent = int(filtered["Сумма платежа"].sum() * -1)
    logger.info("Расчет трат: количество операций=%s, сумма=%s", len(filtered), round(total_spent, 2))

    result = {
        "Категория": category,
        "От": date_start.strftime("%Y.%m.%d"),
        "До": date_end.strftime("%Y.%m.%d"),
        "Потрачено": round(total_spent, 2)
    }

    return json.dumps(result, ensure_ascii=False, indent=4)

# if __name__ == "__main__":
#     df = pd.read_excel("../data/operations.xlsx")
#     print(spending_by_category(df, "супермаркеты", "2021.11.12"))
