# D&D API

A FastAPI application for D&D character data, deployable to AWS Lambda.

## Prerequisites

- Python 3.12 or higher
- AWS CLI configured with credentials
- AWS SAM CLI
- Docker (optional, for containerized builds)

## Local Development

1. Install dependencies

```bash
uv sync
```

2. Run the FastAPI app locally

```bash
uv run uvicorn app.main:app --reload
```

3. Visit the API

- API: http://127.0.0.1:8000
- Interactive docs: http://127.0.0.1:8000/docs
- Endpoints:
  - `/` - Welcome message
  - `/characters` - Get all D&D characters
  - `/classes` - Get all D&D classes
  - `/races` - Get all D&D races

## AWS Lambda Deployment

### Build

Build the application for Lambda deployment:

```bash
sam build
```

Or use Docker for consistent builds (recommended if you have a different Python version):

```bash
sam build --use-container
```

### Deploy

Deploy to AWS Lambda (first time, use guided mode):

```bash
sam deploy --guided
```

For subsequent deployments:

```bash
sam deploy
```

### View Logs

Check CloudWatch logs for your Lambda function:

```bash
sam logs -n DndApiFunction --stack-name DndApiStack --tail
```

### Delete Stack

Remove all AWS resources:

```bash
sam delete --stack-name DndApiStack
```

## Project Structure

```
dnd-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app instance
│   ├── lambda_handler.py    # Lambda entry point with Mangum
│   ├── characters.json      # Character data
│   └── models/
│       ├── __init__.py
│       └── schemas.py       # Pydantic models
├── .aws-sam/                # SAM build artifacts (gitignored)
├── .env
├── .gitignore
├── pyproject.toml           # Python dependencies
├── requirements.txt         # Lambda deployment dependencies
├── README.md
├── samconfig.toml           # SAM configuration
└── template.yaml            # AWS SAM template
```

## Environment Variables

Set any required environment variables in `template.yaml` under `Globals.Function.Environment`.

## API Documentation

Once deployed, find your API Gateway URL in the SAM deploy output or CloudFormation console. The interactive API documentation is available at:

```
https://<api-gateway-url>/Prod/docs
```

[Anatomy of a Scalable Python Project (FastAPI)](https://www.youtube.com/watch?v=Af6Zr0tNNdE)
