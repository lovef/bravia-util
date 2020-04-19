#!/usr/bin/env python3

import urllib.request
import json
import setup as setup_script
import time
from common import printerr

ip = None

def setup(script):
    global ip
    ip = setup_script.main(script)

def get(path, jsonData):
    data = json.dumps(jsonData).encode("utf-8")
    req = urllib.request.Request(f"http://{ip}/{path}", data)
    response = sendRequest(req, path)
    return json.loads(response.read())

def requestCookie(url, data, auth = None):
    headers = { "Authorization": auth } if auth is not None else {}
    req = urllib.request.Request(url, data, headers)
    response = sendRequest(req, "Request cookie")
    return response.info()['Set-Cookie']

def sendRequest(request, log):
    done = False
    try:
        printerr(log, end ="..")
        start = time.time()
        response = urllib.request.urlopen(request)
        done = True
        return response
    finally:
        end = time.time()
        printerr("done" if done else "failed", "in", end - start)
