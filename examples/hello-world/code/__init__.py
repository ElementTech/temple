import random
import temple

@temple.endpoint
def run(**kwargs):
    print("starting")
    return "Started"

@temple.endpoint
def log(**kwargs):
    done = random.choice([True, False])
    if not done:
        return "Not done yet. This is a log.", 425
    return "Done!",200

@temple.endpoint
def res(**kwargs):
    print("resulting")
    return "Result"
