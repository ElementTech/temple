import random
import temple
import json

@temple.endpoint
def run(**kwargs):
    return f"Got:\n{json.dumps(kwargs,sort_keys=True, indent=4)}"

@temple.endpoint
def log(**kwargs):
    done = random.choice([True, False])
    if not done:
        return "Thinking to whom to say hello to...", 425
    return "Going to say it:",200

@temple.endpoint
def res(**kwargs):
    print("resulting")
    return "Hello World!"
