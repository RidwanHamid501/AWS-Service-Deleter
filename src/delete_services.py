from aws_clients import (
    rds, ec2, ecs, redshift,
    elasticache, elbv2, ecr,
    amplify, sns, sfn,
    lambda_client, s3
)
from prefix_filter import get_resources_with_prefix
from logging_config import get_logger
import argparse


def delete_ecs_clusters(prefix, logger, is_execute=False):
    cluster_arns = get_resources_with_prefix(
        ecs, prefix, 'clusterArns', '', service_type='ecs', method='list_clusters')

    if cluster_arns:
        for cluster_arn in cluster_arns:
            logger.info(f"Deleting ECS cluster: {cluster_arn}")
            if is_execute:
                try:
                    ecs.delete_cluster(cluster=cluster_arn)
                except Exception as e:
                    logger.error(
                        f"Failed to delete ECS cluster: {cluster_arn} - {e}")
                    cluster_arns.remove(cluster_arn)
    else:
        logger.info(f"No ECS clusters found with prefix '{prefix}'")


def delete_lambda_functions(prefix, logger, is_execute=False):
    function_names = get_resources_with_prefix(
        lambda_client, prefix, 'Functions', 'FunctionName', service_type='lambda', method='list_functions')

    if function_names:
        for function_name in function_names:
            logger.info(f"Deleting Lambda function: {function_name}")
            if is_execute:
                try:
                    lambda_client.delete_function(FunctionName=function_name)
                except Exception as e:
                    logger.error(
                        f"Failed to delete Lambda function: {function_name} - {e}")
                    function_names.remove(function_name)
    else:
        logger.info(f"No Lambda functions found with prefix '{prefix}'")


def delete_step_functions(prefix, logger, is_execute=False):
    state_machine_arns = get_resources_with_prefix(
        sfn, prefix, 'stateMachines', 'stateMachineArn', service_type='stepfunctions', method='list_state_machines')

    if state_machine_arns:
        for arn in state_machine_arns:
            logger.info(f"Deleting Step Function state machine: {arn}")
            if is_execute:
                try:
                    sfn.delete_state_machine(stateMachineArn=arn)
                except Exception as e:
                    logger.error(
                        f"Failed to delete Step Function state machine: {arn} - {e}")
                    state_machine_arns.remove(arn)
    else:
        logger.info(
            f"No Step Function state machines found with prefix '{prefix}'")


def delete_sns_topics(prefix, logger, is_execute=False):
    topic_arns = get_resources_with_prefix(
        sns, prefix, 'Topics', 'TopicArn', service_type='sns', method='list_topics')

    if topic_arns:
        for topic_arn in topic_arns:
            logger.info(f"Deleting SNS topic: {topic_arn}")
            if is_execute:
                try:
                    sns.delete_topic(TopicArn=topic_arn)
                except Exception as e:
                    logger.error(
                        f"Failed to delete SNS topic: {topic_arn} - {e}")
                    topic_arns.remove(topic_arn)
    else:
        logger.info(f"No SNS topics found with prefix '{prefix}'")


def delete_amplify_apps(prefix, logger, is_execute=False):
    app_ids = get_resources_with_prefix(
        amplify, prefix, 'apps', 'appId', service_type='amplify', method='list_apps')

    if app_ids:
        for app_id in app_ids:
            logger.info(f"Deleting Amplify app: {app_id}")
            if is_execute:
                try:
                    amplify.delete_app(appId=app_id)
                except Exception as e:
                    logger.error(
                        f"Failed to delete Amplify app: {app_id} - {e}")
                    app_ids.remove(app_id)
    else:
        logger.info(f"No Amplify apps found with prefix '{prefix}'")


