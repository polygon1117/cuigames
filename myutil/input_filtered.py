def _print_error_message(error_message, default_message):
    if error_message == "default":
        print(default_message)
    elif error_message:
        print(error_message)


def _filter_inputs_by_min(inputs_int, min_val, error_message="default"):
    default_message = "Input value should be bigger\
     than or equal {}.".format(min_val)

    if inputs_int is None:
        return None

    if min_val is not None and inputs_int < min_val:
        _print_error_message(error_message=error_message,
                             default_message=default_message)
        return None
    return inputs_int


def _filter_inputs_by_max(inputs_int, max_val, error_message="default"):
    default_message = "Input value should be smaller\
     than or equal {}.".format(max_val)

    if inputs_int is None:
        return None

    if max_val is not None and inputs_int > max_val:
        _print_error_message(error_message=error_message,
                             default_message=default_message)
        return None
    return inputs_int


def _split_and_filter_inputs_by_nargs(inputs, nargs, splitter=None,
                                      error_message="default"):
    default_message = "Input value require {} integers\
     splited by {}.".format(nargs, splitter)
    if nargs == 1:
        return [inputs]

    if splitter is None:
        splited = inputs.split()
    else:
        splited = inputs.split(splitter)

    if len(splited) == nargs:
        return splited
    else:
        _print_error_message(error_message=error_message,
                             default_message=default_message)
        return None


def int_input(min_val=None, max_val=None, nargs=1, splitter=None,
              description="",
              min_error_message="default",
              max_error_message="default",
              value_error_message="default",
              nargs_error_message="default"):
    """
    Read a string from standard input. And transform a string integer.

    If integer is smaller than min_val or integer is bigger than max_val
    or a string is not integer,
    read a string from standard input again.

    Parameters
    ----------
    min_val : int
        Minimum value (inclued).
    max_val : int
        Maximum value (inclued).
    nargs : int
        Number of integers.
    splitter : string
        Split input value by this if nargs is not 1.
    description : string
        Use like input(description).
    min_error_message : string
        Print this if input value is smaller than min_val.
        If don't want to print message, set None.
    max_error_message : string
        Print this if input value is bigger than max_val.
        If don't want to print message, set None.
    value_error_message : string
        Print this if input value cannot be transformed to integer.
        If don't want to print message, set None.
    nargs_error_message : string
        Print this if length of input value splited by splitter is not nargs.
        If don't want to print message, setNone.

    Returns
    -------
    input_int : int or list
        If nargs is 1 return int, else return list.

    """
    def _filter_inputs_by_min_max(inputs, min_val, max_val):
        inputs_int = int(inputs)
        inputs_filtered_min = _filter_inputs_by_min(inputs_int, min_val,
                                                    min_error_message)
        inputs_filtered = _filter_inputs_by_max(inputs_filtered_min, max_val,
                                                max_error_message)
        return inputs_filtered

    while True:
        inputs = input(description)
        splited_inputs = _split_and_filter_inputs_by_nargs(inputs, nargs,
                                                           splitter,
                                                           nargs_error_message)

        ret_integers = []
        try:
            for integer in splited_inputs:
                inputs_int = _filter_inputs_by_min_max(integer,
                                                       min_val,
                                                       max_val)
                if inputs_int is None:
                    break
                ret_integers.append(inputs_int)
            else:  # Successful in for loop
                return ret_integers[0] if nargs == 1 else ret_integers
            continue  # Fail in for loop
        except ValueError:
            if value_error_message == "default":
                print("Input value should be integer")
            elif value_error_message:
                print(value_error_message)
            continue


def true_or_false_input(true_val, false_val, description="", lower=True):
    """
    Read a string from standard input. And transform into bool val.

    If input equals true_val or false_val, return True or False,
    otherwise read a string againself.

    Parameters
    ----------
    true_val : str
        True word
    false_val : str
        False word
    description : str
        Use like input(description)
    lower : bool
        Transfomr input string to lower case

    Returns
    -------
    true_or_false : bool
        True or False

    """
    while True:
        inputs = input(description)
        if lower:
            inputs = inputs.lower()

        if inputs == true_val:
            return True
        if inputs == false_val:
            return False
        else:
            print('Input {} or {}'.format(true_val, false_val))


def alphabets_input(min_length=None, max_length=None,
                    description="", filter_null=True):
    """
    Read a string from standard. And filter input by length.

    If length of input is out of defined length, read a string again.

    Parameters
    ----------
    min_length : int
        Minimum length of input. None means no minimum length.
    max_length : int
        Maximum length of input. None means no maximum length.
    description : str
        Use like input(description)
    filter_null : bool
        If return input "". If False and input equals "", read again.

    Returns
    -------
    alphabets_input : str
        Only alphabet string or "" (only if filter_null is False).

    """
    while True:
        inputs = input(description)
        if not filter_null and len(inputs) == 0:
            return ""
        if inputs.isalpha():
            if min_length is not None and len(inputs) < min_length:
                continue

            elif max_length is not None and len(inputs) > max_length:
                continue

            return inputs
        else:
            pass
