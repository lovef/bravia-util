import subprocess
import re
import urllib.request
import json

from . import config

ipPatternString = '([0-9]{1,3}\\.){3}[0-9]{1,3}'

def main():
    arpLines = readArpTable()

    selected = -1
    for i, match in enumerate(arpLines):
        (ip, mac) = match
        sony = re.match("70[-:]26[-:]0?5", mac)
        prefix = "Sony" if sony else ""
        if sony:
            selected = i
        print(f'{i:2}: {prefix:5} {mac} {ip}')

    ipPattern = re.compile(ipPatternString)
    ip = ""
    while True:
        if selected >= 0 and selected <= len(arpLines):
            (ip, mac) = arpLines[selected]
        if ipPattern.match(ip):
            print(        "Selected          ", ip, getInfo(ip))
        else:
            print("No IP selected")
        userInput = input("Select other (no): ")
        if ipPattern.match(userInput):
            ip = userInput
            selected = -1
        elif userInput:
            ip = ""
            try:
                selected = int(userInput)
            except:
                selected = -1
        else:
            break

    if not ipPattern.match(ip):
        raise NameError('Could not select IP')

    print(f'Selected {ip}')
    config.writeIp(ip)
    return ip

def readArpTable():
    arp = subprocess.check_output("arp -a", shell=True).decode("utf-8")
    arpMatches = re.findall('((\\d{1,3}\\.){3}\\d{1,3})\\D.*?(([\\da-fA-F]{1,2}[-:]){5}[\\da-fA-F]{1,2})', arp)
    return list(map(
        lambda m: (m[0], m[2]),
        arpMatches))

def getInfo(ip):
    try:
        data = {
            "method": "getInterfaceInformation",
            "id": 33,
            "params": [],
            "version": "1.0"
        }
        contents = urllib.request.urlopen(f"http://{ip}/sony/system", json.dumps(data).encode("utf-8")) \
            .read()
        result = json.loads(contents)['result'][0]
        return f"{result['productName']} {result['modelName']}"
    except:
        return "Could not read server info"
