import json

with open('snippetsEnvVariables2.json') as json_file:
    data = json.load(json_file)
    print(data['key'])

