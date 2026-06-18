# Iterator and Generator Examples

# Iterator Example with set
s = {1, 2, 3}
iterator = iter(s)
print(next(iterator))  # Output: 1 (order may vary)
print(next(iterator))  # Output: 2
print(next(iterator))  # Output: 3

# Generator Example
def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()
print(next(gen))  # Output: 1
print(next(gen))  # Output: 2
print(next(gen))  # Output: 3

# Lambda Function Example
add = lambda x, y: x + y
print(add(2, 3))  # Output: 5

# filter() Example
nums = [1, 2, 3, 4, 5]
even = list(filter(lambda x: x % 2 == 0, nums))
print(even)  # Output: [2, 4]

# map() Example
squares = list(map(lambda x: x ** 2, nums))
print(squares)  # Output: [1, 4, 9, 16, 25]

# apply() Function Equivalent in Python 3
def add(x, y):
    return x + y
result = add(*(2, 3))  # Output: 5
print(result)
