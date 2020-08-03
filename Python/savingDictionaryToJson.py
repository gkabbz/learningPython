import json

dict = {
    "key01": "value01",
    "key02": "value02",

    "key03": "value05",
    "key04": "value07",


    "key05": "value077",
    "key06": "value099"
}

json = json.dumps(dict)
f = open("/Users/kabbz/Google Drive/Python/Github Personal/learningPython/dict.json","w")
f.write(json)
f.close()