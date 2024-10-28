from aws_clients import (
    rds, ec2, ecs, redshift,
    elasticache, elbv2, ecr,
    amplify, sns, sfn,
    lambda_client, s3
)
from prefix_filter import get_resources_with_prefix
from logging_config import logger
import argparse


METHODS_REQUIRING_LIST = {"terminate_instances", "delete_cache_cluster",
                          "delete_db_instance", "delete_load_balancer", "delete_target_group"}


def delete_resources(params, prefix, is_execute=False):
    """Generalized function to delete resources or plan deletion using AWS clients."""

    # Fetch resources matching the prefix
    resources = get_resources_with_prefix(
        params["client"], prefix, params["resource_key"], params["identifier_key"],
        service_type=params["service_type"], method=params["method"]
    )

    if not resources:
        logger.info(f"No {params['resource_name']
                          }s found with prefix '{prefix}'")
        return

    if is_execute:
        try:
            # Prepare deletion method
            delete_method = getattr(
                params["client"], params["delete_method_name"])
            delete_params_key = params["delete_params_key"]
            requires_list = params.get(
                "requires_list", params["delete_method_name"] in METHODS_REQUIRING_LIST)

            # Execute the deletion
            for resource in resources:
                logger.info(f"Deleting {params['resource_name']}: {resource}")

                # Pass list if needed, else pass single value
                delete_method(
                    **{delete_params_key: [resource] if requires_list else resource})

            logger.info(f"Deleted {params['resource_name']}s: {resources}")
        except Exception as e:
            logger.error(f"Failed to delete {params['resource_name']}s: {e}")
    else:
        # Planning mode, log the resources that would be deleted
        logger.info(f"Planning to delete {
                    params['resource_name']}s: {resources}")


def delete_vpcs(prefix, is_execute):
    vpc_ids = get_resources_with_prefix(
        ec2, prefix, 'Vpcs', 'VpcId', service_type='vpc', method='describe_vpcs')

    if vpc_ids:
        if is_execute:
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
            logger.info(f"Planning to delete VPCs: {vpc_ids}")
    else:
        logger.info(f"No VPCs found with prefix '{prefix}'")


FUNCTION_MAP = {
    "ecs": {
        "client": ecs,
        "resource_key": "clusterArns",
        "identifier_key": "",
        "service_type": "ecs",
        "method": "list_clusters",
        "resource_name": "ECS cluster",
        "delete_method_name": "delete_cluster",
        "delete_params_key": "cluster"
    },
    "lambda": {
        "client": lambda_client,
        "resource_key": "Functions",
        "identifier_key": "FunctionName",
        "service_type": "lambda",
        "method": "list_functions",
        "resource_name": "Lambda function",
        "delete_method_name": "delete_function",
        "delete_params_key": "FunctionName"
    },
    "step": {
        "client": sfn,
        "resource_key": "stateMachines",
        "identifier_key": "stateMachineArn",
        "service_type": "stepfunctions",
        "method": "list_state_machines",
        "resource_name": "Step Function state machine",
        "delete_method_name": "delete_state_machine",
        "delete_params_key": "stateMachineArn"
    },
    "sns": {
        "client": sns,
        "resource_key": "Topics",
        "identifier_key": "TopicArn",
        "service_type": "sns",
        "method": "list_topics",
        "resource_name": "SNS topic",
        "delete_method_name": "delete_topic",
        "delete_params_key": "TopicArn"
    },
    "amplify": {
        "client": amplify,
        "resource_key": "apps",
        "identifier_key": "appId",
        "service_type": "amplify",
        "method": "list_apps",
        "resource_name": "Amplify app",
        "delete_method_name": "delete_app",
        "delete_params_key": "appId"
    },
    "ecr": {
        "client": ecr,
        "resource_key": "repositories",
        "identifier_key": "repositoryName",
        "service_type": "ecr",
        "method": "describe_repositories",
        "resource_name": "ECR repository",
        "delete_method_name": "delete_repository",
        "delete_params_key": "repositoryName"
    },
    "elbv2": {
        "client": elbv2,
        "resource_key": "LoadBalancers",
        "identifier_key": "LoadBalancerArn",
        "service_type": "elbv2",
        "method": "describe_load_balancers",
        "resource_name": "Load Balancer",
        "delete_method_name": "delete_load_balancer",
        "delete_params_key": "LoadBalancerArn"
    },
    "tg": {
        "client": elbv2,
        "resource_key": "TargetGroups",
        "identifier_key": "TargetGroupArn",
        "service_type": "elbv2",
        "method": "describe_target_groups",
        "resource_name": "Target Group",
        "delete_method_name": "delete_target_group",
        "delete_params_key": "TargetGroupArn"
    },
    "ec2": {
        "client": ec2,
        "resource_key": "Reservations",
        "identifier_key": "InstanceId",
        "service_type": "ec2",
        "method": "describe_instances",
        "resource_name": "EC2 instance",
        "delete_method_name": "terminate_instances",
        "delete_params_key": "InstanceId"
    },
    "elasticache": {
        "client": elasticache,
        "resource_key": "CacheClusters",
        "identifier_key": "CacheClusterId",
        "service_type": "elasticache",
        "method": "describe_cache_clusters",
        "resource_name": "ElastiCache cluster",
        "delete_method_name": "delete_cache_cluster",
        "delete_params_key": "CacheClusterId"
    },
    "rds": {
        "client": rds,
        "resource_key": "DBInstances",
        "identifier_key": "DBInstanceIdentifier",
        "service_type": "rds",
        "method": "describe_db_instances",
        "resource_name": "RDS instance",
        "delete_method_name": "delete_db_instance",
        "delete_params_key": "DBInstanceIdentifier"
    },
    "redshift": {
        "client": redshift,
        "resource_key": "Clusters",
        "identifier_key": "ClusterIdentifier",
        "service_type": "redshift",
        "method": "describe_clusters",
        "resource_name": "Redshift cluster",
        "delete_method_name": "delete_cluster",
        "delete_params_key": "ClusterIdentifier"
    },
    "sg": {
        "client": ec2,
        "resource_key": "SecurityGroups",
        "identifier_key": "GroupId",
        "service_type": "security_group",
        "method": "describe_security_groups",
        "resource_name": "Security Group",
        "delete_method_name": "delete_security_group",
        "delete_params_key": "GroupId"
    },
    "s3": {
        "client": s3,
        "resource_key": "Buckets",
        "identifier_key": "Name",
        "service_type": "s3",
        "method": "list_buckets",
        "resource_name": "S3 bucket",
        "delete_method_name": "delete_bucket",
        "delete_params_key": "Bucket"
    },
    "vpc": {
        "client": ec2,
        "resource_key": "Vpcs",
        "identifier_key": "VpcId",
        "service_type": "vpc",
        "method": "describe_vpcs",
        "resource_name": "VPC",
        "delete_method_name": "delete_vpc",
        "delete_params_key": "VpcId"
    }
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

    is_execute = args.execute

    for flag, params in FUNCTION_MAP.items():
        if getattr(args, flag):
            if is_execute:
                logger.info(f"Executing {params['resource_name']} deletion with prefix '{
                            args.prefix}'")
            else:
                logger.info(f"Planning to delete {
                            params['resource_name']}s with prefix '{args.prefix}'")
            if flag != "vpc":
                delete_resources(params, args.prefix, is_execute)
            else:
                delete_vpcs(args.prefix, is_execute)


if __name__ == "__main__":
    main()
