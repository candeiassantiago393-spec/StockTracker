# Python module layout (reference)

Numbered banner sections and structured docstrings used on Siemens firmware/tools projects.

```python
###############################################################################
# 1. Module Level Documentation
###############################################################################
"""One-line summary of the module purpose."""

###############################################################################
# 2. Imports
###############################################################################

###############################################################################
# 3. Constants and Global Variables
###############################################################################

###############################################################################
# 4. MyClass
###############################################################################
class MyClass:
    """
    Class:
        What the class does.
    Args:
        ...
    """
    def public_method(self):
        """
        Public Method:
            What it does.
        Args:
            ...
        """
```

Stock Tracker modules already using this pattern:

- `src/main.py`
- `src/core/stock.py`
- `src/core/suppliers/base.py`
- `src/core/suppliers/__init__.py`

Full example from team: `ModbusManager` / `Bus` (RS-485, multiple units per COM port).
