from collections import defaultdict
from threading import Lock


_lock = Lock()
_metrics = defaultdict(lambda: {"tool_calls": 0, "failures": 0, "total_latency_ms": 0.0})


def record_tool_call(tool: str, latency_ms: float, failed: bool) -> None:
    with _lock:
        metric = _metrics[tool]
        metric["tool_calls"] += 1
        metric["failures"] += int(failed)
        metric["total_latency_ms"] += latency_ms


def get_tool_metrics() -> dict:
    with _lock:
        return {
            tool: {
                **values,
                "average_latency_ms": round(
                    values["total_latency_ms"] / values["tool_calls"], 2
                ) if values["tool_calls"] else 0,
            }
            for tool, values in _metrics.items()
        }
