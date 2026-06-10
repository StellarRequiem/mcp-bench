"""Minimal MCP operation lister — carries the empty-filter-bypass vulnerability (the fastapi_mcp-003
class). An operation allowlist is supposed to restrict what's exposed, but when the filter is empty
the check degrades to allow-ALL, so an empty or omitted filter silently exposes every operation —
including privileged ones."""

ALL_OPERATIONS = ("list", "get", "create", "delete", "admin_reset")


def exposed_operations(allowed_filter) -> list:
    # VULN: when allowed_filter is empty, `not allowed_filter` is True -> every operation passes the gate
    return [op for op in ALL_OPERATIONS if not allowed_filter or op in allowed_filter]
