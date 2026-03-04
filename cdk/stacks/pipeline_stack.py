"""D&D API CodePipeline Stack — Lambda-only deployments per environment"""

from aws_cdk import (
    Stack,
    CfnOutput,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_iam as iam,
)
from constructs import Construct


class DndApiPipelineStack(Stack):
    """CodePipeline that builds and deploys only the Lambda function code.

    Does NOT redeploy CDK infrastructure — only runs `update-function-code`
    after building a deployment zip from the source repo.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        deployment_env: str,
        lambda_function_name: str,
        github_owner: str,
        github_repo: str,
        github_branch: str,
        github_connection_arn: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.deployment_env = deployment_env
        self.lambda_function_name = lambda_function_name

        # Artifacts
        source_artifact = codepipeline.Artifact("SourceArtifact")
        build_artifact = codepipeline.Artifact("BuildArtifact")

        # Build project
        build_project = self._create_build_project(lambda_function_name)

        # Pipeline
        pipeline = codepipeline.Pipeline(
            self,
            "DndApiPipeline",
            pipeline_name=f"dnd-api-{deployment_env}",
            pipeline_type=codepipeline.PipelineType.V2,
            stages=[
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        codepipeline_actions.CodeStarConnectionsSourceAction(
                            action_name="GitHub_Source",
                            owner=github_owner,
                            repo=github_repo,
                            branch=github_branch,
                            connection_arn=github_connection_arn,
                            output=source_artifact,
                        )
                    ],
                ),
                codepipeline.StageProps(
                    stage_name="Build",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name="Build_Lambda",
                            project=build_project,
                            input=source_artifact,
                            outputs=[build_artifact],
                        )
                    ],
                ),
                codepipeline.StageProps(
                    stage_name="Deploy",
                    actions=[
                        codepipeline_actions.CodeBuildAction(
                            action_name=f"Deploy_Lambda_{deployment_env}",
                            project=self._create_deploy_project(lambda_function_name),
                            input=build_artifact,
                        )
                    ],
                ),
            ],
        )

        CfnOutput(
            self,
            "PipelineName",
            value=pipeline.pipeline_name,
            description=f"CodePipeline name for {deployment_env}",
            export_name=f"DndApiPipelineName-{deployment_env}",
        )

    def _create_build_project(
        self, lambda_function_name: str
    ) -> codebuild.PipelineProject:
        """Build project: installs dependencies and zips the deployment package."""

        project = codebuild.PipelineProject(
            self,
            "DndApiBuildProject",
            project_name=f"dnd-api-build-{self.deployment_env}",
            build_spec=codebuild.BuildSpec.from_source_filename("cdk/buildspec.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxArmBuildImage.AMAZON_LINUX_2_STANDARD_3_0,
                compute_type=codebuild.ComputeType.SMALL,
            ),
            description=f"Build D&D API Lambda package - {self.deployment_env}",
        )

        return project

    def _create_deploy_project(
        self, lambda_function_name: str
    ) -> codebuild.PipelineProject:
        """Deploy project: calls update-function-code with the built zip."""

        project = codebuild.PipelineProject(
            self,
            "DndApiDeployProject",
            project_name=f"dnd-api-deploy-{self.deployment_env}",
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": "0.2",
                    "phases": {
                        "build": {
                            "commands": [
                                f"aws lambda update-function-code "
                                f"--function-name {lambda_function_name} "
                                f"--zip-file fileb://lambda.zip "
                                f"--architectures arm64"
                            ]
                        }
                    },
                }
            ),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxArmBuildImage.AMAZON_LINUX_2_STANDARD_3_0,
                compute_type=codebuild.ComputeType.SMALL,
            ),
            description=f"Deploy D&D API Lambda - {self.deployment_env}",
        )

        # Grant permission to update the specific Lambda function
        project.add_to_role_policy(
            iam.PolicyStatement(
                actions=["lambda:UpdateFunctionCode"],
                resources=[
                    f"arn:aws:lambda:{self.region}:{self.account}:function:{lambda_function_name}"
                ],
            )
        )

        return project
