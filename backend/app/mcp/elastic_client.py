import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch


_elastic_client = None


def get_elastic_client():
    """
    Lazily initializes a shared Elasticsearch client for MCP tools.
    Existing Scout services keep their current clients for compatibility.
    """
    global _elastic_client

    if _elastic_client is None:
        load_dotenv()
        _elastic_client = Elasticsearch(
            cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
            basic_auth=(
                os.getenv("ELASTIC_USERNAME"),
                os.getenv("ELASTIC_PASSWORD")
            )
        )

    return _elastic_client
