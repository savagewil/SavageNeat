from typing import List, Tuple
import re


def divide_whole(whole: int, fractions: List[float]):
    top = max(fractions)
    index = fractions.index(top)
    if top >= 1.0:
        chunk = int(top)
        fractions[index] -= chunk
    else:
        chunk = 1
        fractions[index] = 0
    whole -= chunk
    if whole > 0:
        result = divide_whole(whole, fractions)
    else:
        result = [0 for fraction in fractions]
    result[index] += chunk
    return result


def surround_tag(tag, string):
    return "<%s>%s</%s>" % (tag, string, tag)


def remove_tag(tag, string):
    try:
        open_start, open_end, close_start, close_end = find_outside_tags(tag, string)
        content = string[open_end: close_start]
        remainder = string[close_end:]
        return content, remainder
    except StopIteration:
        return None, None


def find_outside_tags(tag, string) -> Tuple[int, int, int, int]:
    open_tag = "<%s>" % tag
    close_tag = "</%s>" % tag
    opens = re.finditer(open_tag, string)
    closes = re.finditer(close_tag, string)
    open = 1
    open_tag_real = opens.__next__()

    try:
        open_tag_curr = opens.__next__()
    except StopIteration:
        open_tag_curr = None
    close_tag_curr = closes.__next__()
    while open > 0:
        if open_tag_curr is not None and open_tag_curr.start() < close_tag_curr.start():
            open += 1
            try:
                open_tag_curr = opens.__next__()
            except StopIteration:
                open_tag_curr = None
        else:
            open -= 1
            if open > 0:
                close_tag_curr = closes.__next__()

    return open_tag_real.start(), open_tag_real.end(), close_tag_curr.start(), close_tag_curr.end()


def save_dict(dictionary: dict) -> str:
    dict_string = ""
    for key, val in dictionary.items():
        dict_string += surround_tag("key", str(key))
        dict_string += surround_tag("val", str(val))
    return dict_string


def load_dict(dictionary_string, key_class, value_class) -> dict:
    dictionary = {}
    while dictionary_string:
        key_str, dictionary_string = remove_tag("key", dictionary_string)
        val_str, dictionary_string = remove_tag("val", dictionary_string)

        if hasattr(key_class, 'load') and callable(getattr(key_class, 'load')):
            key = key_class.load(key_str)
        else:
            key = key_class(key_str)

        if hasattr(value_class, 'load') and callable(getattr(value_class, 'load')):
            val = value_class.load(val_str)
        else:
            val = value_class(val_str)
        dictionary[key] = val
    return dictionary


def save_list(list_: list) -> str:
    list_string = ""
    for item in list_:
        list_string += surround_tag("item", str(item))
    return list_string


def load_list(list_string, item_class) -> list:
    list_ = []
    while list_string:
        item_str, list_string = remove_tag("item", list_string)

        if hasattr(item_class, 'load') and callable(getattr(item_class, 'load')):
            item = item_class.load(item_str)
        else:
            item = item_class(item_str)

        list_.append(item)
    return list_
