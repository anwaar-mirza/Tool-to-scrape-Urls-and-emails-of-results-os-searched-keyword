#!/bin/bash

# Update and install necessary packages
apt-get update
apt-get install -y wget unzip

# Install specific version of Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt-get -f install -y

# Install ChromeDriver that matches the installed Chrome version
wget https://chromedriver.storage.googleapis.com/120.0.6099.224/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/chromedriver

# Set permissions
chmod +x /usr/local/bin/chromedriver
