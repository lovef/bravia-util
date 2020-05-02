#!/usr/bin/env python3

import sys
import server
import config

def main(toggle):
    on = server.powerStatus() == "active"
    if not on:
        powerOn()
        setInput()
        return True

    preset = config.readPreset()
    if preset and preset != server.currentInput():
        setInput(preset)
        return True

    if toggle:
        powerOff()
        return True

    return False

def powerOn():
    server.command("wakeUp", "AAAAAQAAAAEAAAAuAw==")
    server.command("wakeUp", "AAAAAQAAAAEAAAAuAw==")

def powerOff():
    server.command("powerOff", "AAAAAQAAAAEAAAAvAw==")
    server.command("powerOff", "AAAAAQAAAAEAAAAvAw==")

def setInput(preset = config.readPreset()):
    if preset:
        server.currentInput(preset)


if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) > 1 else None
    shouldExit = main(command == "toggle")
    print("true" if shouldExit else "false")
