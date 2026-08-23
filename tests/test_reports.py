import json
from datetime import datetime

from src.reports import spending_by_category


def test_spending_by_category_success(transactions_data):
    date = datetime(2026, 1, 12)

    result = spending_by_category(transactions_data, "супермаркеты", date)
    data = json.loads(result)

    assert data["Категория"] == "супермаркеты"
    assert data["Потрачено"] == 1000
    assert data["От"] == "2025.10.12"
    assert data["До"] == "2026.01.12"


def test_spending_by_category_empty(transactions_data):
    date = datetime(2026, 1, 12)

    result = spending_by_category(transactions_data, "еда", date)
    data = json.loads(result)

    assert data["Категория"] == "еда"
    assert data["Потрачено"] == 0
