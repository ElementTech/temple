#   - default: mytext
#     name: string-param
#     type: text
#   - default: 0
#     name: number-param
#     type: number
#   - choices: [a, b, c, d]
#     default: b
#     name: single-choice-param
#     type: single-choice
#   - choices: [e, f, g, h]
#     default: [e, g]
#     name: multi-choice-param
#     type: multi-choice


def run(**kwargs):
    print("Started", kwargs)

def log(**kwargs):
    print("Following", kwargs)

def res(**kwargs):
    print("Result", kwargs)
