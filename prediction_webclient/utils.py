def convert_to_value_label(data: list):
    return [{"value": value, "label": label} for value, label in data ]

def try_parse_int(value, default=None):
    try:
        return int(value)
    except:
        return default