
import re

def parse_time(value):
    if value is None:
        return None

    if type(value) in [int, float]:
        if value >= 0:
            return value
        else:
            return None

    value = value.strip()
    if value == "":
        return None
        
    if not re.match(r"\d+[smhdw]", value):
        raise ValueError("The time delta %s does not match the regex \\d+[smhdw]"%value)
    
    number = int(value[:-1])
    unit = value[-1]

    if unit == "s":
        return number
    elif unit == "m":
        return number * 60
    elif unit == "h":
        return number * 60 * 60
    elif unit == "d":
        return number * 60 * 60 * 24
    elif unit == "w":
        return number * 60 * 60 * 24 * 7