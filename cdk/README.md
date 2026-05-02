# TradingAgents CDK

This folder contains the AWS CDK app for provisioning the first GPU inference host used by TradingAgents.

## Commands

```bash
cd cdk
npm install
npx cdk synth
npx cdk diff
npx cdk deploy
```

## First stack

`TradingAgentsGpuHostStack` provisions:

- one GPU EC2 instance
- SSM-managed instance role
- ingress only for the configured NIM API CIDR
- encrypted persistent root volume
- bootstrap user data for Docker and NIM startup

By default, the stack resolves the AMI from AWS's public Deep Learning AMI SSM parameter for the latest x86_64 GPU base image on Amazon Linux 2023.

See `../docs/system-specs/aws-cdk-gpu-host.md` for deployment notes.
