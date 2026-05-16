---
description: "Python code conventions and standard practices for Python projects"
applyTo: "**/*.py"
---

# Python Code Guidelines

## Style & Formatting

### Black Formatter

All code must pass `black` formatting:

```bash
make style  # Via PieMaker
```

**Guidelines**:

- Use double quotes for strings (Black default)
- Don't manually format — `black` is authoritative
- Line length: 88 characters max

### Pylint Static Analysis

All code should have zero Pylint error and warning:

```bash
make lint
```

**Guidelines**:

- Disable warnings only when justified: `# pylint: disable=missing-docstring`
- Use specific codes, not blanket disables when the exemptions are only specific lines
- Attempt to fix warning root causes before disabling

## Python Conventions

### Imports

- Standard library imports first
- Third-party imports second (organized alphabetically)
- Local imports last
- Blank line between groups

```python
from typing import Dict, List
from unittest.mock import MagicMock, patch

import yaml

from mymodule import MyClass
from mymodule.utils import helper_function
```

### Type Hints

Use type hints where appropriate:

```python
def process_items(config_file: str, batch_size: int) -> None:
    """Process items from configuration file in batches."""
    ...

def _format_output(data: dict) -> str:
    """Format data to output string format."""
    ...
```

### Docstrings

Use **Google-style** or **Sphinx-style** docstrings depending on the module context:

**Google style (preferred for `__init__` methods)**:

```python
def __init__(self, config: dict):
    """Initialize service with configuration.

    Args:
        config: Configuration dictionary with required keys.

    Raises:
        ValueError: If configuration is invalid.
    """
    ...
```

**Sphinx style (for complex methods)**:

```python
def process_batch(self, items: list, batch_size: int = 50) -> None:
    """Process a batch of items.

    :param items: List of items to process.
    :param batch_size: Number of items per batch (default: 50).
    :raises IOError: If processing fails.
    """
    ...
```

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `DataProcessor`, `TestDataParser`)
- **Functions/Methods**: `snake_case` (e.g., `process_data`, `_format_output`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_BATCH_SIZE`)
- **Private/Internal**: Prefix with `_` (e.g., `_internal_helper`, `_format_error`)
- **Variables**: `snake_case` (e.g., `result_dict`, `item_count`)

### Logging

Always use a logger via Conflog, never print.

Have a logger instance in each module:

```python
from conflog import Conflog

LOGGER = None

def init():
    """Initialize logger.

    Logger is cached to prevent duplicate handlers
    from being added on repeated calls.
    """

    global LOGGER  # pylint: disable=global-statement
    if LOGGER is not None:
        return LOGGER

    cfl = Conflog(
        conf_dict={"level": "info", "format": "[<module>] %(levelname)s %(message)s"}
    )

    LOGGER = cfl.get_logger(__name__)
    return LOGGER
```

Then use the logger for all output:

```python
from .logger import init

logger = init(__name__)

logger.info("Message with %s", variable)
logger.error("Error message")
logger.debug("Debug message")
```

**Guidelines**:

- Use `%s` format placeholders, not f-strings, in logger calls
- Pass variables as separate arguments: `logger.info("msg %s", var)` not `logger.info(f"msg {var}")`
- f-strings are avoided within logger calls to prevent unnecessary string interpolation when the log level is higher than the message level
- Info level for important operations, debug for internal flow and troubleshooting

## File Organization

### Module Structure

```python
# 1. Module docstring
"""Module description and purpose."""

# 2. Imports
from typing import Dict
import yaml

# 3. Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# 4. Classes
class MyClass:
    """Class docstring."""
    ...

# 5. Functions
def my_function():
    """Function docstring."""
    ...

# 6. CLI or main entry (if applicable)
def cli():
    ...
```

### Line Length

- **Code**: 88 characters (Black standard)
- **Docstrings/comments**: 79 characters (PEP 257)
- **URLs/long strings**: Acceptable to exceed if no reasonable break

## Error Handling

### Use Exceptions, Not Exit Codes

```python
# Good
raise IOError(f"Config file not found: {file_path}")

# Avoid
print("ERROR: Config file not found")
sys.exit(1)
```

### Let Exceptions Propagate

Let the caller handle exceptions unless you're adding context:

```python
# Good
try:
    result = perform_operation(data)
except Exception as e:
    logger.error("Operation failed: %s", str(e))
    raise

# Avoid
try:
    result = perform_operation(data)
except Exception:
    pass  # Silent failure
```

## Common Patterns

### Reading Configuration

Always load configuration file using cfgrw:

```python
from cfgrw import CFGRW

def load_config(conf_file: str) -> dict:
    """Load configuration from file."""
    config = CFGRW(conf_file=conf_file).read(["key1", "key2"])
    return config
```

### Mocking Dependencies in Tests

Patch where the dependency is **used**, not where it's defined:

```python
# Good: Patch in the module where the dependency is used
@patch("mymodule.service.ExternalAPI")  # Imported in service.py
def test_operation(self, mock_api_cls):
    ...

# Avoid: Patching at the origin
@patch("external_library.API")  # Generic library module
def test_operation(self, mock_api_cls):
    ...
```

## Avoid

- **Bare `except:`** - Always catch specific exceptions
- **Global state** - Pass dependencies as arguments
- **Mutable default arguments** - Use `None` and create new instance
- **Over-nesting** - Extract functions if indentation gets deep (>3 levels)
- **Silent failures** - Log errors before continuing
