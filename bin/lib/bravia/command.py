import sys

from . import listCommands
from . import server

commandCodes = None

def setup():
    global commandCodes
    server.setupAccess()
    if not commandCodes:
        commandCodes = listCommands.getCommands()

def command(command):
    setup()
    if command in commandCodes:
        code = commandCodes[command] if command in commandCodes else None
        server.command(command, code)
    else:
        print(command, "Command not found")

def main(commands):
    setup()
    for c in commands:
        command(c)
