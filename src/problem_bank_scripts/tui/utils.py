import json
import pathlib
import typing

def remove_excess_newlines(s: str) -> str:
    while "\n\n\n" in s:
        s = s.replace("\n\n\n", "\n\n")
    return s

def apply_indent(lines: list[str], indent: str = " " * 8) -> list[str]:
    return [indent + x for x in lines]

def remove_leading_non_numeric(s: str) -> str:
    while s and s[0] not in "0123456789":
        s = s[1:]
    return s

def remove_trailing_non_numeric(s: str) -> str:
    while s and s[-1] not in "0123456789":
        s = s[:-1]
    return s

def remove_edge_non_numeric(s: str) -> str:
    return remove_leading_non_numeric(remove_trailing_non_numeric(s))

def string_is_numeric(s: str) -> bool:
    return s.lstrip("-").replace(".", "", 1).isdigit()

def string_is_approx_numeric(s: str) -> bool:
    s = remove_edge_non_numeric(s)
    return s.replace(".", "", 1).isdigit()

def string_is_number_range(s: str) -> bool:
    split: list[str] = s.split('-')
    return len(split) == 2 and string_is_numeric(split[0].strip()) and string_is_numeric(split[1].strip())

def string_is_int(s: str) -> bool:
    if s and s[0] in {'-', '+'}:
        return s[1:].isdigit()
    return s.isdigit()

def string_num_digits_after_decimal(s: str | float) -> int:
    s = str(s)
    s = remove_trailing_non_numeric(s)
    if "." not in s:
        return 0
    return len(s.split(".")[1])

def get_number_suffix(s: str) -> str:
    s = s.strip()[-1:]
    if s.isdigit():
        return ""
    return s

possible_prefixes = ["(", "[", "{", r"\$", "|"]
possible_suffixes = [".", ",", "?", "!", ":", ";", ")", "]", "}", "\\%", "%", "|", "\\"]


def handle_word(wordV: str, params_dict: dict) -> str:
    prefix = ""
    suffix = ""
    word = wordV
    for pre in possible_prefixes + possible_prefixes:
        if word.startswith(pre):
            word = word[len(pre):]  # fmt: skip
            prefix += pre
    for suf in possible_suffixes + possible_suffixes:
        if word.endswith(suf):
            word = word[:-len(suf)]  # fmt: skip
            suffix = suf + suffix
    word = word.replace(",", "")  # ex. 1,000,000

    for value, param_name in params_dict.items():
        if word == value or (
            string_is_numeric(word) and isinstance(value, float) and float(word) == value
        ):
            if string_is_numeric(word) and not ("$" in prefix or "$" in suffix):
                return f'{prefix}${{{{ params.{param_name.replace("_", ".")} }}}}${suffix}'
            return f'{prefix}{{{{ params.{param_name.replace("_", ".")} }}}}{suffix}'
    return wordV


# Used to apply params to solutions
def apply_params_to_str(paragraph: str, params_dict: dict) -> str:
    # TODO: handle negative numbers

    words = paragraph.split(" ")
    # re.split(' |/',paragraph)
    for i, word in enumerate(words):
        if len(word) == 0:
            continue
        # TODO: split word by '\\' too
        arr = [handle_word(w, params_dict) for w in word.split("/")]
        words[i] = "/".join(arr)

    return " ".join(words)


def count_decimal_places(num: float) -> int:
    """number of digits after decimal point"""
    return str(num)[::-1].find(".")


def write_json(data: dict, filename: str | pathlib.Path = "saved.json") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def write_file(data: str, filename: str | pathlib.Path = "saved.json") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)


def read_json(filename: str | pathlib.Path = "saved.json") -> typing.Any:
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def split_comma(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]
