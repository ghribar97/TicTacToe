def is_string(val):
    return isinstance(val, str)


def is_int(val):
    return isinstance(val, int)


def is_float(val):
    return isinstance(val, float)


def is_number(val):
    """
    Returns true, if val is float or integer, else throws a ValueError.
    :param val: primitive type
    :return:
    """
    if is_int(val) or is_float(val):
        return True
    raise ValueError(str(val) + " is not a number!")


def are_numbers(val):
    """
    Returns true, if all of the elements in the list are integers or floats, else throws a ValueError.
    :param val: list of primitive types
    :return:
    """
    for value in val:
        if not is_number(value):
            return False
    return True


def remove_key(dictionary, key):
    if isinstance(dictionary, dict):
        new = dict(dictionary)
        del new[key]
        return new
