#!/bin/bash
# Quick deployment script for D&D API

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== D&D API CDK Deployment ===${NC}"

# Get environment (default to dev)
ENV=${1:-dev}
echo -e "${GREEN}Deploying to environment: ${ENV}${NC}"

# Change to CDK directory
cd "$(dirname "$0")"

# Check if CDK is installed
if ! command -v cdk &> /dev/null; then
    echo "CDK CLI not found. Installing..."
    npm install -g aws-cdk
fi

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

# Deploy
echo -e "${GREEN}Deploying stack...${NC}"
cdk deploy --context environment=${ENV} --require-approval never

echo -e "${GREEN}✅ Deployment complete!${NC}"
echo -e "${BLUE}Get your API URL with:${NC}"
echo "aws cloudformation describe-stacks --stack-name DndApiStack-${ENV} --query \"Stacks[0].Outputs[?OutputKey=='ApiUrl'].OutputValue\" --output text"
