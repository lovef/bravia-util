#!/usr/bin/env python3

import listCommands
import server
import sys

def main(commands):
    server.setupAccess(False)
    commandCodes = listCommands.getCommands()
    for command in commands:
        if command in commandCodes:
            code = commandCodes[command] if command in commandCodes else None
            server.command(command, code)
        else:
            print(command, "Command not found")

if __name__ == '__main__':
    main(sys.argv[1:])
