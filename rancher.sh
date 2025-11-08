#!/bin/bash
# Rancher Cluster Installation Script
set -e
exec 3>&1 4>&2
exec 1> >(tee -a rancher_log.out >&3)
exec 2> >(tee -a rancher_error.out >&4)

echo -e "\n# ----- Rancher Cluster Installation Script -----#"
echo -e "\nChecking Helm and kubectl installation..."

if ! command -v helm &> /dev/null
then
    echo -e "\nHelm could not be found. Do you want to install Helm now? (y/n): "
    read -r INSTALL_HELM
    if [[ "$INSTALL_HELM" == "y" ]]; then
        curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
    else
        echo -e "\nHelm installation aborted."
        exit 1
    fi
fi

if ! command -v kubectl &> /dev/null
then
    echo -e "\nKubectl could not be found. Please install Kubectl before proceeding or add to your PATH."
    exit 1
fi

read -p "Enter Rancher Version or latest (e.g., v2.7.5): " RANCHER_VERSION
read -p "Enter chart repo name  stable, latest,alpha (default: stable): " CHART_REPO_NAME
CHART_REPO_NAME=${CHART_REPO_NAME:-stable}
read -p "Enter namespace (default: cattle-system): " NAMESPACE  
NAMESPACE=${NAMESPACE:-cattle-system}
read -p "Enter SSL Configuration self-signed/lets-encrypt/custom, more info https://ranchermanager.docs.rancher.com/getting-started/installation-and-upgrade/install-upgrade-on-a-kubernetes-cluster#3-choose-your-ssl-configuration 
(default: lets-encrypt): " SSL_CONFIG
SSL_CONFIG=${SSL_CONFIG:-lets-encrypt}

echo -e "\nRancher will be installed with the following parameters:"
echo -e "\nRancher Version (e.g 2.7.0) : $RANCHER_VERSION"
echo -e "\nChart Repo Name: $CHART_REPO_NAME"
echo -e "\nNamespace: $NAMESPACE"
echo -e "\nSSL Configuration: $SSL_CONFIG"
read -p "Press Enter to continue or Ctrl+C to abort..."

# Add Helm repo and update
helm repo add rancher-$CHART_REPO_NAME https://releases.rancher.com/server-charts/$CHART_REPO_NAME
helm repo update

# Create namespace
kubectl create namespace $NAMESPACE

if [ "$SSL_CONFIG" == "self-signed" ] || [ "$SSL_CONFIG" == "custom" ]; then
    helm repo add jetstack https://charts.jetstack.io
    helm repo update
    helm install cert-manager jetstack/cert-manager \
        --namespace cert-manager \
        --create-namespace \
        --set crds.enabled=true
    
    echo -e "\nWaiting for cert-manager to be ready..."
    kubectl wait --namespace cert-manager \
      --for=condition=available deployment/cert-manager \
      --timeout=120s
fi
# Install Rancher

if [Chart Repo Name]

