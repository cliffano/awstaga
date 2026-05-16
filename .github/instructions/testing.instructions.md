---
description: "Testing conventions and standard practices for Python projects"
applyTo: "tests/**/*.py,tests-integration/**/*.py"
---

# Testing Guidelines

## Test Structure

### Unit Tests

**Location**: `tests/test_*.py`

**Purpose**: Test individual functions/methods in isolation

**Scope**:

- No filesystem and network calls (mock them)
- Faster execution
- High code coverage

### Integration Tests

**Location**: `tests-integration/test_*.py`

**Purpose**: Test end-to-end flows with real or semi-real external systems

**Scope**:

- May use filesystem and network calls (with test fixtures or mocks if needed)
- Slower execution
- Broader coverage (fewer, larger tests)

## Naming Conventions

### Test Files

```text
tests/
  test_module1.py        # Tests for module1.py
  test_module2.py        # Tests for module2.py
  test_utils.py          # Tests for utils.py

tests-integration/
  test_cli.py            # Integration tests for CLI
  test_service.py        # Integration tests for main service
```

### Test Classes

```python
class TestDataProcessor(unittest.TestCase):
    """Tests for DataProcessor class."""
    ...

class TestFormatOutput(unittest.TestCase):
    """Tests for _format_output method."""
    ...
```

### Test Methods

```python
def test_single_item_success(self):
    """Test processing a single item successfully."""
    ...

def test_operation_failure_logs_error(self):
    """Test that operation failure logs an error."""
    ...

def test_batching_over_max_size(self):
    """Test that items are batched when count exceeds max."""
    ...
```

**Pattern**: `test_<description_of_scenario>`

## Pytest Execution

### Running Tests

```bash
# All tests
make test

# All tests (quick mode)
pytest -q

# Specific file
pytest tests/test_module.py

# Specific test
pytest tests/test_module.py::TestClass::test_method

# Test matching a keyword
pytest -k "batch" -v
```

### Configuration

- Framework: `pytest`
- No special fixtures needed (use `unittest.TestCase` directly)
- Coverage: `pytest-cov` (via `make coverage`)

## Mocking Best Practices

### Import Mocking

```python
from unittest.mock import MagicMock, patch
```

### Patch at the Usage Point

Always patch where the dependency is imported/used:

```python
# Good: Patch in the module where dependency is used
@patch("mymodule.service.ExternalAPI")
def test_operation(self, mock_api_cls):
    ...

# Avoid: Patching at the origin
@patch("external_library.API")
def test_operation(self, mock_api_cls):
    ...
```

### Mock Structure

```python
# Create mocks
mock_api = MagicMock()
mock_logger = MagicMock()

# Set return values
mock_api.execute.return_value = mock_result

# Use in test
...

# Assert calls
mock_api.execute.assert_called_once()
assert mock_logger.info.call_count == 2
```

### Mocking File I/O

```python
with patch("builtins.open", mock.mock_open(read_data="config data")):
    result = read_config_file("config.yaml")
```

### Mocking External Services

```python
with patch("mymodule.service.ExternalAPI") as mock_api_cls:
    mock_api = MagicMock()
    mock_api_cls.return_value = mock_api
    mock_api.execute.return_value = MagicMock(status="ok", data="result")

    service = MyService({"url": "http://localhost:8080", "user": "u", "token": "t"})
    # Test code
```

## Test Assertion Patterns

### Basic Assertions

```python
# Value equality
assert result == expected_dict

# Membership
assert "field" in result
assert key not in result

# Type checking
assert isinstance(result, dict)
assert callable(func)

# Boolean
assert result is None
assert result is not None
```

### Mock Assertions

```python
# Called once with no args
mock_func.assert_called_once()

# Called with specific args
mock_func.assert_called_once_with("arg1", "arg2")

# Not called
mock_func.assert_not_called()

# Call count
assert mock_func.call_count == 3

# Call arguments
assert mock_func.call_args[0] == ("arg1",)
assert mock_func.call_args.kwargs == {"key": "value"}

# All calls
for call in mock_func.call_args_list:
    print(call)
```

### Logger Assertions

```python
# Check logger was called
mock_logger.info.assert_called_once_with("Operation %s completed", "task")

# Check error was logged
mock_logger.error.assert_called_once()

# Check call arguments
error_msg = mock_logger.error.call_args[0][0]
```

## Unit Test Patterns

### Testing a Simple Function

```python
def test_format_output_required_fields_only(self):
    """Test output formatting with required fields only."""
    input_data = {
        "name": "Item",
        "status": "active",
        "value": 42,
    }
    result = format_output(input_data)

    assert result["name"] == "Item"
    assert result["status"] == "active"
    assert result["value"] == 42
```

### Testing a Method with External Dependency

```python
@patch("mymodule.service.ExternalAPI")
@patch("mymodule.logger.init")
def test_operation_success(self, mock_init, mock_api_cls):
    """Test successful operation with external API."""
    # Setup
    mock_logger = MagicMock()
    mock_init.return_value = mock_logger

    mock_api = MagicMock()
    mock_api_cls.return_value = mock_api
    mock_result = MagicMock(status="success", value="result_data")
    mock_api.execute.return_value = mock_result

    # Execute
    config = {"url": "http://localhost", "user": "user", "token": "token"}
    service = MyService(config)
    output = service.perform_operation({"input": "data"})

    # Assert
    mock_logger.info.assert_called_once_with("Operation completed: %s", "result_data")
```

## Integration Test Patterns

### Testing CLI with CliRunner

```python
from click.testing import CliRunner
from mymodule import cli

def test_cli_help():
    """Test CLI help output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
```

### Testing Constructor Error Paths

```python
def test_constructor_with_missing_config(self):
    """Test service constructor with missing config file."""
    from cfgrw import CFGRW
    from mymodule.service import MyService

    with pytest.raises(FileNotFoundError):
        config = CFGRW(conf_file="nonexistent.yaml").read(...)
        service = MyService(config)
```

## Coverage

### Generate Coverage Report

```bash
make coverage
```

### Coverage Goals

- Aim for >= 90% code coverage
- Focus on critical paths (success flows, error handling)
- Be pedantic and don't ignore trivial getters/setters

## Common Pitfalls

1. **Mocking at the wrong level** - Patch where used, not imported
2. **Not resetting mocks** - Use `reset_mock()` between assertions
3. **Hardcoding test data** - Use descriptive variable names
4. **Not testing edge cases** - Empty lists, None values, exceptions
5. **Over-testing** - Test behavior, not implementation details
6. **Flaky tests** - Mock time-based logic, remove random delays

## CI Integration

Tests are run as part of `make ci`:

```bash
make test              # Unit tests
make test-integration  # Integration tests
```

All tests must pass before merging.
