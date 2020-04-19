#!/usr/bin/env python3

import urllib.request
import json
import setup as setup_script

ip = None

def setup(script):
    global ip
    ip = setup_script.main(script)

def get(path, jsonData):
    data = json.dumps(jsonData).encode("utf-8")
    req = urllib.request.Request(f"http://{ip}/{path}", data)
    response = urllib.request.urlopen(req)
    return json.loads(response.read())
