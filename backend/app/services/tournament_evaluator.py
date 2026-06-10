from app.services.event_store import (
    get_next_unprocessed_event,
    mark_event_processed
)

from app.services.mission_store import (
    get_latest_mission,
    update_mission
)

from app.services.state_update_service import (
    update_tournament_state
)

from app.services.mission_state_service import (
    update_mission_state
)

from app.services.mission_state_resolver import (
    resolve_mission_state
)

from app.services.replanning_trigger import (
    needs_replanning
)

def process_latest_event(team):

    event = get_next_unprocessed_event(team)

    if not event:
        return None

    mission = get_latest_mission(team)

    if not mission:
        return None

    current_state = mission["tournament_state"]

    if current_state != event["from_stage"]:
        # Mark event as processed so that it is skipped and does not block the queue
        mark_event_processed(event["_event_id"])
        return {
            "error": "stale_event",
            "current_state": current_state,
            "event_from": event["from_stage"]
        }

    mission = update_tournament_state(
        mission,
        event["to_stage"]
    )

    new_mission_state = resolve_mission_state(
        mission["tournament_state"],
        mission["mission_state"]
    )

    if new_mission_state != mission["mission_state"]:
        mission = update_mission_state(
            mission,
            new_mission_state
        )

    mission["requires_replanning"] = needs_replanning(
        current_state,
        event["to_stage"]
    )

    update_mission(
        mission
    )

    # Mark event as processed after successful update
    mark_event_processed(event["_event_id"])

    return mission