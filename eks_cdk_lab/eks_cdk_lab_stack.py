from aws_cdk import core as cdk
from aws_cdk import aws_eks as eks
from aws_cdk import aws_ec2 as ec2

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class EksCdkLabStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, opts: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.opts = opts

        cluster = eks.Cluster(self, opts["id"],
                              version=eks.KubernetesVersion.V1_20,
                              default_capacity=opts["default_capacity"]
                              )

        for node_group in opts["node_groups"]:
            cluster.add_nodegroup_capacity(node_group["id"],
                                           instance_types=self.instance_types(node_group["instance_types"]),
                                           min_size=node_group["min_size"],
                                           disk_size=node_group["disk_size"],
                                           ami_type=eks.NodegroupAmiType.AL2_X86_64)

        self.cluster = cluster

    def instance_types(self, instance_types):
        instance_types_objects = []
        for instance_type in instance_types:
            instance_types_objects.append(ec2.InstanceType(instance_type))

        return instance_types_objects
