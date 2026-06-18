# **kwargs example
def show(**kwargs):
    for key, value in kwargs.items():
        print(key, value)
show(name="Alice", age=20)
