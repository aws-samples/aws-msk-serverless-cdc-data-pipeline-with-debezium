#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import aws_cdk as cdk

from aws_cdk import (
  Stack,
  aws_msk
)
from constructs import Construct


class MSKClusterPolicyStack(Stack):

  def __init__(self, scope: Construct, construct_id: str, msk_cluster_arn: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    msk_cluster_policy = {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "firehose.amazonaws.com"
          },
          "Action": "kafka:CreateVpcConnection",
          "Resource": msk_cluster_arn
        }
      ]
    }

    cfn_cluster_policy = aws_msk.CfnClusterPolicy(self, 'MSKClusterPolicy',
      cluster_arn=msk_cluster_arn,
      policy=msk_cluster_policy
    )

    cdk.CfnOutput(self, 'MSKClusterPolicyCurrentVersion', value=cfn_cluster_policy.attr_current_version,
      export_name=f'{self.stack_name}-ClusterPolicyCurrentVersion')
    cdk.CfnOutput(self, 'KafkaClusterArn', value=cfn_cluster_policy.cluster_arn,
      export_name=f'{self.stack_name}-KafkaClusterArn')
