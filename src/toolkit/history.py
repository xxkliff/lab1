import json
from datetime import datetime
from pathlib import Path

from toolkit.errors import HistoryError


def load_history(path: Path) -> list[dict]:
    """
    Подгружает history.json и парсит его содержимое. Если его не существует - возвращает пустой список

    :param path: путь к файлу в виде объекта Path
    :raises HistoryError: перехватывает стандартные исключения и выкидывает кастомные с соответствующим error_code
    :return: словарь с историей
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            history = json.load(f)
    except FileNotFoundError:
        return []
    except OSError as e:
        raise HistoryError("Нет прав не чтение файла history.json или путь неверный.",
                           "permission_error") from e
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise HistoryError("JSON файл с историей не читается. Пожалуйста, исправьте его или удалите.",
                           "json_decode_error") from e

    if isinstance(history, list):
        return history

    raise HistoryError(
        "В JSON находится не список. Пожалуйста, исправьте его или удалите.",
        "json_history_format",
    )


def add_entry(path: Path, expression: str, result: float) -> None:
    """
    Добавляет запись в формате {"expression": выражение, "result": результат}. До этого файл подгружает историю и
    проходит через проверки функции load_history

    :param path: путь к файлу в виде объекта Path
    :param expression: выражение в виде строки
    :param result: полученный результат
    :raises HistoryError: перехватывает стандартные исключения и выкидывает кастомные с соответствующим error_code
    :return:
    """
    history = load_history(path)

    current_time = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")

    entry = {"expression": expression, "result": result, "time": current_time}
    history.append(entry)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
    except PermissionError as e:
        raise HistoryError(f"Нет прав для записи в файл {path}.",
                           "permission_error") from e
    except OSError as e:
        raise HistoryError(f"Произошла системная ошибка: {e}", "os_error") from e
