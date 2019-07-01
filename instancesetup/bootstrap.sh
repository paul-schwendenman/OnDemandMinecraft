#!/usr/bin/env bash

MINECRAFT_HOME="/srv/minecraft-server"
MINECRAFT_USER="minecraft"
MINECRAFT_GROUP="minecraft"

# Setup minecraft user
sudo adduser --system --home $MINECRAFT_HOME $MINECRAFT_USER
sudo addgroup --system $MINECRAFT_GROUP
sudo adduser $MINECRAFT_USER $MINECRAFT_GROUP
sudo chown -R $MINECRAFT_USER.$MINECRAFT_GROUP $MINECRAFT_HOME

# Install java
sudo apt update
sudo apt install -y openjdk-11-jdk-headless

# Download server
wget https://launcher.mojang.com/v1/objects/d0d0fe2b1dc6ab4c65554cb734270872b72dadd6/server.jar
sudo mv server.jar $MINECRAFT_HOME/minecraft_server.jar

# Install EULA
sudo mv eula.txt $MINECRAFT_HOME

# Install cron job
chmod +x /home/ubuntu/autoshutdown.sh
sudo crontab /home/ubuntu/crontab

# Install systemd service
sudo cp minecraft-server.service /etc/systemd/system/minecraft-server.service

# Start minecraft
sudo service minecraft-server start
