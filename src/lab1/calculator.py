"""Base calculator"""


def calc(a, b, operator):
    try:
        a = float(a)
        b = float(b)
    except Exception:
        return "Error"
    if operator in "/%" and b == 0:
        return "Error"
    elif operator == "+":
        return int(a + b) if a + b == int(a + b) else a + b
    elif operator == "-":
        return int(a - b) if a - b == int(a - b) else a - b
    elif operator == "*":
        return int(a * b) if a * b == int(a * b) else a * b
    elif operator == "/":
        return int(a / b) if a / b == int(a / b) else a / b
    else:
        return "Error"
