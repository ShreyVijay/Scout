import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from functools import wraps
from time import perf_counter

from scout_mcp.dependencies import tool_timeout_seconds
from scout_mcp.metrics import record_tool_call
from scout_mcp.schemas.base import error_response, success_response


logger = logging.getLogger("scout.mcp")
registry = {}
_executor = ThreadPoolExecutor(max_workers=8, thread_name_prefix="scout-mcp")

EXPECTED_TOOLS = {
    "get_mission",
    "get_mission_history",
    "search_cities",
    "get_city",
    "search_stadiums",
    "get_stadium",
    "get_budget",
    "get_preferences",
    "get_team_status",
    "get_tournament_state",
    "get_recommendation",
    "get_reasoning",
    "get_audit"
}


def tool(name: str | None = None):
    def decorator(func):
        tool_name = name or func.__name__

        @wraps(func)
        def wrapped(*args, **kwargs):
            started = perf_counter()
            failed = False
            try:
                future = _executor.submit(func, *args, **kwargs)
                data = future.result(timeout=tool_timeout_seconds())
                latency_ms = round((perf_counter() - started) * 1000, 2)
                logger.info("mcp_tool_success tool=%s latency_ms=%s", tool_name, latency_ms)
                return success_response(tool_name, data, latency_ms)
            except TimeoutError:
                failed = True
                latency_ms = round((perf_counter() - started) * 1000, 2)
                logger.error("mcp_tool_timeout tool=%s latency_ms=%s", tool_name, latency_ms)
                return error_response(
                    tool_name,
                    TimeoutError(f"Tool exceeded {tool_timeout_seconds()} second timeout"),
                    latency_ms,
                )
            except Exception as exc:
                failed = True
                latency_ms = round((perf_counter() - started) * 1000, 2)
                logger.exception("mcp_tool_failure tool=%s latency_ms=%s", tool_name, latency_ms)
                return error_response(tool_name, exc, latency_ms)
            finally:
                record_tool_call(
                    tool_name,
                    round((perf_counter() - started) * 1000, 2),
                    failed,
                )

        registry[tool_name] = wrapped
        return wrapped

    return decorator


def register_tools(mcp_server) -> None:
    registered = set(registry.keys())
    if registered != EXPECTED_TOOLS:
        missing = EXPECTED_TOOLS - registered
        extra = registered - EXPECTED_TOOLS
        raise RuntimeError(f"Tool registry mismatch. Missing: {missing}, Extra: {extra}")

    for name, func in registry.items():
        mcp_server.tool(name=name)(func)


def list_tools() -> list[str]:
    return sorted(registry)
