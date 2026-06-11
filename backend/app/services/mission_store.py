import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from datetime import datetime

load_dotenv()

es = Elasticsearch(
    cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
    basic_auth=(
        os.getenv("ELASTIC_USERNAME"),
        os.getenv("ELASTIC_PASSWORD")
    )
)

def save_mission(mission):
    mission["created_at"] = datetime.utcnow().isoformat()

    # Exclude metadata from the doc body sent to ES
    doc = {k: v for k, v in mission.items() if k not in ["_elastic_id", "_seq_no", "_primary_term"]}

    response = es.index(
        index="missions",
        document=doc
    )

    mission["_elastic_id"] = response["_id"]
    mission["_seq_no"] = response["_seq_no"]
    mission["_primary_term"] = response["_primary_term"]

    return mission

def get_latest_mission(team):
    result = es.search(
        index="missions",
        size=1,
        seq_no_primary_term=True,
        query={
            "term": {
                "team": team
            }
        },
        sort=[
            {
                "created_at": {
                    "order": "desc"
                }
            }
        ]
    )

    hits = result["hits"]["hits"]

    if not hits:
        return None

    mission = hits[0]["_source"]
    mission["_elastic_id"] = hits[0]["_id"]
    mission["_seq_no"] = hits[0]["_seq_no"]
    mission["_primary_term"] = hits[0]["_primary_term"]

    return mission


def get_mission_history(team, size=20):
    result = es.search(
        index="missions",
        size=size,
        query={"term": {"team": team}},
        sort=[{"created_at": {"order": "desc"}}],
    )
    return [hit["_source"] for hit in result["hits"]["hits"]]

def update_mission(mission):
    mission["updated_at"] = datetime.utcnow().isoformat()

    elastic_id = mission.get("_elastic_id")
    seq_no = mission.get("_seq_no")
    primary_term = mission.get("_primary_term")

    # Exclude metadata from the doc body sent to ES
    doc = {k: v for k, v in mission.items() if k not in ["_elastic_id", "_seq_no", "_primary_term"]}

    update_params = {
        "index": "missions",
        "id": elastic_id,
        "doc": doc
    }

    if seq_no is not None and primary_term is not None:
        update_params["if_seq_no"] = seq_no
        update_params["if_primary_term"] = primary_term

    response = es.update(**update_params)

    if "result" in response and response["result"] in ["updated", "noop"]:
        if "_seq_no" in response:
            mission["_seq_no"] = response["_seq_no"]
        if "_primary_term" in response:
            mission["_primary_term"] = response["_primary_term"]

    return response
