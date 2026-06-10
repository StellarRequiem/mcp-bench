"""Minimal MCP operation router — carries the operation-filter-bypass vulnerability
(the fastapi_mcp-001 class). A resource allowlist is meant to confine access, but the item id is
substituted into the request path UNENCODED, so a crafted id like "1/../../admin/keys" traverses out
of the allowed resource and reaches operations the filter was supposed to block."""

ALLOWED = ("items", "users")


def route(resource: str, item_id: str) -> str:
    if resource not in ALLOWED:                      # filter checks the resource...
        raise PermissionError("resource not allowed")
    # VULN: item_id is not percent-encoded before substitution -> path traversal escapes the filter
    return "/api/{resource}/{id}".replace("{resource}", resource).replace("{id}", item_id)
