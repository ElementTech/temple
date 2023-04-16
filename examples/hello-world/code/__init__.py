import random
import temple

@temple.endpoint
def run(**kwargs):
    return kwargs

@temple.endpoint
def log(**kwargs):
    done = random.choice([True, False])
    if not done:
        return "Still Running..", 425
    return "Done!",200

@temple.endpoint
def res(**kwargs):
    print("resulting")
    return "Congratulations! You have successfully ran the example python module."
