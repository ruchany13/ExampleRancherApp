#!/bin/bash
# Rancher Cluster Installation Script
set -e
exec 3>&1 4>&2
exec 1> >(tee -a rancher_log.out >&3)
exec 2> >(tee -a rancher_error.out >&4)

CONFIG_FILE="rancher.conf"

# Check configuration for Installation
if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"

else
    echo "ERROR: $CONFIG_FILE not found."
    exit 1
fi

echo -e "\n# ----- Rancher Cluster Installation Script -----#"
echo -e "\nChecking Helm and kubectl installation..."

if ! command -v kubectl &> /dev/null
then
    echo -e "\nKubectl could not be found. Please install Kubectl before proceeding or add to your PATH."
    exit 1
fi

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

CHART_REPO_NAME=${CHART_REPO_NAME:-stable}
NAMESPACE=${NAMESPACE:-cattle-system}
SSL_CONFIG=${SSL_CONFIG:-lets-encrypt}
PRIVATE_CA=${PRIVATE_CA:-false}

echo -e "\nRancher will be installed with the following parameters:"
echo -e "\nRancher Version : $RANCHER_VERSION"
echo -e "\nChart Repo Name: $CHART_REPO_NAME"
echo -e "\nNamespace: $NAMESPACE"
echo -e "\nSSL Configuration: $SSL_CONFIG"
read -p "Press Enter to continue or Ctrl+C to abort..."

# Add Helm repo and update
helm repo add rancher-$CHART_REPO_NAME https://releases.rancher.com/server-charts/$CHART_REPO_NAME
helm repo update

# Create namespace
kubectl create namespace $NAMESPACE

# Install cert-manager for Rancher Generated Certificates and Let’s Encrypt

if [ "$SSL_CONFIG" == "self-signed" ] || [ "$SSL_CONFIG" == "lets-encrypt" ]; then
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

# Install Rancher with specific SSL Configuration

if [ "$SSL_CONFIG" == "self-signed" ]; then
    if [ "$CHART_REPO_NAME" == "alpha" ]; then

        helm install rancher rancher-$CHART_REPO_NAME/rancher \
            --devel \
            --namespace $NAMESPACE \
            --set hostname=$HOSTNAME \
            --set bootstrapPassword=$PASSWORD \
            --version=$RANCHER_VERSION
            
    else
        helm install rancher rancher-$CHART_REPO_NAME/rancher \
            --namespace $NAMESPACE \
            --set hostname=$HOSTNAME \
            --set bootstrapPassword=$PASSWORD \
            --version=$RANCHER_VERSION
    fi

elif [ "$SSL_CONFIG" == "lets-encrypt" ]; then
    # Take Let's Encrypt CA and add Kubernetes
    curl -sL -o /tmp/cacerts.pem https://letsencrypt.org/certs/isrgrootx1.pem
    kubectl -n $NAMESPACE create secret generic tls-ca \
        --from-file=/tmp/cacerts.pem
    
    if [ "$CHART_REPO_NAME" == "alpha" ]; then
        helm install rancher rancher-$CHART_REPO_NAME/rancher \
            --devel \
            --namespace $NAMESPACE \
            --set hostname=$HOSTNAME \
            --set bootstrapPassword=$PASSWORD \
            --set ingress.tls.source=letsEncrypt \
            --set letsEncrypt.email=$SSL_MAIL \
            --set letsEncrypt.ingress.class=$INGRESS_CLASS \
            --version=$RANCHER_VERSION \
            --set privateCA=true           
    else
        helm install rancher rancher-$CHART_REPO_NAME/rancher \
            --namespace $NAMESPACE \
            --set hostname=$HOSTNAME \
            --set bootstrapPassword=$PASSWORD \
            --set ingress.tls.source=letsEncrypt \
            --set letsEncrypt.email=$SSL_MAIL \
            --set letsEncrypt.ingress.class=$INGRESS_CLASS \
            --version=$RANCHER_VERSION \
            --set privateCA=true
    fi

elif [ "$SSL_CONFIG" == "custom" ]; then
    kubectl -n cattle-system create secret tls tls-rancher-ingress \
        --cert=$TLS_PATH \
        --key=$KEY_PATH
    
    if [ "$PRIVATE_CA" ]; then
        kubectl -n $NAMESPACE create secret generic tls-ca \
            --from-file=$PRIVATE_CA_PATH
    fi

    if [ "$CHART_REPO_NAME" == "alpha" ]; then
            helm install rancher rancher-$CHART_REPO_NAME/rancher \
                --namespace $NAMESPACE \
                --set hostname=$HOSTNAME \
                --set bootstrapPassword=$PASSWORD \
                --set ingress.tls.source=secret \
                --version=$RANCHER_VERSION \
                --set privateCA=$PRIVATE_CA
        else
            helm install rancher rancher-$CHART_REPO_NAME/rancher \
                --namespace $NAMESPACE \
                --set hostname=$HOSTNAME \
                --set bootstrapPassword=$PASSWORD \
                --set ingress.tls.source=secret \
                --version=$RANCHER_VERSION \
                --set privateCA=$PRIVATE_CA \
                --devel
        fi
fi

