#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_aws.aws import AwsProvider, s3
from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket

class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        AwsProvider(self, 'AWS', region='us-east-1')
        S3Bucket(self, 'StaticWebsite',
            bucket='static-website',
            website=[s3.S3BucketWebsite(index_document='index.html')]
        )


app = App()
MyStack(app, "static-site")

app.synth()
