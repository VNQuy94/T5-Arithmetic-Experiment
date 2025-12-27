from num2words import num2words

def format_decimal(n):
    return str(n)

def format_character(n):
    return " ".join(str(n))

def format_fixed_character(n, max_digits):
    if n < 0:
        sign = "- "
        n = abs(n)
    else:
        sign = ""
        
    s = str(n)
    pad = max_digits - len(s)
    if pad > 0:
        s = "0" * pad + s
    return sign + " ".join(s)

def format_underscore(n):
    if n < 0:
        return "-" + "_".join(str(abs(n)))
    return "_".join(str(n))

def format_words(n):
    return num2words(n).replace("-", " ").replace(",", "")

def format_10_based(n):
    if n < 0:
        sign = "- "
        n = abs(n)
    else:
        sign = ""
        
    s = str(n)
    length = len(s)
    parts = []
    for i, digit in enumerate(s):
        power = length - 1 - i
        if power > 0:
            parts.append(f"{digit} {10**power}")
        else:
            parts.append(f"{digit}")
    return sign + " ".join(parts)

def format_10e_based(n):
    if n < 0:
        sign = "- "
        n = abs(n)
    else:
        sign = ""

    s = str(n)
    length = len(s)
    parts = []
    for i, digit in enumerate(s):
        power = length - 1 - i
        parts.append(f"{digit} 10e{power}")
    return sign + " ".join(parts)

def apply_format(n, fmt, max_digits):
    if fmt == "decimal":
        return format_decimal(n)
    elif fmt == "character":
        return format_character(n)
    elif fmt == "fixed-character":
        return format_fixed_character(n, max_digits)
    elif fmt == "underscore":
        return format_underscore(n)
    elif fmt == "words":
        return format_words(n)
    elif fmt == "10-based":
        return format_10_based(n)
    elif fmt == "10e-based":
        return format_10e_based(n)
    else:
        raise ValueError(f"Unknown format: {fmt}")

def invert_string(text, fmt):
    prefix = ""
    if text.startswith("- "):
        prefix = "- "
        text = text[2:]
    elif text.startswith("-"):
        prefix = "-"
        text = text[1:]
    
    if fmt == "decimal":
        return prefix + text[::-1]
    elif fmt == "character":
        return prefix + " ".join(text.split(" ")[::-1])
    elif fmt == "fixed-character":
        return prefix + " ".join(text.split(" ")[::-1])
    elif fmt == "underscore":
        return prefix + "_".join(text.split("_")[::-1])
    elif fmt == "words":
        return prefix + " ".join(text.split(" ")[::-1])
        
    elif fmt == "10-based":
        grouped_10 = text.split(" ")[::-1]

        length = len(grouped_10)
        for i in range(1, length - 1, 2):
            if grouped_10[i] != "0" and int(grouped_10[i]) % 10 == 0:
                grouped_10[i], grouped_10[i + 1] = grouped_10[i + 1], grouped_10[i]

        return prefix + " ".join(grouped_10)

    elif fmt == "10e-based":
        grouped_10e = text.split(" ")[::-1]

        length = len(grouped_10e)
        for i in range(0, length - 1, 2):
            if grouped_10e[i] != "0" and grouped_10e[i].startswith("10e"):
                grouped_10e[i], grouped_10e[i + 1] = grouped_10e[i + 1], grouped_10e[i]

        return prefix + " ".join(grouped_10e)

    return prefix + text[::-1]
