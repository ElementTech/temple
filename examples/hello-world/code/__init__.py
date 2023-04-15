import random

def run(**kwargs):
    print("starting")
    return "Started"

def log(**kwargs):
    done = random.choice([True, False])
    if not done:
        return "Not done yet. This is a log.", 425
    return "Done!",200

def res(**kwargs):
    print("resulting")
    return "Result"
