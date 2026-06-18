# Function

A function is a reusable block of code that performs a specific task. Functions help organize code, avoid repetition, and make programs easier to read and maintain.

## Why use functions?
- To break a program into smaller, manageable pieces
- To avoid repeating code
- To make code reusable and easier to test

## Defining a Function
Use the `def` keyword, followed by the function name and parentheses `()`.
```python
def greet():
    print("Hello!")
```

## Calling a Function
To run the code inside a function, call it by its name followed by parentheses:
```python
greet()  # Output: Hello!
```

## Function with Parameters
You can pass data to a function using parameters:
```python
def greet(name):
    print("Hello, " + name)

greet("Alice")  # Output: Hello, Alice
```

## Function with Return Value
A function can return a value using the `return` statement:
```python
def add(a, b):
    return a + b

result = add(2, 3)
print(result)  # Output: 5
```
