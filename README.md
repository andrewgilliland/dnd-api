## Project Structure

```
tmnt-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance
│   ├── lambda_handler.py    # Lambda entry point with Mangum
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tmnt.py          # API routes
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   └── business_logic.py
│   └── config.py            # Configuration/settings
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── .env
├── .env.example
├── .gitignore
├── pyproject.toml           # Add mangum dependency
├── README.md
└── template.yaml            # AWS SAM template (or serverless.yml)
```
