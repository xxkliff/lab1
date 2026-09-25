
from toolkit.constants import OPERATORS, PRIORITY
from toolkit.errors import ValidationError


def _tokenize(expression: str) -> list:
    tokens = []
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

def _validate(tokens: list[str]) -> bool:
    if not tokens: raise ValidationError("выражение пустое или некорректно.", "empty_expression")

    expecting_number = True

    for i, token in enumerate(tokens):
        if expecting_number:
            if token in ("+", "-"):
                next_token = tokens[i + 1] if i + 1 < len(tokens) else None

                if next_token is None:
                    raise ValidationError("выражение не может заканчиваться на оператор.",
                                            "missing_operand")

                if next_token in OPERATORS:
                    raise ValidationError("несколько операторав не могут стоять подряд.","repeated_unary_sign")

                continue

            if token in OPERATORS:
                raise ValidationError("несколько операторав не могут стоять подряд.","repeated_unary_sign")
            try:
                float(token)
            except ValueError:
                raise ValidationError("в выражении используются недопустимые символы.", "invalid_number")

            expecting_number = False
        else:
            if token not in OPERATORS:
                if not token.isdigit():
                    raise ValidationError("в выражении используются недопустимые символы.", "invalid_number")

                raise ValidationError("между числами отсутствует оператор.", "missing_operator")

            expecting_number = True

    if expecting_number: raise ValidationError("выражение не может заканчиваться на оператор.",
                                               "missing_operand")

    return True

def _merge_unary_signs(tokens: list[str]) -> list[str]:
    output = []
    i = 0

    while i < len(tokens):
        merge_token = tokens[i]
        prev_token = tokens[i - 1] if i > 0 else ""
        next_token = tokens[i + 1] if i + 1 < len(tokens) else ""

        if merge_token.isspace():
            i += 1
            continue

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
    stack = []
    output = []

    for token in expression:
        try :
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


def _calculate_rpn(rpn_tokens: list[str]) -> float:
    stack = []

    for token in rpn_tokens:
        try:
            float(token)
            stack.append(float(token))
        except ValueError:
            if len(stack) < 2:
                raise RuntimeError("Неверно составленный RPN (не хватает операндов).")

            num2 = float(stack.pop())
            num1 = float(stack.pop())

            stack.append(_apply_operator(num1, num2, token))

    if len(stack) != 1:
        raise RuntimeError("Неверно составленный RPN (в RPN должно остаться одно значение).")

    return float(stack[0])

def evaluate(expression: str) -> float:
    tokens = _tokenize(expression)
    _validate(tokens)
    tokens = _merge_unary_signs(tokens)
    rpn_tokens = _to_rpn(tokens)
    return _calculate_rpn(rpn_tokens)
