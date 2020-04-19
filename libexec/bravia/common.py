import sys
import datetime

def printerr(*args, **kwargs):
    now = datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds')
    print(now, *args, file=sys.stderr, **kwargs)
