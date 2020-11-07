import urllib.request
import json
import time
import sys

from . import setup as setup_script
from . import access
from .common import printerr
from .common import color

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
    req = urllib.request.Request(f"http://{ip}/{path}", data)
    response = sendRequest(req, log if log else "GET " + path, timeout=timeout)
    return json.loads(response.read())


def getWithAuth(path, jsonData, log=None):
    setupAccess()
    data = json.dumps(jsonData).encode("utf-8")
    headers = {"Cookie": cookie}
    req = urllib.request.Request(f"http://{ip}/{path}", data, headers)
    response = sendRequest(req, log if log else "GET with auth " + path)
    return json.loads(response.read())


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
        response = getWithAuth("sony/avContent", {
            "method": "setPlayContent",
            "id": 101,
            "params": [{"uri": selected}],
            "version": "1.0"
        }, log="Set current input")
    else:
        response = getWithAuth("sony/avContent", {
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
        response = get("sony/system", {
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
        response = getWithAuth("sony/system", {
            "method": "setPowerSavingMode",
            "id": 52,
            "params": [{"mode": selected}],
            "version": "1.0"
        }, log=f"Set power saving mode {selected}")
        return
    try:
        response = get("sony/system", {
            "method": "getPowerSavingMode",
            "id": 51,
            "params": [],
            "version": "1.0"
        }, log="Get power saving mode", timeout=1)
        return response['result'][0]['mode']
    except:
        return None
