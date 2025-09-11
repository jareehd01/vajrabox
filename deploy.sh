#!/bin/bash

# Set your ECR details
ECR_URI="YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com"
REPO_NAME="vajrabox"
CLUSTER_NAME="YOUR_CLUSTER"
SERVICE_NAME="YOUR_SERVICE"

echo "Building Docker image for AMD64..."
docker build --platform linux/amd64 -t $REPO_NAME .

echo "Tagging image..."
docker tag $REPO_NAME:latest $ECR_URI/$REPO_NAME:latest

echo "Logging into ECR..."
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_URI

echo "Pushing to ECR..."
docker push $ECR_URI/$REPO_NAME:latest

echo "Updating ECS service..."
aws ecs update-service --cluster $CLUSTER_NAME --service $SERVICE_NAME --force-new-deployment

echo "Deployment initiated!"


aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 940482408383.dkr.ecr.ap-south-1.amazonaws.com
docker build --platform linux/amd64 -t vajrabox/vajrabox-be -f .devcontainer/Dockerfile .
docker tag vajrabox/vajrabox-be:latest 940482408383.dkr.ecr.ap-south-1.amazonaws.com/vajrabox/vajrabox-be:latest
docker push 940482408383.dkr.ecr.ap-south-1.amazonaws.com/vajrabox/vajrabox-be:latest
