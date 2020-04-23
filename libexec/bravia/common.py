import sys
import datetime

def timestamp():
    return datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')

def printerr(*args, prefix = timestamp(), **kwargs):
    if prefix is None:
        print(*args, file=sys.stderr, **kwargs)
    else:
        print(prefix, *args, file=sys.stderr, **kwargs)
