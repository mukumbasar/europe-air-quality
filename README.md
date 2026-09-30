# Prerequisites

- Git
- Python 3.10+
- Docker & Docker Compose

# Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/mukumbasar/europe-air-quality.git](https://github.com/mukumbasar/europe-air-quality.git)
   cd europe-air-quality
   ```

2. **Set up virtual environment & install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Create environment file from template:**
   ```bash
   cp .env.example .env
   # Windows: copy .env.example .env
   ```

4. **Start the database:**
   ```bash
   docker compose up -d
   ```

# Running Tests

The project uses `pytest` for testing the ETL pipeline and forecasting modules.

Run the entire test suite:
```bash
pytest
```

Run tests with verbose output and live print/log statements enabled:
```bash
pytest -v -s
```

Run specific pipeline tests individually:
```bash
# Run extract pipeline tests
pytest tests/test_extract.py

# Run transform pipeline tests
pytest tests/test_transform.py

# Run forecast pipeline tests
pytest tests/test_forecast.py
```

Or run tests by keyword matching:
```bash
pytest -k extract
```

*(Optional)* Suppress third-party warnings during test execution:
```bash
pytest -W ignore
```

# TODO: Finish README.md later.