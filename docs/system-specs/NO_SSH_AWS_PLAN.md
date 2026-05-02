# No-SSH AWS Plan for TradingAgents + NVIDIA NIM

## Goal

Bring up a single `g6e` EC2 instance that:

- installs NVIDIA drivers and Docker automatically
- starts a NIM container automatically
- exposes a private or IP-restricted inference endpoint
- can be managed later with AWS Systems Manager instead of SSH

This is the fastest prototype path before building a fuller production setup.

## Architecture

- `EC2 g6e.xlarge` in `us-west-2`
- `Ubuntu 22.04 LTS`
- `200-300 GB gp3` root disk
- `EC2 User Data` bootstraps the machine
- `systemd` keeps NIM running
- `AWS Systems Manager` for remote command execution
- `TradingAgents` runs separately at first, calling NIM over HTTP

## AWS Console Setup

### 1. Account hygiene

- Enable MFA on root
- Create an admin IAM user for daily use
- Enable billing alerts
- Create a budget alert at `$50`

### 2. IAM role for the EC2 instance

Create an instance profile with:

- `AmazonSSMManagedInstanceCore`

Optional later:

- S3 read/write
- Secrets Manager read

### 3. Security group

For the first prototype:

- allow `22` from nowhere if you want true no-SSH
- allow `8000` from your public IP only
- allow `443` outbound
- allow `80` outbound

If you later place TradingAgents on AWS too, lock `8000` down to the app subnet/security group instead of your IP.

### 4. EC2 launch choices

- Region: `us-west-2`
- AMI: `Ubuntu Server 22.04 LTS`
- Instance type: `g6e.xlarge`
- Storage: `250 GB gp3`
- Public IP: enabled for first run
- IAM role: the SSM role above
- User data: use `cloud-init-nim-g6e.yaml`

## First-Run Sequence

1. Launch instance with user data.
2. Wait for cloud-init to finish.
3. Confirm the instance shows up in AWS Systems Manager.
4. Confirm the service is healthy:
   - `http://INSTANCE_IP:8000/v1/health/live`
   - `http://INSTANCE_IP:8000/v1/health/ready`
   - `http://INSTANCE_IP:8000/v1/models`
5. Point TradingAgents at the endpoint.

## Cost Notes

- `g6e` compute stops billing when the instance is stopped.
- `EBS` persists and still costs money while stopped.
- Public IPv4 may also incur cost if attached.
- Keep the instance stopped when idle.

## What still needs implementation

This gets the model server online, but not the trading app integration. We still need to:

- adapt TradingAgents config to use a self-hosted OpenAI-compatible endpoint
- choose a concrete NIM model that fits in `48 GB`
- add a reproducible way to run TradingAgents jobs
- persist outputs and logs
- optionally schedule runs

## Recommended next milestone

After the instance is up:

1. verify NIM works with one direct API call
2. patch TradingAgents to support `base_url` + model name cleanly
3. run one single-ticker end-to-end test
