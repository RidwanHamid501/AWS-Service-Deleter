from aws_clients import (
    rds, ec2, ecs, redshift,
    elasticache, elbv2, ecr,
    amplify, secrets_manager, sns,
    sfn, lambda_client, s3
)
from prefix_filter import get_resources_with_prefix
from logging_config import logger


def delete_rds_instances(prefix):
    instance_ids = get_resources_with_prefix(
        rds, prefix, 'DBInstances', 'DBInstanceIdentifier')

    if instance_ids:
        for instance_id in instance_ids:
            logger.info(f"Deleting RDS instance: {instance_id}")
            rds.delete_db_instance(
                DBInstanceIdentifier=instance_id,
                SkipFinalSnapshot=True
            )
        logger.info(f"Deleted RDS instances: {instance_ids}")
    else:
        logger.info(f"No RDS instances found with prefix '{prefix}'")


def delete_ec2_instances(prefix):
    instance_ids = get_resources_with_prefix(
        ec2, prefix, 'Reservations', 'InstanceId', service_type='ec2')

    if instance_ids:
        for instance_id in instance_ids:
            logger.info(f"Terminating EC2 instance: {instance_id}")
            ec2.terminate_instances(InstanceIds=[instance_id])
        logger.info(f"Terminated EC2 instances: {instance_ids}")
    else:
        logger.info(f"No EC2 instances found with prefix '{prefix}'")


def delete_security_groups(prefix):
    security_group_ids = get_resources_with_prefix(
        ec2, prefix, 'SecurityGroups', 'GroupId', service_type='security_group')

    if security_group_ids:
        for group_id in security_group_ids:
            logger.info(f"Deleting Security Group: {group_id}")
            ec2.delete_security_group(GroupId=group_id)
        logger.info(f"Deleted Security Groups: {security_group_ids}")
    else:
        logger.info(f"No Security Groups found with prefix '{prefix}'")


def delete_ecs_clusters(prefix):
    cluster_arns = get_resources_with_prefix(
        ecs, prefix, 'clusterArns', '', service_type='ecs')

    if cluster_arns:
        for cluster_arn in cluster_arns:
            logger.info(f"Deleting ECS cluster: {cluster_arn}")
            ecs.delete_cluster(cluster=cluster_arn)
        logger.info(f"Deleted ECS clusters: {cluster_arns}")
    else:
        logger.info(f"No ECS clusters found with prefix '{prefix}'")


def delete_redshift_clusters(prefix):
    cluster_ids = get_resources_with_prefix(
        redshift, prefix, 'Clusters', 'ClusterIdentifier', service_type='redshift')

    if cluster_ids:
        for cluster_id in cluster_ids:
            logger.info(f"Deleting Redshift cluster: {cluster_id}")
            redshift.delete_cluster(
                ClusterIdentifier=cluster_id,
                SkipFinalClusterSnapshot=True
            )
        logger.info(f"Deleted Redshift clusters: {cluster_ids}")
    else:
        logger.info(f"No Redshift clusters found with prefix '{prefix}'")


