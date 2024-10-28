def get_resources_with_prefix(client, prefix, resource_key, identifier_key, service_type, method):
    if service_type == 'ec2':
        resources = client.describe_instances()
        items = []
        for reservation in resources[resource_key]:
            items.extend(reservation['Instances'])
    else:
        method_to_call = getattr(client, method)
        resources = method_to_call()
        items = resources[resource_key]

    resource_ids = []

    if service_type == 'ecs':
        resource_ids = [
            item for item in items if item.split('/')[-1].startswith(prefix)
        ]
    elif service_type == 'amplify':
        resource_ids = [
            item[identifier_key]
            for item in items
            if item['name'].startswith(prefix)
        ]
    elif service_type in ['ec2', 'vpc', 'security_group']:
        for item in items:
            if 'GroupName' in item:
                if item['GroupName'].startswith(prefix):
                    resource_ids.append(item[identifier_key])
            if 'Tags' in item:
                for tag in item['Tags']:
                    if tag['Key'] == 'Name' and tag['Value'].startswith(prefix):
                        resource_ids.append(item[identifier_key])
    else:
        resource_ids = [
            item[identifier_key]
            for item in items
            if prefix in item[identifier_key]
        ]

    return resource_ids
