# Type of parameter example
def example(a, b=2, *args, **kwargs):
    print(a, b, args, kwargs)
example(1, 3, 4, 5, x=10, y=20)
