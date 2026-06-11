import os
import logging

# We only import google.cloud.secretmanager when we need it
# to gracefully handle cases where ADC is not set up during early dev
try:
    from google.cloud import secretmanager
    SECRET_MANAGER_AVAILABLE = True
except ImportError:
    SECRET_MANAGER_AVAILABLE = False

logger = logging.getLogger(__name__)

# Configuration
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "")


def get_secret(name: str) -> str:
    """
    Retrieves a secret from Google Secret Manager.
    Falls back to local environment variables if Secret Manager is not available
    or if the secret is not found.
    """
    local_val = os.getenv(name)
    
    if not GCP_PROJECT_ID or not SECRET_MANAGER_AVAILABLE:
        logger.warning(f"Secret Manager not fully configured (GCP_PROJECT_ID={GCP_PROJECT_ID}). Falling back to local env for {name}.")
        return local_val or ""

    try:
        client = secretmanager.SecretManagerServiceClient()
        # The Secret Manager path requires the project ID and the secret name.
        # "latest" means we pull the most recently created version of the secret.
        name_path = f"projects/{GCP_PROJECT_ID}/secrets/{name}/versions/latest"
        
        response = client.access_secret_version(request={"name": name_path})
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        logger.error(f"Failed to fetch secret {name} from Secret Manager: {e}")
        return local_val or ""
