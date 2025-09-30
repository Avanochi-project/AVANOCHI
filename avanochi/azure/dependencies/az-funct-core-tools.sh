#!/usr/bin/env bash
set -e

echo "[1. Installing basic dependencies...]"
sudo apt-get update -qq >/dev/null
sudo apt-get install -y -qq gnupg2 curl lsb-release apt-transport-https ca-certificates libicu-dev >/dev/null

echo "[2. Cleaning previous broken repos...]"
sudo rm -f /etc/apt/sources.list.d/azure-functions.list
sudo rm -f /etc/apt/trusted.gpg.d/microsoft.gpg

echo "[3. Adding Microsoft public key...]"
curl -sL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor 2>/dev/null | sudo tee /etc/apt/trusted.gpg.d/microsoft.gpg >/dev/null

echo "[4. Configuring Azure Functions repository (forcing bullseye for compatibility)...]"
echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-debian-bullseye-prod bullseye main" \
  | sudo tee /etc/apt/sources.list.d/azure-functions.list

echo "[5. Updating package index...]"
sudo apt-get update

echo "[6. Installing Azure Functions Core Tools v4...]"
sudo apt-get install -y azure-functions-core-tools-4

echo "✅ Installation completed. Installed version:"
func --version
