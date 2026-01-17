
import json

import pandas as pd
from pandas import DataFrame

from src.decorators import log, logger
from src.utils import get_curs_currency, get_list_cards, get_time_for_greeting, stock_prices, top_transactions

@log()
def main_info(df: DataFrame, currency, stocks):
    """ Основная функция, собирает все данные из модуля utils.py в итоговый json для станицы главная. """


    greet = get_time_for_greeting()
    cards = get_list_cards(df)
    top_transaction = top_transactions(df)
    currency_rates = get_curs_currency(currency)
    stock_price = stock_prices(stocks)

    logger.info("Вывод итогового JSON-ответа.")
    result = {
        "greeting": greet,
        "cards": cards,
        "top_transaction": top_transaction,
        "currency_rates": currency_rates,
        "stock_prices": stock_price
    }
    return json.dumps(result, ensure_ascii=False, indent=4)



