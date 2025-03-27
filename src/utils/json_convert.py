import json

# Convert data to JSON format
def to_json(data):
    return json.loads(json.dumps(data))