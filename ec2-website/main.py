#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.aws import AwsProvider
from cdktf_cdktf_provider_aws.vpc import Vpc
from cdktf_cdktf_provider_aws.instance import Instance
from cdktf_cdktf_provider_aws.security_group import SecurityGroup

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        AwsProvider(self, 'AWS', region='us-east-1')

        # Create VPC
        vpc = Vpc(self, 'WebsiteVpc',
            name='website-vpc',
            cidr='10.0.0.0/16',
            azs=["us-east-1a", "us-east-1b"],
            public_subnets=["10.0.1.0/24", "10.0.2.0/24"]
            )
        
        # Create Security Group
        security_group = SecurityGroup(self, 'WebInstanceSG',
            vpc_id=vpc.id,
            ingress=[{
                'from_port': 80,
                'to_port': 80,
                'protocol': 'tcp',
                'cidr_blocks': ['0.0.0.0/0']
            }],
            egress=[{
                'from_port': 0,
                'to_port': 0,
                'protocol': '-1',
                'cidr_blocks': ['0.0.0.0/0']
            }]
        )

        # Read the content of configure.sh to be user data
        with open('configure.sh', 'r') as file:
            user_data = file.read()
        
        ec2_instance = Instance(self, 'Web-Instance',
            ami="ami-0c101f26f147fa7fd",  
            instance_type="t2.micro",
            subnet_id=vpc.public_subnets[0].id,
            vpc_security_group_ids=[security_group.id],
            user_data=user_data
        )

        TerraformOutput(self, "public_ip",
        value=ec2_instance.public_ip,
        )



app = App()
MyStack(app, "ec2-site")

app.synth()
