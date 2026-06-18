# Iterators and Generators in Python

## Iterators
- An iterator is an object that can be iterated upon (traversed through all the values).
- It implements two methods: `__iter__()` and `__next__()`.
- Built-in collections like list, tuple, set, and dict are iterable, but not all are iterators.
- Use `iter()` to get an iterator from an iterable.
- Use `next()` to get the next item from the iterator.

### Example: Set Iterator
```python
s = {1, 2, 3}
iterator = iter(s)
print(next(iterator))  # Output: 1 (order may vary)
print(next(iterator))  # Output: 2
print(next(iterator))  # Output: 3
```

## Generators
- Generators are a simple way to create iterators using functions and the `yield` statement.
- Each time `yield` is called, the function's state is saved, and execution resumes from there on the next call.

### Example: Generator Function
```python
def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()
print(next(gen))  # Output: 1
print(next(gen))  # Output: 2
print(next(gen))  # Output: 3
```

---

# Lambda, filter, and map Functions

## Lambda Function
- A lambda function is a small anonymous function defined with the `lambda` keyword.
- Syntax: `lambda arguments: expression`

### Example:
```python
add = lambda x, y: x + y
print(add(2, 3))  # Output: 5
```

## filter() Function
- `filter(function, iterable)` constructs an iterator from elements of iterable for which function returns True.

### Example:
```python
nums = [1, 2, 3, 4, 5]
even = list(filter(lambda x: x % 2 == 0, nums))
print(even)  # Output: [2, 4]
```

## map() Function
- `map(function, iterable)` applies function to every item of iterable and returns a map object (iterator).

### Example:
```python
nums = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, nums))
print(squares)  # Output: [1, 4, 9, 16, 25]
```

## apply() Function (Python 2 only)
- `apply(function, args[, kwargs])` was used in Python 2 to call a function with arguments supplied as a tuple and optional dictionary.
- It is **removed in Python 3**. In Python 3, use `function(*args, **kwargs)` instead.

### Example (Python 2):
```python
# Python 2 only:
# def add(x, y):
#     return x + y
# result = apply(add, (2, 3))  # Output: 5
```

### Python 3 Equivalent:
```python
def add(x, y):
    return x + y
result = add(*(2, 3))  # Output: 5
print(result)
```
