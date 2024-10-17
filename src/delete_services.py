from aws_clients import (
    rds, ec2, ecs, redshift,
    elasticache, elb, ecr,
    amplify, secrets_manager, sns,
    sfn, lambda_client, s3
)
from prefix_filter import get_resources_with_prefix
from logging_config import logger


def delete_rds_instances_with_prefix(prefix):
    instance_ids = get_resources_with_prefix(
        rds, prefix, 'DBInstances', 'DBInstanceIdentifier')

    if instance_ids:
        for instance_id in instance_ids:
            logger.info(f"Deleting RDS instance: {instance_id}")
            # rds.delete_db_instance(
            #     DBInstanceIdentifier=instance_id,
            #     SkipFinalSnapshot=True
            # )
        logger.info(f"Deleted RDS instances: {instance_ids}")
    else:
        logger.info(f"No RDS instances found with prefix '{prefix}'")


def delete_ec2_instances_with_prefix(prefix):
    instance_ids = get_resources_with_prefix(
        ec2, prefix, 'Reservations', 'InstanceId', service_type='ec2')

    if instance_ids:
        for instance_id in instance_ids:
            logger.info(f"Terminating EC2 instance: {instance_id}")
            # ec2.terminate_instances(InstanceIds=[instance_id])
        logger.info(f"Terminated EC2 instances: {instance_ids}")
    else:
        logger.info(f"No EC2 instances found with prefix '{prefix}'")


def delete_ecs_clusters_with_prefix(prefix):
    cluster_arns = get_resources_with_prefix(
        ecs, prefix, 'clusterArns', '', service_type='ecs')

    if cluster_arns:
        for cluster_arn in cluster_arns:
            logger.info(f"Deleting ECS cluster: {cluster_arn}")
            # ecs.delete_cluster(cluster=cluster_arn)
        logger.info(f"Deleted ECS clusters: {cluster_arns}")
    else:
        logger.info(f"No ECS clusters found with prefix '{prefix}'")


def delete_redshift_clusters_with_prefix(prefix):
    cluster_ids = get_resources_with_prefix(
        redshift, prefix, 'Clusters', 'ClusterIdentifier', service_type='redshift')

    if cluster_ids:
        for cluster_id in cluster_ids:
            logger.info(f"Deleting Redshift cluster: {cluster_id}")
            # redshift.delete_cluster(
            #     ClusterIdentifier=cluster_id,
            #     SkipFinalSnapshot=True
            # )
        logger.info(f"Deleted Redshift clusters: {cluster_ids}")
    else:
        logger.info(f"No Redshift clusters found with prefix '{prefix}'")


def delete_vpcs_with_prefix(prefix):
    vpc_ids = get_resources_with_prefix(
        ec2, prefix, 'Vpcs', 'VpcId', service_type='vpc')

    if vpc_ids:
        for vpc_id in vpc_ids:
            logger.info(f"Deleting VPC: {vpc_id}")
            # ec2.delete_vpc(VpcId=vpc_id)
        logger.info(f"Deleted VPCs: {vpc_ids}")
    else:
        logger.info(f"No VPCs found with prefix '{prefix}'")


def delete_elasticache_clusters_with_prefix(prefix):
    cluster_ids = get_resources_with_prefix(
        elasticache, prefix, 'CacheClusters', 'CacheClusterId', service_type='elasticache')

    if cluster_ids:
        for cluster_id in cluster_ids:
            logger.info(f"Deleting ElastiCache cluster: {cluster_id}")
            # elasticache.delete_cache_cluster(
            #     CacheClusterId=cluster_id
            # )
        logger.info(f"Deleted ElastiCache clusters: {cluster_ids}")
    else:
        logger.info(f"No ElastiCache clusters found with prefix '{prefix}'")


def delete_elbs_with_prefix(prefix):
    load_balancer_names = get_resources_with_prefix(
        elb, prefix, 'LoadBalancerDescriptions', 'LoadBalancerName', service_type='elb')

    if load_balancer_names:
        for lb_name in load_balancer_names:
            logger.info(f"Deleting Load Balancer: {lb_name}")
            # elb.delete_load_balancer(LoadBalancerName=lb_name)
        logger.info(f"Deleted Load Balancers: {load_balancer_names}")
    else:
        logger.info(f"No Load Balancers found with prefix '{prefix}'")


