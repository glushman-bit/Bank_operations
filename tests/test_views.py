
import pytest
import json
from unittest.mock import patch
from src.views import main_info

@pytest.mark.parametrize("currency, stock", [("USD", "AAPL")])
def test_main_info_with_mocks(main_info_data, currency, stock):
    # Мокаем внешние функции внутри views
    with patch("src.views.get_curs_currency", return_value=[{"currency": currency, "rate": 73.21}]), \
         patch("src.views.stock_prices", return_value=[{"stock": stock, "price": 150.12}]), \
         patch("src.views.get_time_for_greeting", return_value="Добрый день"), \
         patch("src.views.get_list_cards", return_value=[{
             "last_digits": "5814",
             "total_spent": 1262.0,
             "cashback": 12.62
         }]), \
         patch("src.views.top_transactions", return_value=[{
             "date": "21.12.2021",
             "amount": 1198.23,
             "category": "Переводы",
             "description": "Перевод Кредитная карта. ТП 10.2 RUR"
         }]):

        result_json = main_info(main_info_data, currency, stock)
        result = json.loads(result_json)

        assert result["greeting"] == "Добрый день"
        assert result["cards"] == [{
            "last_digits": "5814",
            "total_spent": 1262.0,
            "cashback": 12.62
        }]
        assert result["top_transaction"] == [{
            "date": "21.12.2021",
            "amount": 1198.23,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR"
        }]
        assert result["currency_rates"] == [{"currency": currency, "rate": 73.21}]
        assert result["stock_prices"] == [{"stock": stock, "price": 150.12}]






[
    {
        "last_digit": "1112",
        "total_spent": 46207.08,
        "cashback": 462.07
    },
    {
        "last_digit": "4556",
        "total_spent": 1780150.21,
        "cashback": 17801.5
    },
    {
        "last_digit": "5091",
        "total_spent": 17367.5,
        "cashback": 173.68
    },
    {
        "last_digit": "5441",
        "total_spent": 470854.8,
        "cashback": 4708.55
    },
    {
        "last_digit": "5507",
        "total_spent": 84000.0,
        "cashback": 840.0
    },
    {
        "last_digit": "6002",
        "total_spent": 69200.0,
        "cashback": 692.0
    },
    {
        "last_digit": "7197",
        "total_spent": 2487419.56,
        "cashback": 24874.2
    }
]