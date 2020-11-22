import urllib.request
import json
import time
import sys

from . import setup as setup_script
from . import access
from .common import printerr
from .common import color
from .responseFormatter import formatResponse
from .responseFormatter import pretty

ip = None
cookie = None

def setup(newIp=None):
    global ip
    if newIp:
        ip = newIp
    elif ip is None:
        ip = setup_script.main()

def setupAccess():
    setup()
    global cookie
    if cookie is None:
        cookie = access.main()


def get(path, jsonData, log=None, timeout=5):
    setup()
    data = json.dumps(jsonData).encode("utf-8")
    req = urllib.request.Request(f"http://{ip}/sony/{path}", data)
    response = sendRequest(req, log if log else "GET " + path, timeout=timeout)
    return formatResponse(response.read())


def getWithAuth(path, jsonData, log=None):
    setupAccess()
    data = json.dumps(jsonData).encode("utf-8")
    headers = {"Cookie": cookie}
    req = urllib.request.Request(f"http://{ip}/sony/{path}", data, headers)
    response = sendRequest(req, log if log else "GET with auth " + path)
    return formatResponse(response.read())


def command(command, code):
    setupAccess()
    data = f"""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
        <s:Body>
            <u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">
                <IRCCCode>{code}</IRCCCode>
            </u:X_SendIRCC>
        </s:Body>
    </s:Envelope>""".encode("ascii")
    headers = {
        "Cookie": cookie,
        "SOAPACTION": '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"'
    }
    req = urllib.request.Request(
        f"http://{ip}/sony/ircc", data, headers, method="POST")
    response = sendRequest(
        req, f"IRCC {color.BRIGHT_GREEN}{command} {color.GREY}{code}{color.END}")


def requestCookie(url, data, auth=None):
    headers = {"Authorization": auth} if auth is not None else {}
    req = urllib.request.Request(url, data, headers)
    response = sendRequest(req, "Request cookie")
    return response.info()['Set-Cookie']


def sendRequest(request, log, timeout=5):
    statusString = "failed"
    try:
        printerr(log, end=" .. ", flush=True)
        start = time.time()
        response = urllib.request.urlopen(request, timeout=timeout)
        statusString = f"{response.getcode()}"
        return response
    except urllib.error.HTTPError as e:
        statusString = f"{e.code}"
        raise
    finally:
        end = time.time()
        printerr(statusString, f"in {end - start:.3f}", prefix=None)


def currentInput(selected=None):
    if selected:
        response = getWithAuth("avContent", {
            "method": "setPlayContent",
            "id": 101,
            "params": [{"uri": selected}],
            "version": "1.0"
        }, log="Set current input")
    else:
        response = getWithAuth("avContent", {
            "method": "getPlayingContentInfo",
            "id": 103,
            "params": [],
            "version": "1.0"
        }, log="Get current input")
        try:
            return response['result'][0]['uri']
        except:
            return None


def powerStatus():
    try:
        response = get("system", {
            "method": "getPowerStatus",
            "id": 50,
            "params": [],
            "version": "1.0"
        }, log="Get power status", timeout=1)
        return response['result'][0]['status']
    except:
        return None


def turnOffScreen():
    powerSavingMode("pictureOff")


def powerSavingMode(selected=None):
    if selected:
        response = getWithAuth("system", {
            "method": "setPowerSavingMode",
            "id": 52,
            "params": [{"mode": selected}],
            "version": "1.0"
        }, log=f"Set power saving mode {selected}")
        return
    try:
        response = get("system", {
            "method": "getPowerSavingMode",
            "id": 51,
            "params": [],
            "version": "1.0"
        }, log="Get power saving mode", timeout=1)
        return response['result'][0]['mode']
    except:
        return None

def getApplicationList():
    return getWithAuth("appControl", {
        "method": "getApplicationList",
        "id": 60,
        "params": [],
        "version": "1.0"
    })

def getApplicationStatusList():
    return get("appControl", {
        "method": "getApplicationStatusList",
        "id": 55,
        "params": [],
        "version": "1.0"
    })

def getContentCount():
    return getWithAuth("avContent", {
        "method": "getContentCount",
        "id": 11,
        "params": [{"source": "extInput:hdmi"}],
        "version": "1.1"
    })

def getContentList():
    return getWithAuth("avContent", {
        "method": "getContentList",
        "id": 88,
        "params": [{
            "stIdx": 0,
            "cnt": 50,
            "uri": "extInput:hdmi"
        }],
        "version": "1.5"
    })

def getCurrentExternalInputsStatus():
    return getWithAuth("avContent", {
        "method": "getCurrentExternalInputsStatus",
        "id": 105,
        "params": [],
        "version": "1.1"
    })

def getCurrentTime():
    return get("system", {
        "method": "getCurrentTime",
        "id": 51,
        "params": [],
        "version": "1.1"
    })

def getInterfaceInformation():
    return get("system", {
        "method": "getInterfaceInformation",
        "id": 33,
        "params": [],
        "version": "1.0"
    })

