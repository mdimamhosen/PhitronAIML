# Tuple

A tuple in Python is a collection which is ordered and unchangeable (immutable). Once a tuple is created, you cannot modify its elements. Tuples are written with round brackets `()` and can store elements of different data types.

## Why use tuples?
- Tuples are faster than lists for certain operations.
- Useful for data that should not change (like coordinates, RGB colors, etc.).
- Can be used as keys in dictionaries (if they only contain immutable elements).

## Creating a Tuple
```python
t = (1, 2, 3)
print(t)  # Output: (1, 2, 3)
```

## Accessing Tuple Elements
```python
print(t[0])  # Output: 1
print(t[-1]) # Output: 3
```

## Tuple with Different Data Types
```python
mixed = (1, "apple", 3.14)
print(mixed)  # Output: (1, 'apple', 3.14)
```

## Tuple is Immutable
```python
t = (1, 2, 3)
# t[0] = 10  # This will raise an error: 'tuple' object does not support item assignment
```

## Tuple Unpacking
```python
point = (4, 5)
x, y = point
print(x)  # Output: 4
print(y)  # Output: 5
```

## Length of a Tuple
```python
t = (1, 2, 3, 4)
print(len(t))  # Output: 4
```

## Looping Through a Tuple
```python
for item in t:
	print(item)
```

## Nested Tuples
```python
t = ((1, 2), (3, 4))
print(t[0])  # Output: (1, 2)
```

## Tuple Methods
Tuples have only two built-in methods: `count()` and `index()`.
```python
t = (1, 2, 2, 3)
print(t.count(2))  # Output: 2
print(t.index(3))  # Output: 3
```
