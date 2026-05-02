#!/bin/bash
set -euxo pipefail

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y \
  awscli \
  ca-certificates \
  curl \
  gnupg \
  jq \
  lsb-release \
  unzip

mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  > /etc/apt/sources.list.d/docker.list

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

systemctl enable docker
systemctl start docker

mkdir -p /opt/tradingagents
cat >/etc/nim.env <<EOF
NIM_IMAGE=${NIM_IMAGE}
NIM_PORT=${NIM_PORT}
NIM_CACHE_DIR=${NIM_CACHE_DIR}
NGC_API_KEY_SECRET_ARN=${NGC_API_KEY_SECRET_ARN}
EOF

cat >/usr/local/bin/start-nim.sh <<'EOF'
#!/bin/bash
set -euxo pipefail

source /etc/nim.env

if [[ -z "${NGC_API_KEY_SECRET_ARN}" ]]; then
  echo "NGC_API_KEY_SECRET_ARN is empty; skipping NIM startup." >&2
  exit 0
fi

NGC_API_KEY="$(aws secretsmanager get-secret-value \
  --secret-id "${NGC_API_KEY_SECRET_ARN}" \
  --query SecretString \
  --output text)"

mkdir -p "${NIM_CACHE_DIR}"

echo "${NGC_API_KEY}" | docker login nvcr.io --username '$oauthtoken' --password-stdin
docker pull "${NIM_IMAGE}"
docker rm -f nim-llm >/dev/null 2>&1 || true

docker run -d \
  --name nim-llm \
  --restart unless-stopped \
  --gpus all \
  --shm-size=16g \
  -p "${NIM_PORT}:8000" \
  -v "${NIM_CACHE_DIR}:/opt/nim/.cache" \
  -e NGC_API_KEY="${NGC_API_KEY}" \
  "${NIM_IMAGE}"
EOF

chmod +x /usr/local/bin/start-nim.sh

cat >/etc/systemd/system/nim.service <<'EOF'
[Unit]
Description=NVIDIA NIM Service
After=docker.service network-online.target
Wants=network-online.target
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/local/bin/start-nim.sh
ExecStop=/usr/bin/docker rm -f nim-llm
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable nim.service
systemctl start nim.service || true
