import json

from . import server
from . import config
from .common import printerr
from .common import color

def setPreset(preset):
    print("set preset", preset)
    config.writePreset(preset)

def listInputs():
    server.setup()
    response = server.get('sony/avContent', {
        "method": "getCurrentExternalInputsStatus",
        "id": 105,
        "params": [],
        "version": "1.1"
    })

    inputs = response['result'][0]
    inputs = sorted(inputs, key=lambda i: i['connection'], reverse=True)
    preset = config.readPreset()
    print("Commands to change preset:")
    for inputDef in inputs:
        label = inputDef['label']
        title = inputDef['title']
        connection = inputDef['connection']
        status = inputDef['status'] == 'true'
        activeStr = color.BRIGHT_GREEN if status else "" if connection else color.GREY
        uri = inputDef['uri']
        quotedUri = f"'{uri}'"

        inputString = f"  {activeStr}bravia --input {quotedUri:50} # {label:2} {title} {color.END}"
        if preset == uri:
            preset = inputString
        else:
            print(inputString)

    print("Current preset")
    print(preset)
