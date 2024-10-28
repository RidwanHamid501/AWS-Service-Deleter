# Cloud Service Deletion

Python script that deletes AWS resources with a specified prefix.

## Prerequisites

- AWS CLI installed on your machine
- `aws configure` run, setting up your machine with a default profile and AWS security credentials
- Install the required packages using pip:

```sh
pip3 install -r requirements.txt
```

## Usage

To delete AWS resources with a given prefix, use the `delete_services.py` script. The script supports both planning and execution modes.

### Command Line Arguments

- `--prefix`: **(Required)** The prefix for filtering AWS resources.
- `--execute`: **(Optional)** Run in execute mode to actually delete the resources. Default is plan mode.
- Resource-specific flags: **(Optional)** Use these flags to specify which resources to delete. You can use multiple flags to delete multiple types of resources.

### Supported Resource Flags

- `--ecs`: Delete ECS clusters
- `--lambda`: Delete Lambda functions
- `--step`: Delete Step Function state machines
- `--sns`: Delete SNS topics
- `--amplify`: Delete Amplify apps
- `--ecr`: Delete ECR repositories
- `--elbv2`: Delete Load Balancers
- `--tg`: Delete Target Groups
- `--ec2`: Delete EC2 instances
- `--elasticache`: Delete ElastiCache clusters
- `--rds`: Delete RDS instances
- `--redshift`: Delete Redshift clusters
- `--s3`: Delete S3 buckets
- `--sg`: Delete Security Groups
- `--vpc`: Delete VPCs

### Examples

#### Plan Mode (Default)

To plan the deletion of ECS clusters and S3 buckets with a prefix `test`:

```sh
python3 delete_services.py --prefix c14 --ec2 --s3
```

#### Execute Mode

To actually delete ECS clusters and S3 buckets with a prefix `test`:

```sh
python3 delete_services.py --prefix c14 --ecs --s3 --execute
```

## Notes

- The `Name`s of VPCs and Security Groups must include the given prefix (if not already) in order to be matched and deleted by this script.
- The VPCs and Security Groups may error if their dependencies are in the process of deleting. If this happens, simply wait for a while and rerun the script to ensure all dependent resources are fully deleted before attempting to delete again.
- The `delete_compact.py` file holds 2 variables with function parameters enabling it to run each service in one function. For simplicity, use `delete_services.py`.
