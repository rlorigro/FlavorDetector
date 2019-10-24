#!/bin/bash

sudo apt-get install jq

# ---- Adapted from https://askubuntu.com/a/928514 ----

INSTALL_DIR="/usr/local/bin"

curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest > temp.json
url=$(cat temp.json | jq -r '.assets[].browser_download_url | select(contains("linux64"))')
curl -s -L "$url" | tar -xz
chmod +x geckodriver
sudo mv geckodriver "$INSTALL_DIR"
rm temp.json
echo "installed geckodriver binary in $INSTALL_DIR"

# ----


