# AWS CDK Deployment for D&D API

This directory contains the AWS CDK infrastructure code to deploy the D&D API to AWS Lambda with API Gateway.

## Prerequisites

- Python 3.12+
- AWS CLI configured with credentials
- AWS CDK CLI installed: `npm install -g aws-cdk`
- Node.js (for CDK CLI)

## Setup

1. **Install CDK dependencies**:

   ```bash
   cd cdk
   pip install -r requirements.txt
   ```

2. **Configure AWS credentials** (if not already done):

   ```bash
   aws configure
   ```

3. **Bootstrap CDK** (one-time per account/region):
   ```bash
   cdk bootstrap
   ```

## Deployment Commands

### Deploy to Development

```bash
cd cdk
cdk deploy --context environment=dev
```

### Deploy to Staging

```bash
cd cdk
cdk deploy --context environment=staging
```

### Deploy to Production

```bash
cd cdk
cdk deploy --context environment=prod
```

## Useful CDK Commands

- `cdk ls` - List all stacks in the app
- `cdk synth` - Synthesize CloudFormation template
- `cdk diff` - Compare deployed stack with current state
- `cdk deploy` - Deploy stack to AWS
- `cdk destroy` - Remove stack from AWS
- `cdk watch` - Watch for changes and auto-deploy (dev mode)

## Stack Resources

The CDK stack creates:

1. **Lambda Function**
   - Runtime: Python 3.12
   - Memory: 512 MB
   - Timeout: 30 seconds
   - Handler: `app.lambda_handler.handler`

2. **API Gateway**
   - REST API with Lambda proxy integration
   - CORS enabled
   - Throttling: 100 requests/sec (burst: 200)
   - CloudWatch logging

3. **CloudWatch Logs**
   - Log retention: 7 days (dev), 30 days (prod)

## Environment Variables

The Lambda function receives:

- `ENVIRONMENT`: dev/staging/prod
- `POWERTOOLS_SERVICE_NAME`: dnd-api

## Outputs

After deployment, you'll get:

- **ApiUrl**: The API Gateway endpoint URL
- **ApiId**: API Gateway ID
- **LambdaFunctionArn**: Lambda function ARN
- **LambdaFunctionName**: Lambda function name

## Cost Estimation

**Development (low traffic)**:

- Lambda: ~$0-5/month (1M requests free tier)
- API Gateway: ~$3.50/month (1M requests)
- CloudWatch Logs: ~$0.50/month
- **Total**: ~$4-9/month

**Production (moderate traffic)**:

- Depends on request volume
- First 1M Lambda requests free
- $0.20 per 1M requests after

## Testing the Deployment

```bash
# Get the API URL from outputs
API_URL=$(aws cloudformation describe-stacks --stack-name DndApiStack-dev --query "Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue" --output text)

# Test the API
curl $API_URL

# Test specific endpoints
curl $API_URL/api/v1/characters
curl $API_URL/api/v1/monsters
curl $API_URL/api/v1/combat
```

## Cleanup

To remove all resources:

```bash
cd cdk
cdk destroy --context environment=dev
```

## Development Workflow

1. Make changes to your API code
2. Test locally: `uv run uvicorn app.main:app --reload`
3. Deploy to dev: `cd cdk && cdk deploy --context environment=dev`
4. Test deployed API
5. Deploy to prod when ready

## Adding RDS Database (Future)

To add RDS support, update [stacks/dnd_api_stack.py](stacks/dnd_api_stack.py):

```python
from aws_cdk import aws_rds as rds, aws_ec2 as ec2

# Add VPC
vpc = ec2.Vpc(self, "DndApiVpc", max_azs=2)

# Add RDS instance
database = rds.DatabaseInstance(
    self, "DndApiDatabase",
    engine=rds.DatabaseInstanceEngine.postgres(...),
    vpc=vpc,
    # ... other config
)

# Update Lambda with database connection
self.lambda_function.add_environment(
    "DATABASE_URL", database.secret.secret_value_from_json("connectionString")
)
```
