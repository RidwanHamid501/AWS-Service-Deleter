def get_resources_with_prefix(client, prefix, resource_key, identifier_key, service_type='rds'):
    if service_type == 'rds':
        resources = client.describe_db_instances()
        items = resources[resource_key]
    elif service_type == 'ec2':
        resources = client.describe_instances()
        items = []
        for reservation in resources[resource_key]:
            items.extend(reservation['Instances'])
    elif service_type == 'security_group':
        resources = client.describe_security_groups()
        items = resources[resource_key]
    elif service_type == 'ecs':
        resources = client.list_clusters()
        items = resources[resource_key]
    elif service_type == 'redshift':
        resources = client.describe_clusters()
        items = resources[resource_key]
    elif service_type == 'vpc':
        resources = client.describe_vpcs()
        items = resources[resource_key]
    elif service_type == 'elasticache':
        resources = client.describe_cache_clusters()
        items = resources[resource_key]
    elif service_type == 'elbv2':
        resources = client.describe_load_balancers()
        items = resources[resource_key]
    elif service_type == 'elbv2b':
        resources = client.describe_target_groups()
        items = resources[resource_key]
    elif service_type == 'ecr':
        resources = client.describe_repositories()
        items = resources[resource_key]
    elif service_type == 'amplify':
        resources = client.list_apps()
        items = resources[resource_key]
    elif service_type == 'secrets':
        resources = client.list_secrets()
        items = resources[resource_key]
    elif service_type == 'sns':
        resources = client.list_topics()
        items = resources[resource_key]
    elif service_type == 'stepfunctions':
        resources = client.list_state_machines()
        items = resources[resource_key]
    elif service_type == 'lambda':
        resources = client.list_functions()
        items = resources[resource_key]
    elif service_type == 's3':
        resources = client.list_buckets()
        items = resources[resource_key]

    resource_ids = []

    if service_type == 'ecs':
        resource_ids = [
            item for item in items if item.split('/')[-1].startswith(prefix)
        ]
    elif service_type == 'ec2' or service_type == 'vpc' or service_type == 'security_group':
        for item in items:
            if 'Tags' in item:
                for tag in item['Tags']:
                    if tag['Key'] == 'Name' and prefix in tag['Value']:
                        resource_ids.append(item[identifier_key])
    elif service_type == 'amplify':
        resource_ids = [
            item[identifier_key]
            for item in items
            if item['name'].startswith(prefix)
        ]
    else:
        resource_ids = [
            item[identifier_key]
            for item in items
            if prefix in item[identifier_key]
        ]

    return resource_ids