def delete_ecr_repositories_with_prefix(prefix):
    repository_names = get_resources_with_prefix(
        ecr, prefix, 'repositories', 'repositoryName', service_type='ecr')

    if repository_names:
        for repo_name in repository_names:
            logger.info(f"Deleting ECR repository: {repo_name}")
            # ecr.delete_repository(
            #     repositoryName=repo_name,
            #     force=True
            # )
        logger.info(f"Deleted ECR repositories: {repository_names}")
    else:
        logger.info(f"No ECR repositories found with prefix '{prefix}'")


def delete_amplify_apps_with_prefix(prefix):
    app_ids = get_resources_with_prefix(
        amplify, prefix, 'apps', 'appId', service_type='amplify')

    if app_ids:
        for app_id in app_ids:
            logger.info(f"Deleting Amplify app: {app_id}")
            # amplify.delete_app(appId=app_id)
        logger.info(f"Deleted Amplify apps: {app_ids}")
    else:
        logger.info(f"No Amplify apps found with prefix '{prefix}'")


def delete_secrets_with_prefix(prefix):
    secret_arns = get_resources_with_prefix(
        secrets_manager, prefix, 'SecretList', 'Name', service_type='secrets')

    if secret_arns:
        for secret_name in secret_arns:
            logger.info(f"Deleting secret: {secret_name}")
            # secrets_manager.delete_secret(SecretId=secret_name, ForceDeleteWithoutRecovery=True)
        logger.info(f"Deleted secrets: {secret_arns}")
    else:
        logger.info(f"No secrets found with prefix '{prefix}'")


def delete_sns_topics_with_prefix(prefix):
    topic_arns = get_resources_with_prefix(
        sns, prefix, 'Topics', 'TopicArn', service_type='sns')

    if topic_arns:
        for topic_arn in topic_arns:
            logger.info(f"Deleting SNS topic: {topic_arn}")
            # sns.delete_topic(TopicArn=topic_arn)
        logger.info(f"Deleted SNS topics: {topic_arns}")
    else:
        logger.info(f"No SNS topics found with prefix '{prefix}'")


def delete_step_functions_with_prefix(prefix):
    state_machine_arns = get_resources_with_prefix(
        sfn, prefix, 'stateMachines', 'stateMachineArn', service_type='stepfunctions')

    if state_machine_arns:
        for arn in state_machine_arns:
            logger.info(f"Deleting Step Function state machine: {arn}")
            # sfn.delete_state_machine(stateMachineArn=arn)
        logger.info(f"Deleted Step Functions state machines: {
                    state_machine_arns}")
    else:
        logger.info(
            f"No Step Function state machines found with prefix '{prefix}'")


def delete_lambda_functions_with_prefix(prefix):
    function_names = get_resources_with_prefix(
        lambda_client, prefix, 'Functions', 'FunctionName', service_type='lambda')

    if function_names:
        for function_name in function_names:
            logger.info(f"Deleting Lambda function: {function_name}")
            # lambda_client.delete_function(FunctionName=function_name)
        logger.info(f"Deleted Lambda functions: {function_names}")
    else:
        logger.info(f"No Lambda functions found with prefix '{prefix}'")


def delete_s3_buckets_with_prefix(prefix):
    bucket_names = get_resources_with_prefix(
        s3, prefix, 'Buckets', 'Name', service_type='s3')

    if bucket_names:
        for bucket_name in bucket_names:
            logger.info(f"Deleting S3 bucket: {bucket_name}")
            # s3.delete_bucket(Bucket=bucket_name)
        logger.info(f"Deleted S3 buckets: {bucket_names}")
    else:
        logger.info(f"No S3 buckets found with prefix '{prefix}'")


if __name__ == "__main__":
    prefix = 'database'
    delete_rds_instances_with_prefix(prefix)
    delete_ec2_instances_with_prefix(prefix)
    delete_ecs_clusters_with_prefix(prefix)
    delete_redshift_clusters_with_prefix(prefix)
    delete_vpcs_with_prefix(prefix)
    delete_elasticache_clusters_with_prefix(prefix)
    delete_elbs_with_prefix(prefix)
    delete_ecr_repositories_with_prefix(prefix)
    delete_amplify_apps_with_prefix(prefix)
    delete_secrets_with_prefix(prefix)
    delete_sns_topics_with_prefix(prefix)
    delete_step_functions_with_prefix(prefix)
    delete_lambda_functions_with_prefix(prefix)
    delete_s3_buckets_with_prefix(prefix)
