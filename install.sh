#!/bin/bash

# Aktualizace systému
echo "Updating system..."
sudo apt update -y
sudo apt full-upgrade -y

# Kontrola upgradovatelných balíčků
echo "Listing upgradable packages..."
apt list --upgradable -y

# Instalace základních balíčků
echo "Installing necessary packages..."
sudo apt install -y python3 python3-pip portaudio19-dev python3-fastapi python3-uvicorn lsof git git-lfs docker.io

# Instalace Seeed voicecard
echo "Installing Seeed voicecard..."
if [ -d /opt/audio/seeed-voicecard ]; then
    cd /opt/audio/seeed-voicecard
    sudo ./install.sh
else
    echo "Error: /opt/audio/seeed-voicecard not found. Skipping voicecard installation."
fi

# Přesun konfiguračního souboru ~/.asoundrc
echo "Setting up .asoundrc..."
if [ -f /opt/oldbot_audio/asoundrc ]; then
    mv /opt/oldbot_audio/asoundrc ~/.asoundrc
    echo "Moved /opt/oldbot_audio/asoundrc to ~/.asoundrc"
else
    echo "Error: /opt/oldbot_audio/asoundrc not found. Skipping."
fi

# Restart systému
echo "Installation complete. Restarting system..."
sudo reboot