def getLEDIndicatorStatus():
    return getWithAuth("system", {
        "method": "getLEDIndicatorStatus",
        "id": 45,
        "params": [],
        "version": "1.0"
    })

def getNetworkSettings():
    return getWithAuth("system", {
        "method": "getNetworkSettings",
        "id": 2,
        "params": [{"netif": "eth0"}],
        "version": "1.0"
    })

def getPlayingContentInfo():
    return getWithAuth("avContent", {
        "method": "getPlayingContentInfo",
        "id": 103,
        "params": [],
        "version": "1.0"
    })

def getPowerSavingMode():
    return getWithAuth("system", {
        "method": "getPowerSavingMode",
        "id": 51,
        "params": [],
        "version": "1.0"
    })

def getPowerStatus():
    return get("system", {
        "method": "getPowerStatus",
        "id": 50,
        "params": [],
        "version": "1.0"
    })

def getRemoteControllerInfo():
    return get("system", {
        "method": "getRemoteControllerInfo",
        "id": 54,
        "params": [],
        "version": "1.0"
    })

def getRemoteDeviceSettings():
    return get("system", {
        "method": "getRemoteDeviceSettings",
        "id": 44,
        "params": [{"target": "accessPermission"}],
        "version": "1.0"
    })

def getSchemeList():
    return get("avContent", {
        "method": "getSchemeList",
        "id": 1,
        "params": [],
        "version": "1.0"
    })

def getSoundSettings():
    return get("audio", {
        "method": "getSoundSettings",
        "id": 73,
        "params": [{"target": "outputTerminal"}],
        "version": "1.1"
    })

def getSourceList():
    return get("avContent", {
        "method": "getSourceList",
        "id": 1,
        "params": [{"scheme": "extInput"}],
        "version": "1.0"
    })

def getSpeakerSettings():
    return get("audio", {
        "method": "getSpeakerSettings",
        "id": 67,
        "params": [{"target": ""}],
        "version": "1.0"
    })

def getSupportedApiInfo():
    return get("guide", {
        "method": "getSupportedApiInfo",
        "id": 5,
        "params": [{"services": [
            "system",
            "avContent"
        ]}],
        "version": "1.0"
    })

def getSystemInformation():
    return getWithAuth("system", {
        "method": "getSystemInformation",
        "id": 33,
        "params": [],
        "version": "1.0"
    })

def getSystemSupportedFunction():
    return get("system", {
        "method": "getSystemSupportedFunction",
        "id": 55,
        "params": [],
        "version": "1.0"
    })

def getTextForm():
    return getWithAuth("appControl", {
        "method": "getTextForm",
        "id": 60,
        "params": [{}],
        "version": "1.1"
    })

def getVolumeInformation():
    return get("audio", {
        "method": "getVolumeInformation",
        "id": 33,
        "params": [],
        "version": "1.0"
    })

def getWebAppStatus():
    return getWithAuth("appControl", {
        "method": "getWebAppStatus",
        "id": 1,
        "params": [],
        "version": "1.0"
    })

def getWolMode():
    return getWithAuth("system", {
        "method": "getWolMode",
        "id": 50,
        "params": [],
        "version": "1.0"
    })

def requestReboot():
    return getWithAuth("system", {
        "method": "requestReboot",
        "id": 10,
        "params": [],
        "version": "1.0"
    })

def setActiveApp(uri):
    return getWithAuth("appControl", {
        "method": "setActiveApp",
        "id": 601,
        "params": [{
            "uri": uri
        }],
        "version": "1.0"
    })

def setAudioMute(mute=True):
    return getWithAuth("audio", {
        "method": "setAudioMute",
        "id": 601,
        "params": [{"status": mute}],
        "version": "1.0"
    })

def setAudioVolume(volume, target="", ui=None):
    return getWithAuth("audio", {
        "method": "setAudioVolume",
        "id": 98,
        "params": [{
            "volume": f"{volume}",
            "ui": ui,
            "target": target
        }],
        "version": "1.2"
    })

def setLEDIndicatorStatus(mode="Dark", status="true"):
    return getWithAuth("system", {
        "method": "setLEDIndicatorStatus",
        "id": 53,
        "params": [{
            "mode": mode,
            "status": status
        }],
        "version": "1.1"
    })

def setSoundSettings(value="audioSystem"):
    return getWithAuth("audio", {
        "method": "setSoundSettings",
        "id": 5,
        "params": [{"settings": [{
            "value": value,
            "target": "outputTerminal"
        }]}],
        "version": "1.1"
    })

def setTextForm(text, encKey=""):
    return getWithAuth("appControl", {
        "method": "setTextForm",
        "id": 601,
        "params": [{
            "encKey": encKey,
            "text": text
        }],
        "version": "1.1"
    })

def terminateApps():
    return getWithAuth("appControl", {
        "method": "terminateApps",
        "id": 55,
        "params": [],
        "version": "1.0"
    })
