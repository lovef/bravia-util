import sys
import datetime

class color:
    END       = '\33[0m'
    BOLD      = '\33[1m'
    ITALIC    = '\33[3m'
    UNDERLINE = '\33[4m'
    BLINK     = '\33[5m'
    BLINK2    = '\33[6m'
    SELECTED  = '\33[7m'

    BLACK  = '\33[30m'
    RED    = '\33[31m'
    GREEN  = '\33[32m'
    YELLOW = '\33[33m'
    BLUE   = '\33[34m'
    VIOLET = '\33[35m'
    CYAN   = '\33[36m'
    WHITE  = '\33[37m'

    GREY          = '\33[90m'
    BRIGHT_RED    = '\33[91m'
    BRIGHT_GREEN  = '\33[92m'
    BRIGHT_YELLOW = '\33[93m'
    BRIGHT_BLUE   = '\33[94m'
    BRIGHT_VIOLET = '\33[95m'
    BRIGHT_CYAN   = '\33[96m'
    BRIGHT_WHITE  = '\33[97m'

    class bg:
        BLACK  = '\33[40m'
        RED    = '\33[41m'
        GREEN  = '\33[42m'
        YELLOW = '\33[43m'
        BLUE   = '\33[44m'
        VIOLET = '\33[45m'
        CYAN   = '\33[46m'
        WHITE  = '\33[47m'

        GREY          = '\33[100m'
        BRIGHT_RED    = '\33[101m'
        BRIGHT_GREEN  = '\33[102m'
        BRIGHT_YELLOW = '\33[103m'
        BRIGHT_BLUE   = '\33[104m'
        BRIGHT_VIOLET = '\33[105m'
        BRIGHT_CYAN   = '\33[106m'
        BRIGHT_WHITE  = '\33[107m'

def timestamp():
    return color.GREY + datetime.datetime.now().isoformat(sep=' ', timespec='milliseconds') + color.END

def printerr(*args, prefix = timestamp(), **kwargs):
    if prefix is None:
        print(*args, file=sys.stderr, **kwargs)
    else:
        print(prefix, *args, file=sys.stderr, **kwargs)
