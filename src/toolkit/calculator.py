
from src.constants import OPERATORS, PRIORITY
from toolkit.errors import ValidationError

def tokenize(expression: str) -> list:
    for operator in OPERATORS:
        expression = expression.replace(operator, f" {operator} ")

    expression = expression.split()

    if expression[0] == "-":
        combined = "-" + expression[1]
        expression[0:2] = [combined]
    elif expression[0] == "+":
        expression.remove(expression[0])

    return expression

def validate(expression: list[str]) -> bool:
    if not expression: raise ValidationError("Выражение не должно быть пустым", "empty_expression")

    expecting_number = True
    is_allowed = True

    for token in expression:
        if expecting_number:
            if token in ("+", "-"):
                if not is_allowed:
                    raise ValidationError("Два оператора стоят подряд", "repeated_unary_sign")

                is_allowed = False
                continue

            try:
                float(token)
            except ValueError:
                raise ValidationError("В выражении используются недопустимые символы", "invalid_number")

            expecting_number = False
        else:
            if token not in OPERATORS:
                raise ValidationError("Между числами отсутствует оператор, или такой оператор не поддерживается",
                                      "missing_operator")

            expecting_number = True

    if expecting_number: raise ValidationError("Выражение не должно заканчиваться на оператор",
                                               "missing_operand")

    return True

def to_rpn(expression: list[str]) -> list[str]:
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

def apply_operator(a: float, b: float, operator: str) -> float:
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
            raise ValidationError("Оператор не поддерживается", 'undefined_operator')


def calculate(rpn_tokens: list[str]) -> float:
    stack = []

    for token in rpn_tokens:
        try:
            float(token)
            stack.append(token)
        except ValueError:
            if len(stack) < 2:
                raise ValidationError("Неверно составленный RPN (не хватает операндов)", error_code="invalid_rpn")

            num2 = float(stack.pop())
            num1 = float(stack.pop())

            stack.append(apply_operator(num1, num2, token))

    if len(stack) != 1:
        raise ValidationError("Неверно составленный RPN (в RPN должно остаться одно значение)", error_code="invalid_rpn")

    return stack[0]
