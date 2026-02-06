# D&D API

A FastAPI application for D&D 5e game data with character, monster, and item management. Features random generators, comprehensive filtering, and RESTful API design. Deployable to AWS Lambda.

## Features

- **API Versioning** - `/api/v1` endpoints for future compatibility
- **Character Management** - Browse D&D characters with filtering by class, race, and name
- **Monster Database** - Extensive monster collection with CR-based filtering
- **Item/Equipment System** - Weapons, armor, potions, and magical items
- **Random Generators** - Create random characters and monsters with context-aware descriptions
- **Data Separation** - Clean JSON data files for easy maintenance
- **Utility Helpers** - Dice rolling, calculations, validators, and formatters

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
- API endpoints: http://127.0.0.1:8000/api/v1

## API Endpoints

### Core Endpoints

- `GET /` - Welcome message and API info
- `GET /health` - Health check for monitoring

### Characters (v1)

- `GET /api/v1/characters` - List all characters (filter by class, race, name)
- `GET /api/v1/characters/{id}` - Get specific character
- `GET /api/v1/characters/random` - Generate random character

### Monsters (v1)

- `GET /api/v1/monsters` - List all monsters (filter by type, size, CR, name)
- `GET /api/v1/monsters/{id}` - Get specific monster
- `GET /api/v1/monsters/random` - Generate random monster (optional filters)

### Items (v1)

- `GET /api/v1/items` - List all items (filter by type, rarity, magic, cost, name)
- `GET /api/v1/items/{id}` - Get specific item

### Game Data (v1)

- `GET /api/v1/classes` - List all character classes
- `GET /api/v1/races` - List all character races

## AWS Lambda Deployment

This project supports two environments: **staging** and **prod**.

### Environments

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
sam deploy --guided --config-env staging
```

### GitHub Actions Setup

The project uses GitHub Actions for CI/CD:

1. **Tests** run on every push and PR to `staging` and `main`
2. **Deployments** are automatic:
   - `staging` branch → deploys to staging environment
   - `main` branch → deploys to production (requires PR approval)

#### Required GitHub Configuration

1. Go to **Settings** → **Environments** in your GitHub repo
2. Create two environments: `staging`, `production`
3. For `production` environment:
   - Enable **Required reviewers** (add team members who should approve)
   - Optionally add **Wait timer** for additional safety
4. Add `AWS_ROLE_ARN` secret at the repository level

### View Logs

Check CloudWatch logs for your Lambda functions:

```bash
# Staging environment
sam logs -n dnd-api-staging --stack-name DndApiStack-staging --tail

# Production environment
sam logs -n dnd-api-prod --stack-name DndApiStack-prod --tail
```

### Delete Stack

Remove AWS resources for a specific environment:

```bash
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
│   ├── api/                 # API routes (versioned)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── characters.py
│   │       ├── monsters.py
│   │       ├── items.py
│   │       └── game_data.py
│   ├── models/              # Pydantic models (domain)
│   │   ├── __init__.py
│   │   ├── common.py        # Shared models (Stats, Size, Alignment)
│   │   ├── character.py     # Character models and enums
│   │   ├── monster.py       # Monster models and enums
│   │   ├── item.py          # Item models and enums
│   │   └── responses/       # API response models
│   │       ├── __init__.py
│   │       ├── character_responses.py
│   │       ├── monster_responses.py
│   │       └── item_responses.py
│   ├── services/            # Business logic
│   │   ├── data_loader.py   # Cached JSON data loading
│   │   ├── character_service.py
│   │   └── monster_service.py
│   ├── utils/               # Helper utilities
│   │   ├── __init__.py
│   │   ├── dice.py          # Dice rolling utilities
│   │   ├── calculations.py  # Game mechanic calculations
│   │   ├── formatters.py    # String formatting helpers
│   │   └── validators.py    # Validation utilities
│   ├── config/              # Configuration
│   │   ├── __init__.py
│   │   ├── settings.py      # Application settings
│   │   └── constants.py     # Game constants (XP, hit dice, etc.)
│   └── data/                # JSON data files
│       ├── characters.json  # Character records
│       ├── monsters.json    # Monster records
│       ├── items.json       # Item records
│       ├── character_names.json
│       ├── character_traits.json
│       └── monster_names.json
├── tests/                   # Test files
├── .aws-sam/                # SAM build artifacts (gitignored)
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD pipeline
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
