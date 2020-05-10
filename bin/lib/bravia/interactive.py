import sys

from . import keyboard
from . import server
from . import command
from .common import printerr

def main():
    server.setupAccess()
    print("Interactive mode")
    print("Press Escape or Q to exit")
    keyBoard = keyboard.KeyBoard()
    commandTable = {
        'up': 'up',
        'down': 'down',
        'left': 'left',
        'right': 'right',
        'home': 'home',
        'enter': 'dpadCenter',
        'backspace': 'exit',
        '-': 'volumeDown',
        '+': 'volumeUp',
        '1': 'hdmi1',
        '2': 'hdmi2',
        '3': 'hdmi3',
        '4': 'hdmi4'
    }
    while True:
        c = keyBoard()
        sys.stdout.write("\033[K")
        print(f'Pressed {c}', end = "\r")
        if c == 'escape' or c == 'q':
            print()
            return
        if c in commandTable:
            command.command(commandTable[c])
