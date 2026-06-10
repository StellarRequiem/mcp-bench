"""Patched operation lister — an empty allowlist is REJECTED, never degraded to allow-all. Clean
negative / counterpart to empty-filter-bypass. A finding here is a false positive."""

ALL_OPERATIONS = ("list", "get", "create", "delete", "admin_reset")


def exposed_operations(allowed_filter) -> list:
    if not allowed_filter:
        raise ValueError("operation filter must be explicit")
    return [op for op in ALL_OPERATIONS if op in allowed_filter]
