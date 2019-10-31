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
