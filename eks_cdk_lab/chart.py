from aws_cdk import core as cdk
from aws_cdk import aws_eks as eks


class ChartStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, cluster: str, opts: dict, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.opts = opts
        self.cluster = cluster

        eks.HelmChart(self, opts["id"],
                      cluster=cluster,
                      chart=opts["chart_name"],
                      repository=opts["repository"],
                      namespace=opts["namespace"],
                      values=opts["values"])
