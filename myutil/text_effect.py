from time import sleep
import sys


def type_print(s, interval=0.1, end="\n"):
    """
    Print string like type.

    Parameters
    ----------
    s : str
        Print string
    interval : float
        Type interval (second)
    end : str
        Like print(s, end)

    Returns
    -------
    None
    
    """
    for c in s:
        print(c, end="")
        sys.stdout.flush()
        sleep(interval)
    print(end=end)
