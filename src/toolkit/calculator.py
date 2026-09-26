
from toolkit.constants import OPERATORS, PRIORITY
from toolkit.errors import ValidationError


def _tokenize(expression: str) -> list[str]:
    """
    Разбивает строку выражения на токены: числа и операторы

    Пробелы пропускаются, недопустимые символы тоже становятся токенами, потом их отсекает _validate
    "//" воспринимается как один токен

    :param expression: исходная строка, введённая пользователем
    :return: список токенов
    """
    tokens: list[str] = []
    i = 0

    while i < len(expression):
        char = expression[i]

        if char.isspace():
            i += 1
            continue

        if expression[i:i + 2] == "//":
            tokens.append(expression[i:i + 2])
            i += 2
            continue

        if char.isdigit() or char == ".":
            start = i
            while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            tokens.append(expression[start:i])

            continue

        if char in OPERATORS:
            tokens.append(char)
            i += 1
            continue

        tokens.append(char)
        i += 1

    return tokens


def _is_number(token: str) -> bool:
    try:
        float(token)
    except ValueError:
        return False
    return True


def _validate(tokens: list[str]) -> bool:
    """
    Проверяет, что токены образуют корректное выражение: числа и операторы чередуются, унарный знак стоит только
    перед числом

    :param tokens: Токены в обычном виде
    :raises ValidationError: выкидывается с определённым кодом, если выражение не прошло проверку
    :return: True, если все проверки прошли
    """
    if not tokens:
        raise ValidationError("выражение пустое или некорректно.", "empty_expression")

    expecting_number = True
    after_sign = False

    for token in tokens:
        if expecting_number:
            if token in ("+", "-") and not after_sign:
                after_sign = True
                continue

            if token in OPERATORS:
                raise ValidationError("несколько операторов не могут стоять подряд.", "unexpected_operator")
            if not _is_number(token):
                raise ValidationError("в выражении используются недопустимые символы.", "invalid_number")

            after_sign = False
            expecting_number = False
        else:
            if _is_number(token):
                raise ValidationError("между числами отсутствует оператор.", "missing_operator")
            if token not in OPERATORS:
                raise ValidationError("в выражении используются недопустимые символы.", "invalid_number")

            expecting_number = True

    if expecting_number:
        raise ValidationError("выражение не может заканчиваться на оператор.", "missing_operand")

    return True


def _merge_unary_signs(tokens: list[str]) -> list[str]:
    """
    Приклеивает унарный + или - к следующему числу за ним

    Знак считается унарным в двух случаях:

    1) если стоит в начале выражения
    2) если стоит после другого оператора

    :param tokens: токены в обычной записи
    :return: токены, где унарные операторы соединены с числом
    """
    output: list[str] = []
    i = 0

    while i < len(tokens):
        merge_token = tokens[i]
        prev_token = tokens[i - 1] if i > 0 else ""
        next_token = tokens[i + 1] if i + 1 < len(tokens) else ""

        if merge_token in ("+", "-") and (prev_token == "" or prev_token in OPERATORS):
            output.append(merge_token + next_token)
            i += 2
            continue

        if merge_token in OPERATORS:
            output.append(merge_token)
            i += 1
            continue

        output.append(merge_token)
        i += 1

    return output


def _to_rpn(expression: list[str]) -> list[str]:
    """
    Переводит токены в обратную польскую запись с помощью алгоритма сортировочной станции Дейкстры
    Приоритет операторов берётся из constants.py

    Токены должны быть валидированы, иначе составится неправильный rpn, что приведёт к ошибке RuntimeError
    из _calculate_rpn

    :param expression: токены в обычной записи
    :return: токены в постфиксной записи
    """
    stack: list[str] = []
    output: list[str] = []

    for token in expression:
        try:
            float(token)
            output.append(token)
        except ValueError:
            while stack and PRIORITY[stack[-1]] >= PRIORITY[token]:
                output.append(stack.pop())

            stack.append(token)

    while stack:
        output.append(stack.pop())

    return output


def _apply_operator(a: float, b: float, operator: str) -> float:
    """
    Применяет бинарный оператор к двум числам a и b в соответствующем порядке

    :raises ValidationError: при делении на ноль или неизвестном операторе
    """
    try:
        match operator:
            case "+":
                return a + b
            case "-":
                return a - b
            case "*":
                return a * b
            case "/":
                return a / b
            case "//":
                return a // b
            case "%":
                return a % b
            case _:
                raise ValidationError("выражение содержит неподдерживаемый оператор.", 'undefined_operator')
    except ZeroDivisionError:
        raise ValidationError("деление на ноль", 'division_by_zero')


def _calculate_rpn(rpn_tokens: list[str]) -> float:
    """
    Алгоритм вычисления результата из обратной польской записи

    :param rpn_tokens: Токены в постфиксной записи
    :return: результат вычислений, например 5.0
    :raises RuntimeError: возникает из-за возможной ошибки в коде. При правильном порядке выполнения функций не выкинется
    """
    stack: list[float] = []

    for token in rpn_tokens:
        if _is_number(token):
            stack.append(float(token))
        else:
            if len(stack) < 2:
                raise RuntimeError("Неверно составленный RPN (не хватает операндов).")

            num2 = stack.pop()
            num1 = stack.pop()

            stack.append(_apply_operator(num1, num2, token))

    if len(stack) != 1:
        raise RuntimeError("Неверно составленный RPN (в RPN должно остаться одно значение).")

    return float(stack[0])


def evaluate(expression: str) -> float:
    """
    Вычисляет арифметическое выражение

    Выражение проходит через путь: токенизация -> валидация -> склейка унарных знаков ->
    перевод в обратную польскую запись -> вычисление результата из неё

    :param expression: выражение, например "2 + 3 * -4"
    :raises ValidationError: выкидывает при любых возможных ошибках с определённым error_code
    :return: результат вычисления
    """
    tokens = _tokenize(expression)
    _validate(tokens)
    tokens = _merge_unary_signs(tokens)
    rpn_tokens = _to_rpn(tokens)
    return _calculate_rpn(rpn_tokens)
