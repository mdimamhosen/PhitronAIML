# **kwargs

`**kwargs` allows a function to accept any number of keyword arguments.

**Example (Python):**
```python
def show(**kwargs):
    for key, value in kwargs.items():
        print(key, value)
show(name="Alice", age=20)
```
