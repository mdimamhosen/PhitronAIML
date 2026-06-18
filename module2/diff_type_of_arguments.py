# Different types of arguments example
def func(a, b=2, *args, **kwargs):
    print(a, b, args, kwargs)
func(1, 3, 4, 5, x=10, y=20)
