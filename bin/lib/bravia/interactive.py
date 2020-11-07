import sys

from . import keyboard
from . import server
from . import command
from .common import printerr
from .input import listInputs

def main():
    server.setupAccess()
    print("Interactive mode")
    print("Press Escape or Q to exit, type ? to list commands")
    keyBoard = keyboard.KeyBoard()
    commandTable = {
        '?': 'list commands',
        'i': 'list inputs',
        's': 'status',
        'up': 'up',
        'down': 'down',
        'left': 'left',
        'right': 'right',
        'home': 'home',
        'delete': 'tvPower',
        'p': 'picOff',
        'end': 'turn off screen',
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
        elif c == '?':
            print("Command table:")
            for e in commandTable:
                print(f" {e:10} {commandTable[e]}")
        elif c == 's':
            print(server.powerStatus())
            print(server.powerSavingMode())
        elif c == 'end':
            server.turnOffScreen()
        elif c == 'i':
            listInputs()
        elif c in commandTable:
            command.command(commandTable[c])
