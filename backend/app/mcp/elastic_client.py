import os

from elasticsearch import Elasticsearch


_elastic_client = None


class ElasticConfigurationError(RuntimeError):
    """Raised when Elasticsearch credentials are not available."""


def is_elastic_configured():
    return all(
        os.getenv(name)
        for name in (
            "ELASTIC_CLOUD_ID",
            "ELASTIC_USERNAME",
            "ELASTIC_PASSWORD",
        )
    )


def require_elastic_config():
    if not is_elastic_configured():
        raise ElasticConfigurationError(
            "Elasticsearch integration is not configured. Set "
            "ELASTIC_CLOUD_ID, ELASTIC_USERNAME, and ELASTIC_PASSWORD."
        )


def get_elastic_client():
    """
    Lazily initializes a shared Elasticsearch client for MCP tools.
    Existing Scout services keep their current clients for compatibility.
    """
    global _elastic_client

    if _elastic_client is None:
        require_elastic_config()
        _elastic_client = Elasticsearch(
            cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
            basic_auth=(
                os.getenv("ELASTIC_USERNAME"),
                os.getenv("ELASTIC_PASSWORD")
            )
        )

    return _elastic_client
