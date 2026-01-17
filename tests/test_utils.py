

import json
from freezegun import freeze_time
from unittest.mock import patch, Mock
from src.utils import get_time_for_greeting
from src.utils import get_list_cards
from src.utils import top_transactions
from src.utils import get_curs_currency
from src.utils import stock_prices



@freeze_time("2026-01-01 7:00:00")
def test_get_time_for_greeting_morning():
    morning = "Доброе утро"
    assert morning == get_time_for_greeting()



@freeze_time("2026-01-01 13:00:00")
def test_get_time_for_greeting_afternoon():
    afternoon = "Добрый день"
    assert afternoon == get_time_for_greeting()


@freeze_time("2026-01-01 19:00:00")
def test_get_time_for_greeting_evening():
    evening = "Добрый вечер"
    assert evening == get_time_for_greeting()

@freeze_time("2026-01-01 01:00:00")
def test_get_time_for_greeting_night():
    night = "Доброй ночи"
    assert night == get_time_for_greeting()


def test_get_list_cards_correct(main_info_data):
    assert get_list_cards(main_info_data) == [
        {"last_digit": "1111", "total_spent": 2000, "cashback": 20.0},
        {"last_digit": "2222", "total_spent": 3000, "cashback": 30.0}
    ]


def test_top_transactions_correct(main_info_data):
    assert top_transactions(main_info_data) == [
        {"date": "22.12.2021", "amount": 3000, "category": "Покупки", "description": "Покупка в магазине"},
        {"date": "21.12.2021", "amount": 2000, "category": "Переводы",
        "description": "Перевод Кредитная карта. ТП 10.2 RUR"}
    ]

def test_get_curs_currency_correct():
    currency = "USD"
    response_mock = Mock()
    response_mock.json.return_value = {"rates": {"USD": 0.0136}}
    response_mock.status_code = 200

    with patch("src.utils.requests.get", return_value=response_mock):
        assert get_curs_currency(currency) == [{"currency": "USD", "rate": 73.53}]


def test_get_curs_currency_not_connect():
    currency = "USD"
    response_mock = Mock()
    response_mock.status_code = 500

    with patch("src.utils.requests.get", return_value=response_mock):
        assert get_curs_currency(currency) == []


def test_get_curs_currency_not_json():
    currency = "USD"
    response_mock = Mock()
    response_mock.json.side_effect = json.decoder.JSONDecodeError("err", "", 0)
    response_mock.status_code = 200

    with patch("src.utils.requests.get", return_value=response_mock):
        assert get_curs_currency(currency) == 0



def test_stock_prices_correct():
    stock = "AAPL"
    response_mock = Mock()
    response_mock.json.return_value = {"AAPL": {"price": 230.0}}
    response_mock.status_code = 200

    with patch("src.utils.requests.get", return_value=response_mock):
        assert stock_prices(stock) == [{"stock": "AAPL", "price": 230.0}]


def test_stock_prices_not_connect():
    stock = "AAPL"
    response_mock = Mock()
    response_mock.status_code = 500

    with patch("src.utils.requests.get", return_value=response_mock):
        assert stock_prices(stock) == []


def test_stock_prices_not_json():
    stock = "AAPL"
    response_mock = Mock()
    response_mock.json.side_effect = json.decoder.JSONDecodeError("err", "", 0)
    response_mock.status_code = 200

    with patch("src.utils.requests.get", return_value=response_mock):
        assert stock_prices(stock) == 0



