#!/bin/bash
set -e

# Configuration
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
SERVICE_NAME="skaut-backend"

echo "Deploying ${SERVICE_NAME} to Google Cloud Run in project ${PROJECT_ID}..."

# Build and deploy the container
gcloud run deploy ${SERVICE_NAME} \
    --source . \
    --region ${REGION} \
    --platform managed \
    --allow-unauthenticated \
    --update-secrets="GOOGLE_MAPS_API_KEY=GOOGLE_MAPS_API_KEY:latest,GOOGLE_GEMINI_API_KEY=GOOGLE_GEMINI_API_KEY:latest,ELASTIC_CLOUD_ID=ELASTIC_CLOUD_ID:latest,ELASTIC_USERNAME=ELASTIC_USERNAME:latest,ELASTIC_PASSWORD=ELASTIC_PASSWORD:latest,MONGODB_URI=MONGODB_URI:latest" \
    --update-env-vars="GCP_PROJECT_ID=${PROJECT_ID}" \
    --port 8000

echo "Deployment complete."
