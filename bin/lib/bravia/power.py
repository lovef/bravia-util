import sys

from . import server
from . import config
from .common import printerr

def main(toggle):
    printerr("--- power ---")
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
