

def endpoint(func, **kwargs):
    def inner(**kwargs):
        print("Starting temple endpoint")
        result = func(**kwargs)
        print("Finished temple endpoint")
        return result
    inner.endpoint = True
    return inner