def delete_vpcs(prefix):
    vpc_ids = get_resources_with_prefix(
        ec2, prefix, 'Vpcs', 'VpcId', service_type='vpc')

    if vpc_ids:
        for vpc_id in vpc_ids:
            logger.info(f"Deleting resources in VPC: {vpc_id}")

            igws = ec2.describe_internet_gateways(
                Filters=[{'Name': 'attachment.vpc-id', 'Values': [vpc_id]}]
            )['InternetGateways']
            for igw in igws:
                igw_id = igw['InternetGatewayId']
                logger.info(
                    f"Detaching and deleting internet gateway: {igw_id}")
                ec2.detach_internet_gateway(
                    InternetGatewayId=igw_id, VpcId=vpc_id)
                ec2.delete_internet_gateway(InternetGatewayId=igw_id)

            subnets = ec2.describe_subnets(
                Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['Subnets']
            for subnet in subnets:
                subnet_id = subnet['SubnetId']
                logger.info(f"Deleting subnet: {subnet_id}")
                ec2.delete_subnet(SubnetId=subnet_id)

            route_tables = ec2.describe_route_tables(
                Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['RouteTables']
            for rt in route_tables:
                if not rt['Associations'][0]['Main']:
                    rt_id = rt['RouteTableId']
                    logger.info(f"Deleting route table: {rt_id}")
                    ec2.delete_route_table(RouteTableId=rt_id)

            network_interfaces = ec2.describe_network_interfaces(
                Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['NetworkInterfaces']
            for eni in network_interfaces:
                eni_id = eni['NetworkInterfaceId']
                logger.info(f"Deleting network interface: {eni_id}")
                ec2.delete_network_interface(NetworkInterfaceId=eni_id)

            logger.info(f"Deleting VPC: {vpc_id}")
            ec2.delete_vpc(VpcId=vpc_id)
        logger.info(f"Deleted VPCs: {vpc_ids}")
    else:
        logger.info(f"No VPCs found with prefix '{prefix}'")


def delete_elasticache_clusters(prefix):
    cluster_ids = get_resources_with_prefix(
        elasticache, prefix, 'CacheClusters', 'CacheClusterId', service_type='elasticache')

    if cluster_ids:
        for cluster_id in cluster_ids:
            logger.info(f"Deleting ElastiCache cluster: {cluster_id}")
            elasticache.delete_cache_cluster(
                CacheClusterId=cluster_id
            )
        logger.info(f"Deleted ElastiCache clusters: {cluster_ids}")
    else:
        logger.info(f"No ElastiCache clusters found with prefix '{prefix}'")


def delete_load_balancers(prefix):
    lb_arns = get_resources_with_prefix(
        elbv2, prefix, 'LoadBalancers', 'LoadBalancerArn', service_type='elbv2')

    if lb_arns:
        for lb_arn in lb_arns:
            logger.info(f"Deleting Load Balancer: {lb_arn}")
            elbv2.delete_load_balancer(LoadBalancerArn=lb_arn)
        logger.info(f"Deleted Load Balancers: {lb_arns}")
    else:
        logger.info(f"No Load Balancers found with prefix '{prefix}'")


def delete_target_groups(prefix):
    target_group_arns = get_resources_with_prefix(
        elbv2, prefix, 'TargetGroups', 'TargetGroupArn', service_type='elbv2b')

    if target_group_arns:
        for target_group_arn in target_group_arns:
            logger.info(f"Deleting Target Group: {target_group_arn}")
            elbv2.delete_target_group(TargetGroupArn=target_group_arn)
        logger.info(f"Deleted Target Groups: {target_group_arns}")
    else:
        logger.info(f"No Target Groups found with prefix '{prefix}'")


def delete_ecr_repositories(prefix):
    repository_names = get_resources_with_prefix(
        ecr, prefix, 'repositories', 'repositoryName', service_type='ecr')

    if repository_names:
        for repo_name in repository_names:
            logger.info(f"Deleting ECR repository: {repo_name}")
            ecr.delete_repository(
                repositoryName=repo_name,
                force=True
            )
        logger.info(f"Deleted ECR repositories: {repository_names}")
    else:
        logger.info(f"No ECR repositories found with prefix '{prefix}'")


def delete_amplify_apps(prefix):
    app_ids = get_resources_with_prefix(
        amplify, prefix, 'apps', 'appId', service_type='amplify')

    if app_ids:
        for app_id in app_ids:
            logger.info(f"Deleting Amplify app: {app_id}")
            amplify.delete_app(appId=app_id)
        logger.info(f"Deleted Amplify apps: {app_ids}")
    else:
        logger.info(f"No Amplify apps found with prefix '{prefix}'")


def delete_sns_topics(prefix):
    topic_arns = get_resources_with_prefix(
        sns, prefix, 'Topics', 'TopicArn', service_type='sns')

    if topic_arns:
        for topic_arn in topic_arns:
            logger.info(f"Deleting SNS topic: {topic_arn}")
            sns.delete_topic(TopicArn=topic_arn)
        logger.info(f"Deleted SNS topics: {topic_arns}")
    else:
        logger.info(f"No SNS topics found with prefix '{prefix}'")


def delete_step_functions(prefix):
    state_machine_arns = get_resources_with_prefix(
        sfn, prefix, 'stateMachines', 'stateMachineArn', service_type='stepfunctions')

    if state_machine_arns:
        for arn in state_machine_arns:
            logger.info(f"Deleting Step Function state machine: {arn}")
            sfn.delete_state_machine(stateMachineArn=arn)
        logger.info(f"Deleted Step Functions state machines: {
                    state_machine_arns}")
    else:
        logger.info(
            f"No Step Function state machines found with prefix '{prefix}'")


def delete_lambda_functions(prefix):
    function_names = get_resources_with_prefix(
        lambda_client, prefix, 'Functions', 'FunctionName', service_type='lambda')

    if function_names:
        for function_name in function_names:
            logger.info(f"Deleting Lambda function: {function_name}")
            lambda_client.delete_function(FunctionName=function_name)
        logger.info(f"Deleted Lambda functions: {function_names}")
    else:
        logger.info(f"No Lambda functions found with prefix '{prefix}'")


def delete_s3_buckets(prefix):
    bucket_names = get_resources_with_prefix(
        s3, prefix, 'Buckets', 'Name', service_type='s3')

    if bucket_names:
        for bucket_name in bucket_names:
            logger.info(f"Deleting S3 bucket: {bucket_name}")
            s3.delete_bucket(Bucket=bucket_name)
        logger.info(f"Deleted S3 buckets: {bucket_names}")
    else:
        logger.info(f"No S3 buckets found with prefix '{prefix}'")


if __name__ == "__main__":
    prefix = 'c14'
    delete_ecs_clusters(prefix)
    delete_lambda_functions(prefix)
    delete_step_functions(prefix)
    delete_sns_topics(prefix)
    delete_amplify_apps(prefix)
    delete_ecr_repositories(prefix)
    delete_load_balancers(prefix)
    delete_target_groups(prefix)
    delete_ec2_instances(prefix)
    delete_elasticache_clusters(prefix)
    delete_rds_instances(prefix)
    delete_redshift_clusters(prefix)
    delete_s3_buckets(prefix)
    delete_security_groups(prefix)
    delete_vpcs(prefix)
