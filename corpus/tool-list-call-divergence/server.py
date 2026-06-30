"""Tool registry -- the operation surface ADVERTISED to a caller and the surface actually
DISPATCHABLE are pruned by the same function, but a guard on that prune silently no-ops on the
empty-filter edge case -- so the un-pruned registry stays reachable through dispatch even though
the advertised list correctly shows empty."""

ALL_OPERATIONS = {"list": "read", "get": "read", "create": "write", "delete": "write", "admin_reset": "admin"}


def filter_tools(operation_map: dict, include) -> dict:
    filtered = {k: v for k, v in operation_map.items() if k in include}
    if filtered:        # VULN: an empty `include` -> guard skipped -> operation_map left un-pruned
        operation_map.clear()
        operation_map.update(filtered)
    return filtered      # the advertised list correctly reflects `filtered` (empty when include is empty)


def dispatch(operation_map: dict, name: str):
    # dispatch reads operation_map directly -- if filter_tools's guard no-op'd, every operation
    # (including ones never advertised) stays callable here
    return operation_map.get(name)
