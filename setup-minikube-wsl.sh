#!/bin/bash
# =============================================================================
# Setup Minikube on Ubuntu WSL2 - Run inside WSL Ubuntu terminal
# =============================================================================

set -e

echo "🚀 Starting Minikube setup in WSL2..."

# 1. Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# 2. Install prerequisites
echo "📦 Installing system dependencies..."
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    conntrack \
    socat \
    git

# 3. Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER

# 4. Install kubectl
echo "☸️  Installing kubectl..."
KUBECTL_VERSION="v1.30.0"
curl -L "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" -o /tmp/kubectl
sudo chmod +x /tmp/kubectl
sudo mv /tmp/kubectl /usr/local/bin/kubectl
kubectl version --client

# 5. Install Minikube
echo "🐳 Installing Minikube..."
MINIKUBE_VERSION="v1.33.0"
curl -L "https://storage.googleapis.com/minikube/releases/${MINIKUBE_VERSION}/minikube-linux-amd64" -o /tmp/minikube
sudo chmod +x /tmp/minikube
sudo mv /tmp/minikube /usr/local/bin/minikube
minikube version

# 6. Start Minikube cluster
echo "🚀 Starting Minikube with Docker driver..."
minikube start \
    --driver=docker \
    --cpus=2 \
    --memory=2200mb \
    --addons=ingress

# 7. Enable addons
echo "⚙️  Enabling Kubernetes addons..."
minikube addons enable metrics-server
minikube addons enable dashboard

# 8. Verify setup
echo "✅  Verifying cluster..."
kubectl get nodes -o wide

echo ""
echo "================================================"
echo "✅  Minikube setup complete!"
echo "================================================"
echo ""
echo "📍 Next steps:"
echo "  1. Run: kubectl get pods --all-namespaces"
echo "  2. Run: docker ps  (to verify Docker integration)"
echo "  3. For dashboard: minikube dashboard"
echo "  4. For app deployment: ansible-playbook -i inventory.ini deploy-app.yml"
echo ""
