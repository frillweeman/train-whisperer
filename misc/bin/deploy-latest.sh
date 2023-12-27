#!/bin/bash

# must be run as root
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script with sudo."
  exit 1
fi

cd /home/trainwhisperer/train-whisperer

git fetch

# Compare the local branch with the remote branch
if git diff --quiet HEAD origin/master; then
  echo "Local repository is already up to date."
  # TODO: check for -f flag to continue regardless
  if [[ "$1" != "-f" ]]; then
      exit 0
  fi
else
  # Perform a git pull if there are differences
  git pull origin master
  echo "Repository has been updated."
fi


# Compare the local Caddyfile with the one in /etc/caddy
if ! diff -q /home/trainwhisperer/train-whisperer/misc/Caddyfile /etc/caddy/Caddyfile >/dev/null; then
  systemctl stop caddy
  cp /home/trainwhisperer/train-whisperer/misc/Caddyfile /etc/caddy/Caddyfile
  systemctl start caddy
fi


# add /var/lib/mongodb if it doensn't exist
mongodb_data_dir="/var/lib/mongodb"
if [ ! -d "$mongodb_data_dir" ]; then
  sudo mkdir -p "$mongodb_data_dir"
  sudo chown -R trainwhisperer:trainwhisperer "$mongodb_data_dir"
  sudo chmod -R 777 "$mongodb_data_dir" # TODO: fix permissions instead of 777
  echo "Directory $mongodb_data_dir created."
fi

# building new docker-compose project
docker-compose down
docker-compose up --build -d

if [ $? -eq 0 ]; then
  echo "Docker Compose up succeeded. Pruning images."
  # Remove unused Docker images
  docker image prune -af
fi
