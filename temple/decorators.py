def endpoint(func):
    def inner():
        return func()
    inner.endpoint = True
    return inner
