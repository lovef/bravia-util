import json

class ResponseFormatter:
    def format(responseText):
        return json.loads(responseText)

class PrettyResponseFormatter:
    def format(responseText):
        print(json.dumps(ResponseFormatter.format(responseText), indent=2))

formatter = ResponseFormatter

def formatResponse(response):
    return formatter.format(response)

def pretty(usePrettyFormatter=True):
    global formatter
    formatter = PrettyResponseFormatter if usePrettyFormatter else ResponseFormatter
