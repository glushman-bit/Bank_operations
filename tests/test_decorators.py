import pytest

from src.decorators import my_func


def test_log_correct():
    """Проверка правильности работы декоратора"""
    x = my_func(1, 2)
    assert x == 3


def test_decorator_log_error(capsys):
    """Проверка на правильность обработки ошибок"""
    with pytest.raises(TypeError):
        my_func(1, "2")
    captured = capsys.readouterr()
    assert captured.out == ""
