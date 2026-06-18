# Different Types of Arguments

Arguments can be positional, keyword, default, variable-length, etc.

**Example (Python):**
```python
def func(a, b=2, *args, **kwargs):
    print(a, b, args, kwargs)
func(1, 3, 4, 5, x=10, y=20)
```
