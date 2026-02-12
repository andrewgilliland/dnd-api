#!/usr/bin/env python3
"""AWS CDK App for D&D API"""

import os
import aws_cdk as cdk
from stacks.dnd_api_stack import DndApiStack

app = cdk.App()

# Get environment from context or default to dev
deployment_env = app.node.try_get_context("environment") or "dev"

DndApiStack(
    app,
    f"DndApiStack-{deployment_env}",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION", "us-east-1"),
    ),
    deployment_env=deployment_env,
    description=f"D&D API Stack - {deployment_env}",
)

app.synth()
