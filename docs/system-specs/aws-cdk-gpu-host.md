# AWS CDK GPU Host

## Purpose

This stack creates a single GPU inference host for TradingAgents:

- one EC2 GPU instance such as `g6e.xlarge`
- SSM-enabled instance role
- encrypted GP3 root volume
- security group that exposes only the NIM API port to your CIDR
- user data that installs Docker and optionally starts NIM

## Location

- CDK app: `cdk/`
- Stack: `cdk/lib/tradingagents-gpu-host-stack.ts`
- User data template: `cdk/assets/gpu-host-user-data.sh`

## Important constraints

- The stack now defaults to AWS's public SSM parameter for the latest x86_64 Deep Learning Base OSS Nvidia Driver GPU AMI on Amazon Linux 2023.
- NIM startup only happens if you provide a Secrets Manager secret ARN containing the raw NGC API key as `SecretString`.
- The current bootstrap installs Docker, and the default DLAMI already includes the NVIDIA driver stack, container toolkit, Docker, and SSM agent.

## Recommended first deploy shape

- Region: `us-west-2`
- Instance type: `g6e.xlarge`
- Root volume: `250 GiB`
- NIM port: `8000`
- Allowed ingress CIDR: your public IP `/32`
- AMI SSM parameter: `/aws/service/deeplearning/ami/x86_64/base-oss-nvidia-driver-gpu-amazon-linux-2023/latest/ami-id`

## Deploy workflow

From `cdk/`:

1. `npm install`
2. `npx cdk bootstrap aws://ACCOUNT_ID/us-west-2`
3. create a Secrets Manager secret tagged `Project=TradingAgents`
4. `npx cdk deploy --parameters ...`

## Suggested next improvement

Add a deploy script that resolves your public IP automatically and wraps the `cdk deploy` parameters.
