"""D&D API CDK Stack"""

from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    BundlingOptions,
    RemovalPolicy,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_cognito as cognito,
    aws_logs as logs,
)
from constructs import Construct


class DndApiStack(Stack):
    """CDK Stack for D&D API with Lambda and API Gateway"""

    def __init__(
        self, scope: Construct, construct_id: str, deployment_env: str = "dev", **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.deployment_env = deployment_env

        # Create Cognito User Pool
        self.user_pool, self.user_pool_client = self._create_cognito()

        # Create Lambda function
        self.lambda_function = self._create_lambda_function()

        # Create API Gateway with Cognito authorizer
        self.api = self._create_api_gateway()

        # Create outputs
        self._create_outputs()

    def _create_cognito(
        self,
    ) -> tuple[cognito.UserPool, cognito.UserPoolClient]:
        """Create Cognito User Pool and App Client for JWT authentication"""

        user_pool = cognito.UserPool(
            self,
            "DndApiUserPool",
            user_pool_name=f"dnd-api-users-{self.deployment_env}",
            # Users must be created by an admin — no public self-signup
            self_sign_up_enabled=False,
            sign_in_aliases=cognito.SignInAliases(email=True, username=True),
            password_policy=cognito.PasswordPolicy(
                min_length=12,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True,
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            removal_policy=RemovalPolicy.DESTROY
            if self.deployment_env == "dev"
            else RemovalPolicy.RETAIN,
        )

        # App client — no client secret so tokens can be retrieved from CLI/frontend
        user_pool_client = user_pool.add_client(
            "DndApiUserPoolClient",
            user_pool_client_name=f"dnd-api-client-{self.deployment_env}",
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
            ),
            # Token validity
            access_token_validity=Duration.hours(1),
            id_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.days(30),
            generate_secret=False,
        )

        return user_pool, user_pool_client

    def _create_lambda_function(self) -> lambda_.Function:
        """Create the Lambda function for the D&D API"""

        # Create log group with retention policy
        log_group = logs.LogGroup(
            self,
            "DndApiFunctionLogGroup",
            log_group_name=f"/aws/lambda/dnd-api-{self.deployment_env}",
            retention=logs.RetentionDays.ONE_WEEK
            if self.deployment_env == "dev"
            else logs.RetentionDays.ONE_MONTH,
        )

        function = lambda_.Function(
            self,
            "DndApiFunction",
            function_name=f"dnd-api-{self.deployment_env}",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="app.lambda_handler.handler",
            architecture=lambda_.Architecture.ARM_64,
            code=lambda_.Code.from_asset(
                "../",
                bundling=BundlingOptions(
                    image=lambda_.Runtime.PYTHON_3_12.bundling_image,
                    platform="linux/arm64",
                    command=[
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t /asset-output && "
                        "cp -r app /asset-output/",
                    ],
                ),
            ),
            timeout=Duration.seconds(30),
            memory_size=512,
            environment={
                "ENVIRONMENT": self.deployment_env,
                "POWERTOOLS_SERVICE_NAME": "dnd-api",
            },
            description=f"D&D API FastAPI Lambda function - {self.deployment_env}",
            log_group=log_group,
        )

        return function

    def _create_api_gateway(self) -> apigateway.LambdaRestApi:
        """Create API Gateway with Cognito JWT authorizer"""

        authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self,
            "DndApiCognitoAuthorizer",
            cognito_user_pools=[self.user_pool],
            authorizer_name=f"dnd-api-cognito-authorizer-{self.deployment_env}",
            # Cache the authorization result for 5 minutes to reduce Cognito calls
            results_cache_ttl=Duration.minutes(5),
        )

        api = apigateway.LambdaRestApi(
            self,
            "DndApiGateway",
            handler=self.lambda_function,
            rest_api_name=f"dnd-api-{self.deployment_env}",
            proxy=True,
            description=f"D&D API Gateway - {self.deployment_env}",
            # Require a valid Cognito JWT on every method except OPTIONS (CORS preflight)
            default_method_options=apigateway.MethodOptions(
                authorizer=authorizer,
                authorization_type=apigateway.AuthorizationType.COGNITO,
            ),
            deploy_options=apigateway.StageOptions(
                stage_name=self.deployment_env,
                throttling_rate_limit=100,
                throttling_burst_limit=200,
                logging_level=apigateway.MethodLoggingLevel.INFO
                if self.deployment_env == "dev"
                else apigateway.MethodLoggingLevel.ERROR,
                data_trace_enabled=self.deployment_env == "dev",
                metrics_enabled=True,
            ),
            # CORS configuration
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS,
                allow_methods=apigateway.Cors.ALL_METHODS,
                allow_headers=[
                    "Content-Type",
                    "X-Amz-Date",
                    "Authorization",
                    "X-Api-Key",
                    "X-Amz-Security-Token",
                ],
            ),
        )

        return api

    def _create_outputs(self) -> None:
        """Create CloudFormation outputs"""

        CfnOutput(
            self,
            "UserPoolId",
            value=self.user_pool.user_pool_id,
            description="Cognito User Pool ID",
            export_name=f"DndApiUserPoolId-{self.deployment_env}",
        )

        CfnOutput(
            self,
            "UserPoolClientId",
            value=self.user_pool_client.user_pool_client_id,
            description="Cognito User Pool App Client ID",
            export_name=f"DndApiUserPoolClientId-{self.deployment_env}",
        )

        CfnOutput(
            self,
            "ApiUrl",
            value=self.api.url,
            description="D&D API Gateway URL",
            export_name=f"DndApiUrl-{self.deployment_env}",
        )

        CfnOutput(
            self,
            "ApiId",
            value=self.api.rest_api_id,
            description="API Gateway ID",
            export_name=f"DndApiId-{self.deployment_env}",
        )

        CfnOutput(
            self,
            "LambdaFunctionArn",
            value=self.lambda_function.function_arn,
            description="Lambda Function ARN",
            export_name=f"DndApiFunctionArn-{self.deployment_env}",
        )

        CfnOutput(
            self,
            "LambdaFunctionName",
            value=self.lambda_function.function_name,
            description="Lambda Function Name",
            export_name=f"DndApiFunctionName-{self.deployment_env}",
        )

        CfnOutput(
            self,
            "Environment",
            value=self.deployment_env,
            description="Deployment environment",
        )
