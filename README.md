# DevOps Demo Project

**Automated Design and Deployment of Applications using DevOps**

A complete DevOps pipeline: Flask app → GitHub → GitHub Actions CI/CD → DockerHub → Minikube (Kubernetes).

---

## Architecture

```
Developer pushes code
        │
        ▼
   GitHub (main)
        │
        ▼
GitHub Actions CI/CD
  ┌─────┴──────┐
  │  1. Test   │
  │  2. Build  │
  │  3. Push   │
  └─────┬──────┘
        │
        ▼
    DockerHub
        │
        ▼
  Minikube (local Kubernetes)
  ┌─────────────────────────┐
  │  Deployment (2 replicas) │
  │  Service (NodePort)      │
  └─────────────────────────┘
```

---

## Prerequisites

| Tool       | Version  |
|------------|----------|
| Ubuntu     | 20.04+   |
| Ansible    | 2.14+    |
| Git        | any      |
| Python     | 3.10+    |

---

## Step-by-Step Setup

### 1. Clone this repository

```bash
git clone https://github.com/<YOUR_USERNAME>/devops-demo-app.git
cd devops-demo-app
```

### 2. Install Ansible

```bash
sudo apt update
sudo apt install -y ansible
ansible --version
```

### 3. Run the Minikube Setup Playbook

This installs Docker, kubectl, and Minikube, then starts a local cluster using the Docker driver.

```bash
cd ansible
ansible-playbook -i inventory.ini setup-minikube.yml
```

After it completes, verify:

```bash
minikube status
kubectl get nodes
```

### 4. Add GitHub Secrets

Go to your repo → **Settings → Secrets and variables → Actions** and add:

| Secret Name          | Value                        |
|----------------------|------------------------------|
| `DOCKERHUB_USERNAME` | your DockerHub username      |
| `DOCKERHUB_TOKEN`    | DockerHub access token       |

> Create a DockerHub token at: https://hub.docker.com/settings/security

### 5. Push code and trigger the pipeline

```bash
git add .
git commit -m "feat: initial DevOps pipeline setup"
git push origin main
```

The GitHub Actions pipeline will automatically:
1. **Test** – run pytest on the Flask app
2. **Build** – build a multi-stage Docker image
3. **Push** – push the image to DockerHub

Monitor it at: `https://github.com/<YOUR_USERNAME>/devops-demo-app/actions`

### 6. Deploy to Minikube

After the pipeline pushes the image, deploy it locally:

```bash
cd ansible
ansible-playbook -i inventory.ini deploy-app.yml \
  -e "dockerhub_username=<YOUR_DOCKERHUB_USERNAME>"
```

Or deploy manually:

```bash
# Replace the placeholder in the manifest first
sed -i 's/<YOUR_DOCKERHUB_USERNAME>/YOUR_ACTUAL_USERNAME/g' k8s/deployment.yaml

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Wait for pods to be ready
kubectl rollout status deployment/devops-demo-app
```

### 7. Access the application

```bash
minikube service devops-demo-app-service --url
```

Open the printed URL in your browser. 🎉

---

## Project Structure

```
devops-demo-app/
├── app/
│   ├── app.py               # Flask application
│   ├── requirements.txt     # Python dependencies
│   └── templates/
│       └── index.html       # Web UI
├── k8s/
│   ├── deployment.yaml      # Kubernetes Deployment (2 replicas, rolling update)
│   └── service.yaml         # Kubernetes NodePort Service
├── ansible/
│   ├── inventory.ini        # Ansible inventory (localhost)
│   ├── setup-minikube.yml   # Playbook: install Docker + kubectl + Minikube
│   └── deploy-app.yml       # Playbook: deploy app to Minikube
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions: Test → Build → Push
├── Dockerfile               # Multi-stage Docker build
├── .gitignore
└── README.md
```

---

## CI/CD Pipeline Stages

| Stage  | Trigger          | Description                              |
|--------|------------------|------------------------------------------|
| Test   | Any push / PR    | pytest smoke tests on Flask app          |
| Build  | Push to `main`   | Multi-stage Docker image build           |
| Push   | After build      | Push image to DockerHub with SHA tag     |

---

## Useful Commands

```bash
# Check running pods
kubectl get pods

# View pod logs
kubectl logs -l app=devops-demo-app

# Scale deployment
kubectl scale deployment devops-demo-app --replicas=3

# Roll back to previous version
kubectl rollout undo deployment/devops-demo-app

# Open Kubernetes dashboard
minikube dashboard

# Pull latest image and redeploy
kubectl rollout restart deployment/devops-demo-app
```

---

## Course Outcome Mapping

| CO  | Metric                   | How this project fulfils it                        |
|-----|--------------------------|---------------------------------------------------|
| CO2 | Version Control          | Git branching, commits, PR workflow on GitHub     |
| CO3 | CI/CD Pipeline           | GitHub Actions: test → build → push (3 stages)   |
| CO5 | Containerization         | Multi-stage Dockerfile + Kubernetes (Minikube)    |
| CO5 | Infrastructure as Code   | Ansible playbooks for full environment setup      |
