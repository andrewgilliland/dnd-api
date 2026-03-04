#!/usr/bin/env python3
"""AWS CDK App for D&D API"""

import os
import aws_cdk as cdk
from stacks.dnd_api_stack import DndApiStack
from stacks.pipeline_stack import DndApiPipelineStack

app = cdk.App()

aws_env = cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION", "us-east-1"),
)

# ---------------------------------------------------------------------------
# API stacks — one per environment
# Deploy with: cdk deploy DndApiStack-dev --context environment=dev
# ---------------------------------------------------------------------------
for env in ("dev", "staging", "prod"):
    DndApiStack(
        app,
        f"DndApiStack-{env}",
        env=aws_env,
        deployment_env=env,
        description=f"D&D API Stack - {env}",
    )

# ---------------------------------------------------------------------------
# Pipeline stacks — one per environment
# Requires context values (set in cdk.context.json or via --context flags):
#   github_owner, github_repo, github_connection_arn
# Branch convention: dev → dev, staging → staging, prod → main
# ---------------------------------------------------------------------------
github_owner = app.node.try_get_context("github_owner") or ""
github_repo = app.node.try_get_context("github_repo") or ""
github_connection_arn = app.node.try_get_context("github_connection_arn") or ""

BRANCH_MAP = {
    "dev": "dev",
    "staging": "staging",
    "prod": "main",
}

for env, branch in BRANCH_MAP.items():
    DndApiPipelineStack(
        app,
        f"DndApiPipelineStack-{env}",
        env=aws_env,
        deployment_env=env,
        lambda_function_name=f"dnd-api-{env}",
        github_owner=github_owner,
        github_repo=github_repo,
        github_branch=branch,
        github_connection_arn=github_connection_arn,
        description=f"D&D API CodePipeline - {env}",
    )

app.synth()
