import boto3

rds = boto3.client('rds')
ec2 = boto3.client('ec2')
ecs = boto3.client('ecs')
redshift = boto3.client('redshift')
elasticache = boto3.client('elasticache')
elbv2 = boto3.client('elbv2')
ecr = boto3.client('ecr')
amplify = boto3.client('amplify')
secrets_manager = boto3.client('secretsmanager')
sns = boto3.client('sns')
sfn = boto3.client('stepfunctions')
lambda_client = boto3.client('lambda')
s3 = boto3.client('s3')
