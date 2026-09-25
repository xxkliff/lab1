
from typing import Callable, Dict, Tuple

OPERATORS: tuple[str, ...] = ("+", "-", "*", "/", "//", "%")

PRIORITY: dict[str, int] = {"+": 2,
                            "-": 2,
                            "*": 3,
                            "/": 3,
                            "//": 3,
                            "%": 3
}

LENGTH_GROUP: dict[str, float] = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

WEIGHT_GROUP: dict[str, float] = {
    "g": 1.0,
    "kg": 1000.0,
}

TEMPERATURE_GROUP: Dict[str, Tuple[Callable[[float], float], Callable[[float], float]]]= {
    "c": (lambda c: c + 273.15, lambda k: k - 273.15),
    "k": (lambda k: k, lambda k: k),
    "f": (lambda f: (f - 32)*5/9 + 273.15, lambda k: (k - 273.15)*9/5 + 32)
}

GROUPS: list[Dict] = [LENGTH_GROUP, TEMPERATURE_GROUP, WEIGHT_GROUP]

