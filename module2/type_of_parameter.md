# Type of Parameter

Parameters can be positional, keyword, default, variable-length, etc.

**Example (Python):**
```python
def example(a, b=2, *args, **kwargs):
    print(a, b, args, kwargs)
example(1, 3, 4, 5, x=10, y=20)
```
