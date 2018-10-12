def int_input(min_val=None, max_val=None, description="",
              min_error_message="default",
              max_error_message="default",
              value_error_message="default"):
    """
    Read a string from standard input. And transform a string integer.
    If integer is smaller than min_val or integer is bigger than max_val or a string is not integer,
    read a string from standard input again.

    Parameters
    ----------
    min_val : int
        Minimum value (inclued).
    max_val : int
        Maximum value (inclued).
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

    Returns
    -------
    input_int : int
        Input value.
    """
    while True:
        inputs = input(description)
        try:
            inputs_int = int(inputs)
            if min_val is not None and inputs_int < min_val:
                if min_error_message == "default":
                    print("Input value should be bigger than or equal {}.".format(min_val))
                elif min_error_message:
                    print(min_error_message)
                continue

            if max_val is not None and inputs_int > max_val:
                if max_error_message == "default":
                    print("Input value should be smaller than or equal {}.".format(max_val))
                elif max_error_message:
                    print(max_error_message)
                continue

            return inputs_int
        except ValueError:
            if value_error_message == "default":
                print("Input value should be integer")
            elif value_error_message:
                print(value_error_message)
            continue
