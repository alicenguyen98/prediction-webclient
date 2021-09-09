import json

config = None

def init(config_path):
    global config
    with open(config_path, 'r') as f:
        config = json.load(f)

def get():
    global config
    return config