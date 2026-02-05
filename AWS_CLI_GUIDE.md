# ☁️ AWS Infrastructure Setup via CLI

This guide provides the exact AWS CLI commands to set up the infrastructure for the **Kidney Disease Classification** project.

---

## 🛠️ Prerequisites
1. **AWS CLI installed** on your local machine.
2. **AWS CLI configured** with your credentials (`aws configure`).
3. **Region set** (e.g., `us-east-1`).

---

## 📦 Step 1: Create ECR Repository
Create the private repository where your Docker images will be stored.

```bash
# Replace 'kidney-disease' with your preferred name
aws ecr create-repository --repository-name kidney-disease --region us-east-1
```

**Note the Output:** You will need the `repositoryUri` later for your GitHub Secrets.
Example: `888888888888.dkr.ecr.us-east-1.amazonaws.com/kidney-disease`

---

## 🔐 Step 2: Network & Security Setup

### 1. Create a Security Group
This allows you to access the app on port 8080 and SSH into the server.

```bash
# Get your default VPC ID
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" --query "Vpcs[0].VpcId" --output text)

# Create the Security Group
SG_ID=$(aws ec2 create-security-group \
    --group-name kidney-sg \
    --description "Security group for Kidney Project" \
    --vpc-id $VPC_ID \
    --query "GroupId" \
    --output text)

echo "Security Group ID: $SG_ID"
```

### 2. Configure Inbound Rules
```bash
# Allow SSH (Port 22)
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0

# Allow App Traffic (Port 8080)
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 8080 --cidr 0.0.0.0/0
```

---

## 🚀 Step 3: Launch EC2 Instance

Launch a `t2.medium` instance (recommended for TensorFlow) with Ubuntu 22.04.

```bash
# Find Ubuntu 22.04 AMI (Example for us-east-1)
AMI_ID=$(aws ec2 describe-images --owners 099720109477 \
    --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
    --query "sort_by(Images, &CreationDate)[-1].ImageId" --output text)

# Launch Instance
# Replace <your-key-pair-name> with your actual key pair name
aws ec2 run-instances \
    --image-id $AMI_ID \
    --count 1 \
    --instance-type t2.medium \
    --key-name <your-key-pair-name> \
    --security-group-ids $SG_ID \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=kidney-server}]'
```

---

## 🐳 Step 4: Configure EC2 (SSH into server)
Once the instance is running, connect via SSH and install Docker:

```bash
# Replace with your EC2 Public IP
ssh -i "your-key.pem" ubuntu@<your-ec2-ip>

# Run these ON the EC2:
sudo apt-get update -y
sudo apt-get install docker.io -y
sudo usermod -aG docker ubuntu
newgrp docker
```

---

## 🤖 Step 5: Setup GitHub Runner
On your EC2, follow the steps from your GitHub Repository:
**Settings > Actions > Runners > New self-hosted runner**

Copy and paste the commands provided by GitHub into your SSH terminal.

---

## 🔐 Step 6: GitHub Secrets Checklist
Go to **Settings > Secrets and variables > Actions** and add:

| Secret Name | Value Example |
|-------------|---------------|
| `AWS_ACCESS_KEY_ID` | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | `your-secret-key` |
| `AWS_REGION` | `us-east-1` |
| `ECR_REPOSITORY_NAME` | `kidney-disease` |
| `AWS_ECR_LOGIN_URI` | `888888888.dkr.ecr.us-east-1.amazonaws.com` |

---

### ⚠️ Pro-Tip for Free Tier
The **t2.medium** is NOT in the free tier (approx $0.04/hr), but it is needed for TensorFlow stability. If you want 100% free, use **t2.micro**, but the application may be slow or crash during prediction if it runs out of RAM.
