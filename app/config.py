import json

data = None

with open('app/app_config.json') as f:
    data = json.loads(f.read())
