#!/usr/bin/env python3

import sys

# https://stackoverflow.com/a/510364/1020871
class KeyBoard:
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys
        self.keys = {
            b'\x7f': 'backspace',
            b'\r': 'enter',
            b'\x1b': {
                b'\x1b': 'escape',
                b'[': {
                    b'A': 'up',
                    b'B': 'down',
                    b'D': 'left',
                    b'C': 'right',
                    b'O': 'end',
                    b'H': 'home',
                    b'F': 'end',
                    b'3': {b'~': 'delete'},
                    b'5': {b'~': 'pageUp'},
                    b'6': {b'~': 'pageDown'}
                }
            }
        }

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())

            keys = self.keys
            last = sys.stdin.read(1).encode()
            allBytes = last
            while last in keys:
                resolved = keys[last]
                if type(resolved) is str:
                    return resolved
                keys = resolved
                last = sys.stdin.read(1).encode()
                allBytes = allBytes + last

            try:
                return allBytes.decode()
            except:
                return allBytes
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


class _GetchWindows:
    def __init__(self):
        import msvcrt
        self.keys = windowsKeys = {
            b'\x1b': 'escape',
            b'\x08': 'backspace',
            b'\x1a': 'pause',
            b'\r': 'enter',
            b'\xe0': {
                b'H': 'up',
                b'P': 'down',
                b'K': 'left',
                b'M': 'right',
                b'M': 'right',
                b'R': 'insert',
                b'S': 'delete',
                b'G': 'home',
                b'O': 'end',
                b'I': 'pageUp',
                b'Q': 'pageDown',
            }
        }

    def __call__(self):
        import msvcrt

        keys = self.keys
        last = msvcrt.getch()
        allBytes = last
        while last in keys:
            resolved = keys[last]
            if type(resolved) is str:
                return resolved
            keys = resolved
            last = msvcrt.getch()
            allBytes = allBytes + last

        try:
            return allBytes.decode()
        except:
            return allBytes

def main():
    print("Press Escape to exit")
    keyBoard = KeyBoard()
    while True:
        c = keyBoard()
        sys.stdout.write("\033[K")
        print(f'Pressed {c}', end = "\r")
        if c == 'escape':
            return

if __name__ == '__main__':
    main()
    print()
