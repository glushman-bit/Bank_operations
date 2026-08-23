import json

import pytest

from src.services import cashback_analysis
from src.services import find_transactions_by_phone


@pytest.mark.parametrize(
    "year,month,expected",
    [
        (2025, 10, {"супермаркеты": 40.0, "ресторан": 30.0}),
        (2025, 11, {"аптека": 20.0}),
        (2025, 12, {"кафе": 10.0}),
    ],
)
def test_cashback_analysis_parametrize(cashback_and_phone_data, year: int, month: int, expected):
    result = cashback_analysis(cashback_and_phone_data, year, month)
    data = json.loads(result)
    assert data == expected


def test_find_transactions_by_phone(cashback_and_phone_data):
    phone = "+7 (123) 456-78-90"
    result = find_transactions_by_phone(cashback_and_phone_data, phone)
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["Категория"] == "супермаркеты"
    assert "1234567890" in "".join(filter(str.isdigit, data[0]["Описание"]))


def test_find_transactions_by_phone_empty(cashback_and_phone_data):
    phone = ""
    result = find_transactions_by_phone(cashback_and_phone_data, phone)
    assert result == "Ошибка ввода номера телефона."


def test_find_transactions_by_phone_not_find(cashback_and_phone_data):
    phone = "9999999999"
    result = find_transactions_by_phone(cashback_and_phone_data, phone)
    assert result == "Номер телефона не найден."


def test_cashback_analysis_filter_data_empty(filter_data_empty):
    result = cashback_analysis(filter_data_empty, 2025, 1)
    assert result == "По вашему запросу ничего не найдено."
