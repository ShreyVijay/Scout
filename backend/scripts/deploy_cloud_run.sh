#!/bin/bash
set -e

# Configuration
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"
SERVICE_NAME="scout-backend"
SERVICE_ACCOUNT="scout-service-account@${PROJECT_ID}.iam.gserviceaccount.com"

echo "Deploying ${SERVICE_NAME} to Google Cloud Run in project ${PROJECT_ID}..."

# Build and deploy the container
gcloud run deploy ${SERVICE_NAME} \
    --source . \
    --region ${REGION} \
    --platform managed \
    --allow-unauthenticated \
    --service-account ${SERVICE_ACCOUNT} \
    --set-secrets="GOOGLE_MAPS_API_KEY=GOOGLE_MAPS_API_KEY:latest,GOOGLE_GEMINI_API_KEY=GOOGLE_GEMINI_API_KEY:latest" \
    --set-env-vars="GCP_PROJECT_ID=${PROJECT_ID}" \
    --port 8000

echo "Deployment complete."
