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

This project supports three environments: **dev**, **staging**, and **prod**.

### Environments

- **Dev**: Deploys automatically on push to `dev` branch → Lambda: `dnd-api-dev`
- **Staging**: Deploys automatically on push to `staging` branch → Lambda: `dnd-api-staging`
- **Production**: Deploys automatically on push to `main` branch (requires PR approval) → Lambda: `dnd-api-prod`

### Manual Deployment

#### Build

Build the application for Lambda deployment:

```bash
sam build
```

Or use Docker for consistent builds (recommended if you have a different Python version):

```bash
sam build --use-container
```

#### Deploy to Specific Environment

Deploy to **dev**:

```bash
sam deploy --config-env dev
```

Deploy to **staging**:

```bash
sam deploy --config-env staging
```

Deploy to **prod**:

```bash
sam deploy --config-env prod
```

First time deployment (guided mode):

```bash
sam deploy --guided --config-env dev
```

### GitHub Actions Setup

The project uses GitHub Actions for CI/CD:

1. **Tests** run on every push and PR to `dev`, `staging`, and `main`
2. **Deployments** are automatic:
   - `dev` branch → deploys to dev environment
   - `staging` branch → deploys to staging environment
   - `main` branch → deploys to production (requires PR approval)

#### Required GitHub Configuration

1. Go to **Settings** → **Environments** in your GitHub repo
2. Create three environments: `dev`, `staging`, `production`
3. For `production` environment:
   - Enable **Required reviewers** (add team members who should approve)
   - Optionally add **Wait timer** for additional safety
4. Add `AWS_ROLE_ARN` secret at the repository level

### View Logs

Check CloudWatch logs for your Lambda functions:

```bash
# Dev environment
sam logs -n dnd-api-dev --stack-name DndApiStack-dev --tail

# Staging environment
sam logs -n dnd-api-staging --stack-name DndApiStack-staging --tail

# Production environment
sam logs -n dnd-api-prod --stack-name DndApiStack-prod --tail
```

### Delete Stack

Remove AWS resources for a specific environment:

```bash
# Delete dev
sam delete --stack-name DndApiStack-dev

# Delete staging
sam delete --stack-name DndApiStack-staging

# Delete production
sam delete --stack-name DndApiStack-prod
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

[Example Repo](https://github.com/ArjanCodes/examples/tree/main/2025/project)
