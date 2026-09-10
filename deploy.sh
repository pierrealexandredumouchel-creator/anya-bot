#!/bin/bash

# Adresse du VPS piotr
SERVER="67.215.13.169"

echo "[1] Packaging Anya..."
rm -f anya.tar.gz
tar czf anya.tar.gz *

echo "[2] Sending to VPS ($SERVER)..."
scp anya.tar.gz root@$SERVER:/root/

echo "[3] Deploying on VPS..."
ssh -t root@$SERVER "
cd /root &&
rm -rf anya &&
mkdir anya &&
tar xzf anya.tar.gz -C anya &&
cd anya &&
python3 -m venv venv &&
source venv/bin/activate &&
pip install -r requirements.txt &&
systemctl restart anya.service
"

echo "[4] Deployment complete."


