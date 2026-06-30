"""Clean negative / counterpart to tool-list-call-divergence: the prune always applies
unconditionally, even when the filter is empty, so the advertised and dispatchable surfaces can
never diverge. A finding here is a false positive."""

ALL_OPERATIONS = {"list": "read", "get": "read", "create": "write", "delete": "write", "admin_reset": "admin"}


def filter_tools(operation_map: dict, include) -> dict:
    filtered = {k: v for k, v in operation_map.items() if k in include}
    operation_map.clear()      # always applied -- no guard to skip, even when `filtered` is empty
    operation_map.update(filtered)
    return filtered


def dispatch(operation_map: dict, name: str):
    return operation_map.get(name)
