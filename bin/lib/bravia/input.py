#!/usr/bin/env python3

import server
import json
from common import printerr

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

def main():
    server.setup(False)
    response = server.get('sony/avContent', {
        "method": "getCurrentExternalInputsStatus",
        "id": 105,
        "params": [],
        "version": "1.1"
    })

    inputs = response['result'][0]
    inputs = sorted(inputs, key=lambda i: i['connection'], reverse=True)
    print("Commands to change preset:")
    for inputDef in inputs:
        label = inputDef['label']
        title = inputDef['title']
        connection = inputDef['connection']
        status = inputDef['status'] == 'true'
        activeStr = color.BRIGHT_GREEN if status else "" if connection else color.GREY
        uri = inputDef['uri']
        quotedUri = f"'{uri}'"

        print(f"  {activeStr}bravia --input {quotedUri:50} # {label:2} {title} {color.END}")

if __name__ == '__main__':
    main()
