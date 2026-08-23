import json
from unittest.mock import patch

import pytest

from src.views import main_info


@pytest.mark.parametrize("currency, stock", [("USD", "AAPL")])
def test_main_info_with_mocks(main_info_data, currency, stock):
    # Мокаем внешние функции внутри views
    with patch("src.views.get_curs_currency", return_value=[{"currency": currency, "rate": 73.21}]), patch(
        "src.views.stock_prices", return_value=[{"stock": stock, "price": 150.12}]
    ), patch("src.views.get_time_for_greeting", return_value="Добрый день"), patch(
        "src.views.get_list_cards", return_value=[{"last_digits": "5814", "total_spent": 1262.0, "cashback": 12.62}]
    ), patch(
        "src.views.top_transactions",
        return_value=[
            {
                "date": "21.12.2021",
                "amount": 1198.23,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR",
            }
        ],
    ):

        result_json = main_info(main_info_data, currency, stock)
        result = json.loads(result_json)

        assert result["greeting"] == "Добрый день"
        assert result["cards"] == [{"last_digits": "5814", "total_spent": 1262.0, "cashback": 12.62}]
        assert result["top_transaction"] == [
            {
                "date": "21.12.2021",
                "amount": 1198.23,
                "category": "Переводы",
                "description": "Перевод Кредитная карта. ТП 10.2 RUR",
            }
        ]
        assert result["currency_rates"] == [{"currency": currency, "rate": 73.21}]
        assert result["stock_prices"] == [{"stock": stock, "price": 150.12}]
