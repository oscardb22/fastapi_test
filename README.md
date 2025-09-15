# ⚡️ fastapi_test

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Docker & Docker Compose
- [uv](https://docs.astral.sh/uv/) (Python package manager)

## 🛠️ Development Tools
#### Running Linters

```bash

# Install development dependencies
uv sync --group dev

# Run Ruff linter
uv run ruff check .

# Run Ruff formatter
uv run ruff format .

# Run MyPy type checking
uv run mypy .
```

### Available Make Commands

```bash

make run_dev         # Start development environment
make stop_dev        # Stop development environment
make build           # Build Docker image
make run_tests       # Run the tests project
make run_linter      # Run the linter rules
make run_linter_fix  # Run check and fix linter rules
make run_app         # Run application
```
