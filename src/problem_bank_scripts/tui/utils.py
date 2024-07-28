import json
import pathlib
import typing


def apply_indent(lines: list[str], indent: str = " " * 8) -> list[str]:
    return [indent + x for x in lines]


def string_is_numeric(s: str) -> bool:
    return s.lstrip("-").replace(".", "", 1).isdigit()


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
    with open(filename, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def write_file(data: str, filename: str | pathlib.Path = "saved.json") -> None:
    with open(filename, "w") as f:
        f.write(data)


def read_json(filename: str | pathlib.Path = "saved.json") -> typing.Any:
    with open(filename) as f:
        return json.load(f)


def split_comma(text: str) -> list[str]:
    return [x.strip() for x in text.split(",") if x.strip()]
