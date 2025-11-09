#!/bin/bash
# RKE2 Cluster Installation Script
set -e

exec 3>&1 4>&2
exec 1> >(tee -a log.out >&3)
exec 2> >(tee -a error.out >&4)

CONFIG_FILE="rke2.conf"

# Check configuration for Installation
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"

else
    echo "ERROR: $CONFIG_FILE not found."
    exit 1
fi

INSTALL_RKE2_CHANNEL=${INSTALL_RKE2_CHANNEL:-stable}
INSTALL_RKE2_VERSION=${INSTALL_RKE2_VERSION:-latest}

echo -e "\n# ----- RKE2 Cluster Installation Script -----#"
echo -e "\nRKE2 will be installed with the following parameters:"
echo -e "\nInstalling RKE2 version: $INSTALL_RKE2_VERSION"
echo -e "\nRKE2 Channel: $INSTALL_RKE2_CHANNEL"
echo -e "\nRKE2 Type: $INSTALL_RKE2_TYPE"
read -p "Press Enter to continue or Ctrl+C to abort..."


# Download and install RKE2

if [ "$INSTALL_RKE2_VERSION" == "latest" ]; then
    curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE="$INSTALL_RKE2_TYPE" INSTALL_RKE2_CHANNEL="$INSTALL_RKE2_CHANNEL" sh -
else
    curl -sfL https://get.rke2.io | INSTALL_RKE2_VERSION="$INSTALL_RKE2_VERSION" INSTALL_RKE2_TYPE="$INSTALL_RKE2_TYPE" INSTALL_RKE2_CHANNEL="$INSTALL_RKE2_CHANNEL" sh -
fi

sudo systemctl enable rke2-server.service  
echo -e "\nStarting RKE2 $INSTALL_RKE2_TYPE service..."  

if [ "$INSTALL_RKE2_TYPE" == "agent" ]; then
    sudo systemctl enable rke2-agent.service  
    sudo mkdir -p /etc/rancher/rke2/
    
    echo -e "\nserver: $RKE2_SERVER_URL" | sudo tee /etc/rancher/rke2/config.yaml
    echo -e "\ntoken: $RKE2_TOKEN" | sudo tee -a /etc/rancher/rke2/config.yaml

    sudo systemctl start rke2-agent.service

    echo -e "\nRKE2 agent service started. Installation complete."
    exit 0

elif [ "$INSTALL_RKE2_TYPE" == "server" ]; then
    echo -e "\nRKE2 server service starting..."

    sudo systemctl enable rke2-server.service  
    sudo systemctl start rke2-server.service  

    echo -e "\nRKE2 server service started."
    echo -e "\nToken generated at /var/lib/rancher/rke2/server/token. Use this token to join agents to the cluster:"
    cat /var/lib/rancher/rke2/server/token

    echo -e "\nRKE2 server service started. Installation complete."
    echo -e "\nCreating symbolic links for rke2 binaries..."

    sudo ln -s /var/lib/rancher/rke2/bin/ctr /usr/local/bin/ctr
    sudo ln -s /var/lib/rancher/rke2/bin/crictl /usr/local/bin/crictl

    echo -e "\nKubectl configuration started for current user..."
    sudo ln -s /var/lib/rancher/rke2/bin/kubectl /usr/local/bin/kubectl
    mkdir -p $HOME/.kube
    sudo cp /etc/rancher/rke2/rke2.yaml $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config 
    exit 0
fi