def delete_ecr_repositories(prefix, logger, is_execute=False):
    repository_names = get_resources_with_prefix(
        ecr, prefix, 'repositories', 'repositoryName', service_type='ecr', method='describe_repositories')

    if repository_names:
        for repo_name in repository_names:
            logger.info(f"Deleting ECR repository: {repo_name}")
            if is_execute:
                try:
                    ecr.delete_repository(
                        repositoryName=repo_name,
                        force=True
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to delete ECR repository: {repo_name} - {e}")
                    repository_names.remove(repo_name)
    else:
        logger.info(f"No ECR repositories found with prefix '{prefix}'")


def delete_load_balancers(prefix, logger, is_execute=False):
    lb_arns = get_resources_with_prefix(
        elbv2, prefix, 'LoadBalancers', 'LoadBalancerArn', service_type='elbv2', method='describe_load_balancers')

    if lb_arns:
        for lb_arn in lb_arns:
            logger.info(f"Deleting Load Balancer: {lb_arn}")
            if is_execute:
                try:
                    elbv2.delete_load_balancer(LoadBalancerArn=lb_arn)
                except Exception as e:
                    logger.error(
                        f"Failed to delete Load Balancer: {lb_arn} - {e}")
                    lb_arns.remove(lb_arn)
    else:
        logger.info(f"No Load Balancers found with prefix '{prefix}'")


def delete_target_groups(prefix, logger, is_execute=False):
    target_group_arns = get_resources_with_prefix(
        elbv2, prefix, 'TargetGroups', 'TargetGroupArn', service_type='elbv2b', method='describe_target_groups')

    if target_group_arns:
        for target_group_arn in target_group_arns:
            logger.info(f"Deleting Target Group: {target_group_arn}")
            if is_execute:
                try:
                    elbv2.delete_target_group(TargetGroupArn=target_group_arn)
                except Exception as e:
                    logger.error(
                        f"Failed to delete Target Group: {target_group_arn} - {e}")
                    target_group_arns.remove(target_group_arn)
    else:
        logger.info(f"No Target Groups found with prefix '{prefix}'")


def delete_ec2_instances(prefix, logger, is_execute=False):
    instance_ids = get_resources_with_prefix(
        ec2, prefix, 'Reservations', 'InstanceId', service_type='ec2', method='')

    if instance_ids:
        for instance_id in instance_ids:
            logger.info(f"Terminating EC2 instance: {instance_id}")
            if is_execute:
                try:
                    instance_state = ec2.describe_instances(InstanceIds=[instance_id])[
                        'Reservations'][0]['Instances'][0]['State']['Name']
                    if instance_state != 'terminated':
                        ec2.terminate_instances(InstanceIds=[instance_id])
                    else:
                        logger.info(
                            f"Instance {instance_id} is already terminated.")
                except Exception as e:
                    logger.error(
                        f"Failed to terminate EC2 instance: {instance_id} - {e}")
                    instance_ids.remove(instance_id)
    else:
        logger.info(f"No EC2 instances found with prefix '{prefix}'")


def delete_elasticache_clusters(prefix, logger, is_execute=False):
    cluster_ids = get_resources_with_prefix(
        elasticache, prefix, 'CacheClusters', 'CacheClusterId', service_type='elasticache', method='describe_cache_clusters')

    if cluster_ids:
        for cluster_id in cluster_ids:
            logger.info(f"Deleting ElastiCache cluster: {cluster_id}")
            if is_execute:
                try:
                    elasticache.delete_cache_cluster(
                        CacheClusterId=cluster_id
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to delete ElastiCache cluster: {cluster_id} - {e}")
                    cluster_ids.remove(cluster_id)
    else:
        logger.info(f"No ElastiCache clusters found with prefix '{prefix}'")


def delete_rds_instances(prefix, logger, is_execute=False):
    instance_ids = get_resources_with_prefix(
        rds, prefix, 'DBInstances', 'DBInstanceIdentifier', service_type='rds', method='describe_db_instances')

    if instance_ids:
        for instance_id in instance_ids:
            logger.info(f"Deleting RDS instance: {instance_id}")
            if is_execute:
                try:
                    rds.delete_db_instance(
                        DBInstanceIdentifier=instance_id,
                        SkipFinalSnapshot=True
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to delete RDS instance: {instance_id} - {e}")
                    instance_ids.remove(instance_id)
    else:
        logger.info(f"No RDS instances found with prefix '{prefix}'")


def delete_redshift_clusters(prefix, logger,  is_execute=False):
    cluster_ids = get_resources_with_prefix(
        redshift, prefix, 'Clusters', 'ClusterIdentifier', service_type='redshift', method='describe_clusters')

    if cluster_ids:
        for cluster_id in cluster_ids:
            logger.info(f"Deleting Redshift cluster: {cluster_id}")
            if is_execute:
                try:
                    redshift.delete_cluster(
                        ClusterIdentifier=cluster_id,
                        SkipFinalClusterSnapshot=True
                    )
                except Exception as e:
                    logger.error(
                        f"Failed to delete Redshift cluster: {cluster_id} - {e}")
                    cluster_ids.remove(cluster_id)
    else:
        logger.info(f"No Redshift clusters found with prefix '{prefix}'")


def delete_s3_buckets(prefix, logger,  is_execute=False):
    bucket_names = get_resources_with_prefix(
        s3, prefix, 'Buckets', 'Name', service_type='s3', method='list_buckets')

    if bucket_names:
        for bucket_name in bucket_names:
            logger.info(f"Deleting S3 bucket: {bucket_name}")
            if is_execute:
                try:
                    s3.delete_bucket(Bucket=bucket_name)
                except Exception as e:
                    logger.error(
                        f"Failed to delete S3 bucket: {bucket_name} - {e}")
                    bucket_names.remove(bucket_name)
    else:
        logger.info(f"No S3 buckets found with prefix '{prefix}'")


def delete_security_groups(prefix, logger, is_execute=False):
    security_group_ids = get_resources_with_prefix(
        ec2, prefix, 'SecurityGroups', 'GroupId', service_type='security_group', method='describe_security_groups')

    if security_group_ids:
        for group_id in security_group_ids:
            logger.info(f"Deleting Security Group: {group_id}")
            if is_execute:
                try:
                    ec2.delete_security_group(GroupId=group_id)
                except Exception as e:
                    logger.error(
                        f"Failed to delete Security Group: {group_id} - {e}")
                    security_group_ids.remove(group_id)
    else:
        logger.info(f"No Security Groups found with prefix '{prefix}'")


def delete_vpcs(prefix, logger,  is_execute=False):
    vpc_ids = get_resources_with_prefix(
        ec2, prefix, 'Vpcs', 'VpcId', service_type='vpc', method='describe_vpcs')

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
                if is_execute:
                    ec2.detach_internet_gateway(
                        InternetGatewayId=igw_id, VpcId=vpc_id)
                    ec2.delete_internet_gateway(InternetGatewayId=igw_id)

            subnets = ec2.describe_subnets(
                Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['Subnets']
            for subnet in subnets:
                subnet_id = subnet['SubnetId']
                logger.info(f"Deleting subnet: {subnet_id}")
                if is_execute:
                    ec2.delete_subnet(SubnetId=subnet_id)

            route_tables = ec2.describe_route_tables(
                Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['RouteTables']
            for rt in route_tables:
                if not rt['Associations'][0]['Main']:
                    rt_id = rt['RouteTableId']
                    logger.info(f"Deleting route table: {rt_id}")
                    if is_execute:
                        ec2.delete_route_table(RouteTableId=rt_id)

            network_interfaces = ec2.describe_network_interfaces(
                Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])['NetworkInterfaces']
            for eni in network_interfaces:
                eni_id = eni['NetworkInterfaceId']
                logger.info(f"Deleting network interface: {eni_id}")
                if is_execute:
                    ec2.delete_network_interface(NetworkInterfaceId=eni_id)

            logger.info(f"Deleting VPC: {vpc_id}")
            if is_execute:
                ec2.delete_vpc(VpcId=vpc_id)
    else:
        logger.info(f"No VPCs found with prefix '{prefix}'")


FUNCTION_MAP = {
    "ecs": delete_ecs_clusters,
    "lambda": delete_lambda_functions,
    "step": delete_step_functions,
    "sns": delete_sns_topics,
    "amplify": delete_amplify_apps,
    "ecr": delete_ecr_repositories,
    "elbv2": delete_load_balancers,
    "tg": delete_target_groups,
    "ec2": delete_ec2_instances,
    "elasticache": delete_elasticache_clusters,
    "rds": delete_rds_instances,
    "redshift": delete_redshift_clusters,
    "s3": delete_s3_buckets,
    "sg": delete_security_groups,
    "vpc": delete_vpcs,
}


def main():
    parser = argparse.ArgumentParser(
        description="Delete AWS resources with a given prefix.")

    parser.add_argument('--prefix', type=str, required=True,
                        help="Prefix for filtering AWS resources.")

    for flag in FUNCTION_MAP.keys():
        parser.add_argument(f'--{flag}', action='store_true',
                            help=f"Delete {flag.replace('_', ' ')} resources.")

    parser.add_argument('--execute', action='store_true',
                        help="Run in execute mode to actually delete the resources. Default is plan mode.")

    args = parser.parse_args()

    is_execute = args.execute or False
    logger = get_logger(is_execute)

    for flag, func in FUNCTION_MAP.items():
        if getattr(args, flag):
            try:
                if is_execute:
                    logger.info(f"Executing {flag} deletion with prefix '{
                                args.prefix}'")
                    func(args.prefix, logger, is_execute)
                else:
                    logger.info(f"Planning to delete {
                                flag} resources with prefix '{args.prefix}'")
                    func(args.prefix, logger, is_execute)
            except Exception as e:
                logger.error(f"Failed to delete {flag} resources: {e}")


if __name__ == "__main__":
    main()
