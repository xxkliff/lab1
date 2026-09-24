

LENGTH_GROUP: dict = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

WEIGHT_GROUP: dict = {
    "g": 1.0,
    "kg": 1000.0,
}

TEMPERATURE_GROUP: dict = {
    "c": (lambda c: c + 273.15, lambda k: k - 273.15),
    "k": (lambda k: k, lambda k: k),
    "f": (lambda f: (f - 32)*5/9 + 273.15, lambda k: (k - 273.15)*9/5 + 32)
}

GROUPS: list = [LENGTH_GROUP, TEMPERATURE_GROUP, WEIGHT_GROUP]

