#!/usr/bin/env bash
set -e

echo "[1] Installing prerequisites..."
sudo apt-get update -qq >/dev/null
sudo apt-get install -y -qq python3 python3-pip >/dev/null

echo "[2] Installing Azure CLI via pip..."
python3 -m pip install --upgrade --user azure-cli >/dev/null

echo "[3] Adding Azure CLI to PATH..."
export PATH=$PATH:~/.local/bin
if ! grep -q 'export PATH=.*~/.local/bin' ~/.bashrc; then
  echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
fi

echo "✅ Azure CLI installation completed. Installed version:"
az --version
