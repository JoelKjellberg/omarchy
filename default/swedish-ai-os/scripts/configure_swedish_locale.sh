#!/usr/bin/env bash
set -euo pipefail

echo "Configuring Swedish locale, keymap and timezone on Arch-like systems..."

echo "1) Enable locale in /etc/locale.gen"
sudo sed -i 's/^#\s*sv_SE.UTF-8 UTF-8/sv_SE.UTF-8 UTF-8/' /etc/locale.gen
sudo locale-gen

echo "2) Set system locale and keyboard"
sudo localectl set-locale LANG=sv_SE.UTF-8
sudo localectl set-keymap sv-latin1
sudo localectl set-x11-keymap se

echo "3) Set timezone"
sudo timedatectl set-timezone Europe/Stockholm

echo "Swedish base locale configuration complete."
