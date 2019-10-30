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
        open_tag = "<%s>" % tag
        close_tag = "</%s>" % tag
        print(string)
        print(open_tag)
        print(close_tag)
        print(string.index(open_tag))
        print(string.index(close_tag))
        content = string[string.index(open_tag) + len(open_tag):string.index(close_tag)]
        remainder = string[string.index(close_tag) + len(close_tag):]
        return content, remainder
    except Exception:
        return None, None
