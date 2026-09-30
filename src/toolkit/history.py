import errno
import json
from pathlib import Path

from toolkit.errors import HistoryError


def load_history(path: Path) -> list[dict]:
    """
    Подгружает history.json и парсит его содержимое. Если его не существует - возвращает пустой список

    :param path: путь к файлу в виде объекта Path
    :return: словарь с историей
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            history = json.load(f)

        if isinstance(history, list):
            return history

        raise HistoryError("В JSON находится не список. Пожалуйста, исправьте его или удалите.",
                           "json_history_format") from None
    except FileNotFoundError:
        return []
    except json.decoder.JSONDecodeError:
        raise HistoryError("JSON файл с историей не читается. Пожалуйста, исправьте его или удалите.",
                           "json_decode_error") from None


# def add_entry()

print(load_history(Path("history.json")))
