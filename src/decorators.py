
import logging
from functools import wraps
from pathlib import Path
from typing import Callable

log_folder = Path(__file__).parent.parent / "logs"
log_folder.mkdir(parents=True, exist_ok=True)
log_file = log_folder / "mylog.txt"
# создание файла mylog.txt в директории logs


def logger_init():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler= logging.FileHandler(log_file, mode="w", encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(funcName)s - %(name)s - %(levelname)s: - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

logger = logger_init()



def log() -> Callable:
    """Декоратор, который создает log-и на работу функции и ее результат в файл или консоль."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                logger.info(f'Успешный запуск функции: {func.__name__} - {func.__doc__}')
                return result

            except Exception as e:
                logger.exception(f'Ошибка: {func.__name__}: {type(e).__name__}: {e}')
                raise

        return wrapper

    return decorator

@log()
def my_func(x, y):
    """Функция для проверки декоратора"""
    return x + y
