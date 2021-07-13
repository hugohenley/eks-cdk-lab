#!/usr/bin/env python3
import os
import yaml

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from eks_cdk_lab.eks_cdk_lab_stack import EksCdkLabStack
from eks_cdk_lab.chart import ChartStack


app = core.App()
# eks_stack = EksCdkLabStack(app, "EksCdkLabStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    # env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=core.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    # )

with open("configs/clusters.yaml", "r") as f:
    clusters = yaml.load(f, Loader=yaml.FullLoader)

eks_stacks = []

for cluster in clusters["clusters"]:
    eks_stack = EksCdkLabStack(app, clusters["clusters"][cluster]["id"], opts=clusters["clusters"][cluster])
    eks_stacks.append(eks_stack)

with open("configs/charts.yaml", "r") as f:
    charts = yaml.load(f, Loader=yaml.FullLoader)

for chart in charts["default"]:
    for eks_stack in eks_stacks:
        ChartStack(app, chart, eks_stack.cluster, charts["default"][chart])


app.synth()
