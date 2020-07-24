def is_order_of_strings_in_string_correct(string1, string2, whole_string):
    """
    Returns True if String 1 is before String 2 in a given string and False otherwise.

    :param string1: The substring supposed to be first in the string.
    :param string2: The substring supposed to be second in the string.
    :param whole_string: The whole string containing both substrings.
    :return: True if String 1 before String 2, False otherwise
    """

    if type(string1) != type(whole_string) or type(string2) != type(whole_string):
        if not isinstance(string1, bytes): string1 = bytes(string1, encoding='ascii')
        if not isinstance(string2, bytes): string2 = bytes(string2, encoding='ascii')
        if not isinstance(whole_string, bytes): whole_string = bytes(whole_string, encoding='ascii')

    if string1 not in whole_string:
        raise ValueError('Whole_string doesn\'t contain string 1')
    if string2 not in whole_string:
        raise ValueError('Whole_string doesn\'t contain string 2')

    begin_string_1 = whole_string.find(string1)
    begin_string_2 = whole_string.find(string2)

    return_value = True if begin_string_1 < begin_string_2 else False
    return return_value