# Cars API Testing Framework

Automated testing framework for API Ninjas Cars API using Python, pytest, and JSON Schema validation.

## 🚀 Features

- **API Testing**: REST API testing with requests library
- **JSON Schema Validation**: Contract validation with jsonschema
- **Flexible Configuration**: YAML + .env configuration system
- **Factory Pattern**: Easy API client creation for multiple services
- **Allure Reporting**: Beautiful test reports
- **CI/CD**: GitHub Actions integration

## 🛠️ Installation

1. **Clone and setup**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment**
   ```bash
   cp env.example .env
   # Edit .env with your API_NINJAS_KEY
   ```

## 📁 Project Structure

```
cars-api-tests/
├── config/base.yaml          # Configuration
├── src/
│   ├── api/                  # API client, endpoints, schemas
│   ├── utils/config.py       # Configuration manager
│   └── fixtures/             # Pytest fixtures
├── tests/api/                # API tests
├── .env                      # Environment variables
└── requirements.txt          # Dependencies
```

## 🧪 Running Tests

```bash
# All tests
pytest

# API tests only
pytest -m api

# With Allure reporting
pytest --allure-results-dir=reports/allure-results
allure serve reports/allure-results
```

## 📊 JSON Schema Validation

```python
import jsonschema
from src.api.schemas import CARS_RESPONSE_SCHEMA

# Validate API response
jsonschema.validate(cars_data, CARS_RESPONSE_SCHEMA)
```

## 📚 Best Practices

1. Use factory pattern for API clients
2. Validate contracts with JSON Schema
3. Keep secrets in .env (not in git)
4. Use Allure steps for better reporting
5. Group related tests in classes

## 🐛 Debugging

### VS Code Debug Configuration

Create a `.vscode` directory in your project root and add the following `launch.json` configuration:

```json
{
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Python: pytest",
        "type": "debugpy",
        "request": "launch",
        "module": "pytest",
        "args": [
          "${file}"
        ],
        "console": "integratedTerminal"
      }
    ]
}
```

## 🔧 Code Quality

### Black (Code Formatter)
Black automatically formats your Python code to ensure consistent style:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .

# Format specific directory
black src/ tests/
```

### Flake8 (Linter)
Flake8 analyzes your code for errors and style issues:

```bash
# Lint all Python files
flake8 .

# Lint specific directories
flake8 src/ tests/

```

## 📊 Test Reports

**Live Allure Report**: [https://yasnowitzz.github.io/testing-framework/allure-report/]


