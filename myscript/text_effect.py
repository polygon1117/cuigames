from time import sleep
import sys


def type_print(s, interval=0.1, end="\n"):
    for c in s:
        print(c, end="")
        sys.stdout.flush()
        sleep(interval)
    print(end=end)
