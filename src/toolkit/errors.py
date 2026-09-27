class ToolkitError(Exception):
    """Базовая ошибка toolkit"""

    def __init__(self, message: str, error_code: str) -> None:
        """
        :param message: текст ошибки для пользователя
        :param error_code: код ошибки
        """
        super().__init__(message)
        self.error_code = error_code

class ConverterError(ToolkitError):
    """Ошибка конвертера"""

class ValidationError(ToolkitError):
    """Ошибка калькулятора"""
