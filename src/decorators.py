import logging
from functools import wraps
from pathlib import Path
from typing import Callable

log_folder = Path(__file__).parent.parent / "logs"
log_folder.mkdir(parents=True, exist_ok=True)
log_file = log_folder / "mylog.txt"
# создание файла mylog.txt в директории logs


def logger_init() -> logging.Logger:
    logg = logging.getLogger("app")
    logg.setLevel(logging.INFO)

    if not logg.handlers:
        handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(funcName)s - %(name)s - %(levelname)s: - %(message)s")
        consol = logging.StreamHandler()
        consol.setFormatter(formatter)
        handler.setFormatter(formatter)

        # logg.addHandler(consol)
        logg.addHandler(handler)

    return logg


logger = logger_init()


def log() -> Callable:
    """Декоратор, который создает log-и на работу функции и ее результат в файл или консоль."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                logger.info("Успешный запуск функции: %s - %s", {func.__name__}, {func.__doc__})
                return result

            except Exception as e:
                logger.exception("Ошибка: %s: %s: %s", {func.__name__}, {type(e).__name__}, {e})
                raise

        return wrapper

    return decorator


@log()
def my_func(x, y):
    """Функция для проверки декоратора"""
    return x + y
